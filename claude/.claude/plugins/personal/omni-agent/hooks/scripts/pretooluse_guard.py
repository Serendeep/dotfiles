#!/usr/bin/env python3
"""
Omni-Agent Pre-Tool Use Guardrails

Strict safety system that:
- BLOCKS critical/dangerous patterns (rm -rf /, fork bombs, etc.)
- DENIES high-risk operations with explanation (sudo, delete, system changes)
- WARNS on moderate-risk operations (permissive perms, config changes)
- Normalizes commands to defeat evasion (variable expansion, flag merging, base64)
- Tracks session risk score with escalation and cooldown
- Creates pre-modification snapshots for rollback capability

Risk Levels:
- CRITICAL: Block entirely (no bypass) → permissionDecision: deny
- RED: Deny with explanation → permissionDecision: deny
- YELLOW: Warn but proceed → systemMessage only
- GREEN: Silent pass → empty response
"""

import hashlib
import json
import os
import random
import re
import sys
from pathlib import Path

# Add scripts directory to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.patterns import (
    BLOCKED_PATTERNS,
    CONFIRM_PATTERNS,
    NETWORK_SENSITIVE_PATTERNS,
    TASK_DANGEROUS_PATTERNS,
    WARN_PATTERNS,
)
from lib.normalizer import normalize_command
from lib.risk_session import (
    cleanup_old_sessions,
    is_in_cooldown,
    record_event,
    should_escalate,
)
from lib.snapshot import cleanup_old_snapshots, create_snapshot

# Pending snapshots directory (read by posttooluse_tracker.py)
PENDING_DIR = Path.home() / ".claude" / "omni-agent" / "pending_snapshots"


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_hook_input():
    """Read hook input from stdin."""
    try:
        return json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return {}


def check_patterns(text, patterns):
    """Check text against a list of patterns. Returns (matched, reason) or (None, None)."""
    for pattern, reason in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return pattern, reason
    return None, None


def check_with_normalization(command, patterns):
    """Check both raw and normalized command against patterns.

    Returns (matched_pattern, reason) or (None, None).
    """
    normalized = normalize_command(command)
    # Use a set to avoid duplicate matching when normalization is a no-op
    candidates = {command}
    candidates.add(normalized)

    for candidate in candidates:
        pattern, reason = check_patterns(candidate, patterns)
        if pattern:
            return pattern, reason
    return None, None


def check_network_sensitive(command):
    """Check for network operations targeting sensitive files.

    Returns reason string or None.
    """
    for net_pattern, sensitive_pattern, reason in NETWORK_SENSITIVE_PATTERNS:
        if re.search(net_pattern, command, re.IGNORECASE):
            if re.search(sensitive_pattern, command, re.IGNORECASE):
                return reason
    return None


# =============================================================================
# EVALUATION FUNCTIONS
# =============================================================================

def evaluate_bash_command(command):
    """Evaluate a bash command for safety."""
    # Check BLOCKED patterns first (with normalization)
    pattern, reason = check_with_normalization(
        command, BLOCKED_PATTERNS.get("bash", [])
    )
    if pattern:
        return "block", reason, pattern

    # Check CONFIRM patterns (with normalization)
    pattern, reason = check_with_normalization(
        command, CONFIRM_PATTERNS.get("bash", [])
    )
    if pattern:
        return "confirm", reason, pattern

    # Check WARN patterns (with normalization)
    pattern, reason = check_with_normalization(
        command, WARN_PATTERNS.get("bash", [])
    )
    if pattern:
        return "warn", reason, pattern

    # Check network-sensitive patterns
    net_reason = check_network_sensitive(command)
    if net_reason:
        # Also check normalized form
        if not net_reason:
            normalized = normalize_command(command)
            net_reason = check_network_sensitive(normalized)
        if net_reason:
            return "warn", net_reason, "network_sensitive"

    return "allow", None, None


def evaluate_file_operation(file_path, tool_name):
    """Evaluate a file operation for safety."""
    # Check CONFIRM patterns for files
    pattern, reason = check_patterns(file_path, CONFIRM_PATTERNS.get("file", []))
    if pattern:
        return "confirm", reason, pattern

    # Check WARN patterns for files
    pattern, reason = check_patterns(file_path, WARN_PATTERNS.get("file", []))
    if pattern:
        return "warn", reason, pattern

    return "allow", None, None


def evaluate_task_prompt(prompt):
    """Evaluate a Task agent prompt for dangerous instructions."""
    pattern, reason = check_patterns(prompt, TASK_DANGEROUS_PATTERNS)
    if pattern:
        return "confirm", reason, pattern
    return "allow", None, None


# =============================================================================
# RESPONSE GENERATION
# =============================================================================

def create_response(action, reason=None, pattern=None):
    """Create the appropriate hook response.

    CRITICAL FIX: Both 'block' and 'confirm' now emit permissionDecision: deny.
    Previous bug: 'confirm' only emitted systemMessage, LLM proceeded anyway.
    """
    if action == "block":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny"
            },
            "systemMessage": (
                f"BLOCKED by omni-agent guardrails: {reason}\n\n"
                "This operation has been blocked for safety. "
                "If you believe this is a false positive, please review the command carefully."
            )
        }
    elif action == "confirm":
        # FIX: Now actually denies instead of just warning
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny"
            },
            "systemMessage": (
                f"DENIED by omni-agent guardrails (RED): {reason}\n\n"
                "This is a potentially dangerous operation that has been denied. "
                "If you need to perform this operation, the user must approve it "
                "through Claude Code's permission system."
            )
        }
    elif action == "warn":
        return {
            "systemMessage": (
                f"WARNING (omni-agent): {reason}\n\n"
                "Proceeding with caution."
            )
        }
    else:
        return {}


# =============================================================================
# SNAPSHOT MANAGEMENT
# =============================================================================

def _pending_key(tool_name, file_path):
    """Compute pending snapshot key from tool name and file path."""
    return hashlib.md5(f"{tool_name}:{file_path}".encode()).hexdigest()


def create_pre_modification_snapshot(tool_name, file_path):
    """Create a snapshot before file modification and write pending reference.

    The pending reference is picked up by posttooluse_tracker.py.
    """
    snap_hash = create_snapshot(file_path)
    if snap_hash:
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        key = _pending_key(tool_name, file_path)
        pending_file = PENDING_DIR / f"{key}.json"
        pending_file.write_text(json.dumps({
            "snapshot_hash": snap_hash,
            "file_path": file_path,
            "tool": tool_name,
        }))


# =============================================================================
# PROBABILISTIC CLEANUP
# =============================================================================

def maybe_run_cleanup():
    """Run cleanup on ~1 in 50 invocations."""
    if random.randint(1, 50) == 1:
        try:
            cleanup_old_sessions()
        except Exception:
            pass
        try:
            cleanup_old_snapshots()
        except Exception:
            pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    hook_input = get_hook_input()

    tool_name = hook_input.get("toolName", "")
    tool_input = hook_input.get("toolInput", {})

    # --- Cooldown check (top priority) ---
    in_cooldown, remaining = is_in_cooldown()
    if in_cooldown:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny"
            },
            "systemMessage": (
                f"SESSION COOLDOWN ACTIVE ({remaining}s remaining): "
                "Too many risky operations detected in this session. "
                "All tool use is temporarily suspended. "
                "Please wait for the cooldown to expire."
            )
        }))
        return

    # --- Evaluate based on tool type ---
    action = "allow"
    reason = None
    pattern = None
    file_path = None

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        action, reason, pattern = evaluate_bash_command(command)

    elif tool_name in ("Write", "Edit", "MultiEdit"):
        file_path = tool_input.get("file_path", "")
        action, reason, pattern = evaluate_file_operation(file_path, tool_name)

    elif tool_name == "NotebookEdit":
        file_path = tool_input.get("notebook_path", "")
        action, reason, pattern = evaluate_file_operation(file_path, tool_name)

    elif tool_name == "Task":
        prompt = tool_input.get("prompt", "")
        action, reason, pattern = evaluate_task_prompt(prompt)

    # --- Risk session escalation ---
    if action == "warn" and should_escalate():
        # Escalate YELLOW → RED when session risk is high
        action = "confirm"
        reason = f"ESCALATED (high session risk): {reason}"

    # --- Record risk events ---
    if action == "block" or action == "confirm":
        record_event("red", tool_name, reason or "unknown")
    elif action == "warn":
        record_event("yellow", tool_name, reason or "unknown")

    # --- Create pre-modification snapshots for allowed/warned file operations ---
    if action in ("allow", "warn") and tool_name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        snap_path = file_path
        if not snap_path:
            if tool_name == "NotebookEdit":
                snap_path = tool_input.get("notebook_path", "")
            else:
                snap_path = tool_input.get("file_path", "")
        if snap_path:
            try:
                create_pre_modification_snapshot(tool_name, snap_path)
            except Exception:
                pass  # Don't block operations if snapshot fails

    # --- Generate response ---
    response = create_response(action, reason, pattern)
    print(json.dumps(response))

    # --- Probabilistic cleanup ---
    maybe_run_cleanup()


if __name__ == "__main__":
    main()
