#!/usr/bin/env python3
"""
Omni-Agent Post-Tool Use Tracker

Tracks operations for potential rollback:
- Logs all file modifications with before/after state
- Tracks bash commands for audit trail
- Maintains rollback registry (v2) for recovery
- Picks up pre-modification snapshot references from PreToolUse

Registry stored at: ~/.claude/omni-agent/rollback_registry.json
Pending snapshots at: ~/.claude/omni-agent/pending_snapshots/<key>.json
"""

import hashlib
import json
import sys
from pathlib import Path

# Add scripts directory to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.registry import add_operation

# Pending snapshots directory (written by pretooluse_guard.py)
PENDING_DIR = Path.home() / ".claude" / "omni-agent" / "pending_snapshots"


def get_hook_input():
    """Read hook input from stdin."""
    try:
        return json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return {}


def _pending_key(tool_name: str, file_path: str) -> str:
    """Compute pending snapshot key from tool name and file path."""
    return hashlib.md5(f"{tool_name}:{file_path}".encode()).hexdigest()


def _read_pending_snapshot(tool_name: str, tool_input: dict) -> str | None:
    """Read and consume a pending snapshot reference from PreToolUse.

    Returns snapshot_hash if found, None otherwise.
    """
    # Determine file path based on tool type
    file_path = ""
    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
    elif tool_name == "MultiEdit":
        file_path = tool_input.get("file_path", "")
    elif tool_name == "NotebookEdit":
        file_path = tool_input.get("notebook_path", "")

    if not file_path:
        return None

    key = _pending_key(tool_name, file_path)
    pending_file = PENDING_DIR / f"{key}.json"

    if pending_file.exists():
        try:
            data = json.loads(pending_file.read_text())
            snapshot_hash = data.get("snapshot_hash")
            # Clean up the pending file
            pending_file.unlink(missing_ok=True)
            return snapshot_hash
        except (json.JSONDecodeError, OSError):
            pass

    return None


def main():
    """Main entry point."""
    hook_input = get_hook_input()

    tool_name = hook_input.get("toolName", "")
    tool_input = hook_input.get("toolInput", {})
    tool_output = hook_input.get("toolOutput", "")

    # Read pending snapshot from PreToolUse (if any)
    snapshot_hash = _read_pending_snapshot(tool_name, tool_input)

    # Track the operation via registry v2
    add_operation(
        tool_name=tool_name,
        tool_input=tool_input,
        tool_output=tool_output,
        snapshot_hash=snapshot_hash,
    )

    # Return empty response (no modifications to output)
    print(json.dumps({}))


if __name__ == "__main__":
    main()
