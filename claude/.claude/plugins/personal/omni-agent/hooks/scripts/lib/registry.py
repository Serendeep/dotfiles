"""
Omni-Agent Rollback Registry v2

Enhanced operation tracking with:
- Schema version field for migration support
- UUID-based operation IDs
- Session ID linking
- Rollback status tracking
- Snapshot hash references
- NotebookEdit and Task tool tracking
- 500-entry limit (up from 100)

Registry stored at: ~/.claude/omni-agent/rollback_registry.json
"""

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_DIR = Path.home() / ".claude" / "omni-agent"
REGISTRY_FILE = REGISTRY_DIR / "rollback_registry.json"
MAX_ENTRIES = 500
SCHEMA_VERSION = 2


def _get_session_id() -> str:
    """Get session ID from environment or fallback to PPID."""
    sid = os.environ.get("CLAUDE_SESSION_ID", "")
    if sid:
        return sid
    return str(os.getppid())


def ensure_registry():
    """Ensure the registry directory and file exist."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.write_text(json.dumps({
            "version": SCHEMA_VERSION,
            "operations": []
        }, indent=2))


def load_registry() -> dict:
    """Load the rollback registry, migrating if needed."""
    ensure_registry()
    try:
        data = json.loads(REGISTRY_FILE.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        data = {"operations": []}

    # Migrate v1 → v2 if needed
    if data.get("version", 1) < SCHEMA_VERSION:
        data = migrate_registry(data)
        save_registry(data)

    return data


def save_registry(registry: dict):
    """Save the rollback registry, keeping only last MAX_ENTRIES."""
    registry["version"] = SCHEMA_VERSION
    registry["operations"] = registry["operations"][-MAX_ENTRIES:]
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2))


def migrate_registry(v1_data: dict) -> dict:
    """Migrate v1 registry to v2 schema.

    Adds: version, id, session_id, rolled_back, rolled_back_at, snapshot_hash
    """
    migrated_ops = []
    for op in v1_data.get("operations", []):
        migrated_ops.append({
            "id": str(uuid.uuid4()),
            "session_id": "migrated",
            "timestamp": op.get("timestamp", ""),
            "tool": op.get("tool", ""),
            "reversible": op.get("reversible", False),
            "details": op.get("details", {}),
            "rolled_back": False,
            "rolled_back_at": None,
            "snapshot_hash": None,
        })
    return {
        "version": SCHEMA_VERSION,
        "operations": migrated_ops,
    }


def compute_hash(content) -> str | None:
    """Compute SHA256 hash of content (truncated to 16 chars)."""
    if content is None:
        return None
    data = content.encode() if isinstance(content, str) else content
    return hashlib.sha256(data).hexdigest()[:16]


def add_operation(tool_name: str, tool_input: dict, tool_output: str = "",
                  snapshot_hash: str = None):
    """Add an operation to the registry.

    Args:
        tool_name: Name of the tool (Write, Edit, Bash, etc.)
        tool_input: Tool input parameters
        tool_output: Tool output (optional)
        snapshot_hash: Pre-modification snapshot hash (optional)
    """
    registry = load_registry()

    operation = {
        "id": str(uuid.uuid4()),
        "session_id": _get_session_id(),
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "tool": tool_name,
        "reversible": False,
        "details": {},
        "rolled_back": False,
        "rolled_back_at": None,
        "snapshot_hash": snapshot_hash,
    }

    if tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")
        operation["details"] = {
            "file_path": file_path,
            "content_hash": compute_hash(content),
            "content_length": len(content),
        }
        operation["reversible"] = True

    elif tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        operation["details"] = {
            "file_path": file_path,
            "old_string": old_string[:100] + "..." if len(old_string) > 100 else old_string,
            "new_string": new_string[:100] + "..." if len(new_string) > 100 else new_string,
        }
        operation["reversible"] = True

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        operation["details"] = {
            "command": command[:200] + "..." if len(command) > 200 else command,
        }
        if command.strip().startswith("git "):
            operation["reversible"] = True

    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        operation["details"] = {
            "file_count": len(edits),
            "files": [e.get("file_path", "") for e in edits[:5]],
        }
        operation["reversible"] = True

    elif tool_name == "NotebookEdit":
        notebook_path = tool_input.get("notebook_path", "")
        edit_mode = tool_input.get("edit_mode", "replace")
        operation["details"] = {
            "notebook_path": notebook_path,
            "edit_mode": edit_mode,
            "cell_type": tool_input.get("cell_type", ""),
        }
        operation["reversible"] = True

    elif tool_name == "Task":
        prompt = tool_input.get("prompt", "")
        operation["details"] = {
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "subagent_type": tool_input.get("subagent_type", ""),
        }
        operation["reversible"] = False

    # Only track if we have details
    if operation["details"]:
        registry["operations"].append(operation)
        save_registry(registry)
