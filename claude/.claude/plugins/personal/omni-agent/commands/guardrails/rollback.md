---
description: View operation history and rollback changes
argument-hint: "[list|last-N|to-timestamp|diff OP_ID|restore OP_ID|session [ID]]"
allowed-tools: Read, Bash, Task
---

# Rollback Operations

View tracked operations and revert changes.

**Action**: "$ARGUMENTS"

## Actions

### list (default)
Show recent tracked operations from rollback registry.

Display in table format:
| ID | Time | Tool | File/Command | Reversible | Snapshot | Rolled Back |
|----|------|------|--------------|------------|----------|-------------|

### last-N
Analyze and optionally rollback last N operations.
Example: `last-5`

### to-timestamp
Rollback all operations after a specific timestamp.
Example: `to-2024-01-15T10:30:00Z`

### diff OP_ID
Show a unified diff between the pre-modification snapshot and the current file state.

```bash
# Find operation by ID prefix
python3 -c "
import json, sys, os, subprocess, tempfile
sys.path.insert(0, os.path.expanduser('~/.claude/plugins/personal/omni-agent/hooks/scripts'))
from lib.registry import load_registry
from lib.snapshot import get_snapshot_content

reg = load_registry()
target = '$ARGUMENTS'.split()[-1] if '$ARGUMENTS' else ''
for op in reg['operations']:
    if op['id'].startswith(target):
        snap = op.get('snapshot_hash')
        fpath = op['details'].get('file_path') or op['details'].get('notebook_path', '')
        if snap:
            content = get_snapshot_content(snap)
            if content:
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.snap', delete=False) as f:
                    f.write(content)
                    tmp = f.name
                print(f'--- Snapshot ({snap[:12]})')
                print(f'+++ Current ({fpath})')
                subprocess.run(['diff', '-u', tmp, fpath])
                os.unlink(tmp)
            else:
                print('Snapshot content not available')
        else:
            print('No snapshot for this operation')
        break
"
```

### restore OP_ID
Restore a file from its pre-modification snapshot.

**Workflow**:
1. Find the operation by ID prefix
2. Create a **safety snapshot** of the file's current state (so this restore can itself be undone)
3. Retrieve snapshot content
4. Write snapshot content to the file
5. Verify restoration
6. Mark operation as `rolled_back` in registry

```bash
python3 -c "
import json, sys, os
sys.path.insert(0, os.path.expanduser('~/.claude/plugins/personal/omni-agent/hooks/scripts'))
from lib.registry import load_registry, save_registry
from lib.snapshot import get_snapshot_content, create_snapshot
from datetime import datetime, timezone

reg = load_registry()
target = '$ARGUMENTS'.split()[-1] if '$ARGUMENTS' else ''
for op in reg['operations']:
    if op['id'].startswith(target):
        snap = op.get('snapshot_hash')
        fpath = op['details'].get('file_path') or op['details'].get('notebook_path', '')
        if not snap:
            print('No snapshot available for this operation')
            break
        content = get_snapshot_content(snap)
        if not content:
            print('Snapshot content not retrievable')
            break
        # Safety snapshot
        safety = create_snapshot(fpath)
        print(f'Safety snapshot created: {safety}')
        # Restore
        with open(fpath, 'wb') as f:
            f.write(content)
        print(f'Restored {fpath} from snapshot {snap[:12]}')
        # Mark as rolled back
        op['rolled_back'] = True
        op['rolled_back_at'] = datetime.now(timezone.utc).isoformat() + 'Z'
        save_registry(reg)
        print('Registry updated')
        break
"
```

### session [SESSION_ID]
View operations grouped by session, or rollback an entire session.

Without SESSION_ID: lists all sessions with operation counts.
With SESSION_ID: shows all operations for that session with rollback option.

For batch session rollback, process operations in **reverse chronological order**.

## Workflow

1. **Load Registry**
   Read from `~/.claude/omni-agent/rollback_registry.json`

2. **Parse Request**
   Determine scope of rollback

3. **Analyze Operations**
   For rollback requests, launch `rollback-advisor` agent to:
   - Show operations to be reverted
   - Calculate dependencies
   - Assess risk
   - Check for available snapshots

4. **Confirm with User**
   Display what will be changed and get confirmation

5. **Execute Rollback** (in priority order)
   - **Snapshot restore**: If `snapshot_hash` exists, restore from snapshot
   - **Git restore**: If file is git-tracked, restore from git
   - **Edit reversal**: Swap old/new strings
   - **Manual**: Provide guidance for manual restoration

6. **Safety Protocol**
   - Create safety snapshot of current state BEFORE any restore
   - Perform rollback
   - Verify correct state

7. **Update Registry**
   Set `rolled_back: true` and `rolled_back_at` on restored operations

## Registry Format (v2)

```json
{
  "version": 2,
  "operations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "session_id": "abc123",
      "timestamp": "2024-01-15T10:30:00Z",
      "tool": "Write",
      "reversible": true,
      "details": {
        "file_path": "/path/to/file",
        "content_hash": "abc123..."
      },
      "rolled_back": false,
      "rolled_back_at": null,
      "snapshot_hash": "a1b2c3d4e5f6..."
    }
  ]
}
```

## Limitations

- Only tracks operations since plugin was enabled
- Snapshots expire after 7 days
- Files > 10MB are not snapshotted
- Non-git, non-snapshotted files may not be fully recoverable
- Some bash operations are not reversible
- Task (sub-agent) operations cannot be reversed
