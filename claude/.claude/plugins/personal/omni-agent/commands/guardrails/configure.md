---
description: View and configure guardrails settings
argument-hint: "[list|status|patterns|risk|storage|session]"
allowed-tools: Read, Bash
---

# Guardrails Configuration

View and understand the omni-agent safety guardrails.

**Action**: "$ARGUMENTS"

## Actions

### list (default)
Show all configured guardrails:
- Blocked patterns (CRITICAL)
- Confirmation required (RED)
- Warning patterns (YELLOW)
- Network-sensitive patterns

### status
Show current guardrails status, last 10 operations with guard tier classification:

Read the rollback registry and display:
| # | Time | Tool | Action | Tier | Details |
|---|------|------|--------|------|---------|

Tier is determined by checking the operation against pattern lists.

### patterns
Show detailed regex patterns used for detection

### risk
Compute and display the current session risk score:

Read the session state from `~/.claude/omni-agent/sessions/` and display:

| Metric | Value |
|--------|-------|
| Session ID | ... |
| Risk Score | X points |
| Escalation Active | Yes/No (threshold: 10) |
| Cooldown Active | Yes/No (threshold: 20) |
| Total Events | N |
| RED events | N (+3 pts each) |
| YELLOW events | N (+1 pt each) |

```bash
# Quick risk score check:
python3 -c "
import sys; sys.path.insert(0, '$HOME/.claude/plugins/personal/omni-agent/hooks/scripts')
from lib.risk_session import get_session_info
import json; print(json.dumps(get_session_info(), indent=2))
"
```

### storage
Show snapshot directory statistics:

```bash
# Snapshot storage stats:
echo '--- Snapshot Storage ---'
SNAP_DIR="$HOME/.claude/omni-agent/snapshots"
if [ -d "$SNAP_DIR" ]; then
  echo "Location: $SNAP_DIR"
  echo "Snap files: $(find "$SNAP_DIR" -name '*.snap' | wc -l)"
  echo "Total size: $(du -sh "$SNAP_DIR" 2>/dev/null | cut -f1)"
  if [ -f "$SNAP_DIR/index.json" ]; then
    echo "Index entries: $(python3 -c "import json; print(len(json.load(open('$SNAP_DIR/index.json')).get('snapshots', {})))")"
  fi
else
  echo "No snapshots directory found"
fi
```

### session
Show current session operations grouped by tool, with reversibility status:

```bash
python3 -c "
import json, sys, os
sys.path.insert(0, os.path.expanduser('~/.claude/plugins/personal/omni-agent/hooks/scripts'))
from lib.registry import load_registry
from lib.risk_session import _get_session_id

reg = load_registry()
sid = _get_session_id()
ops = [o for o in reg['operations'] if o.get('session_id') == sid]
print(f'Session: {sid}')
print(f'Operations: {len(ops)}')
for op in ops:
    rb = 'ROLLED BACK' if op.get('rolled_back') else 'active'
    snap = 'yes' if op.get('snapshot_hash') else 'no'
    print(f\"  {op['id'][:8]} | {op['tool']:12} | snap:{snap} | {rb}\")
"
```

## Guardrail Levels

### CRITICAL (Blocked)
These operations are ALWAYS blocked (permissionDecision: deny):
- `rm -rf /` — Recursive delete from root
- `dd if=... of=/dev/` — Direct disk write
- Fork bombs
- Piping remote content to shell
- Force push to main/master
- `git clean -fd` — Remove untracked files
- `truncate -s 0` — Zero out files
- Reverse shells (nc, bash, socat, python)
- Kernel modules (modprobe, insmod, rmmod)
- Firewall rules (iptables, nft, ufw)
- Base64-to-shell pipes

### RED (Denied)
These are DENIED with explanation (permissionDecision: deny):
- `sudo` commands
- System upgrades (`pacman -Syu`)
- Package removal
- Service management
- Git push operations
- Deleting files (`rm -rf`)
- Modifying .env or credentials
- Crontab/at job scheduling
- Process killing (kill, killall, pkill)
- System tracing (strace, ltrace)

### YELLOW (Warn)
These show a warning but proceed:
- `chmod 777`
- Configuration file changes
- Recursive ownership changes
- Network operations on sensitive files

## Evasion Resistance

Commands are normalized before matching:
- `$HOME` and `~` expanded to actual home path
- Split flags merged (`rm -r -f` → `rm -rf`)
- Path traversal resolved (`../../etc/passwd` → `/etc/passwd`)
- Base64 payloads decoded and appended for matching

## Configuration Location

Guardrails are defined in:
`~/.claude/plugins/personal/omni-agent/hooks/scripts/pretooluse_guard.py`

Pattern definitions in:
`~/.claude/plugins/personal/omni-agent/hooks/scripts/lib/patterns.py`

## Rollback Registry

Operations are tracked in:
`~/.claude/omni-agent/rollback_registry.json`

Use `/omni-agent:rollback` to view and revert operations.

## Snapshots

Pre-modification snapshots stored at:
`~/.claude/omni-agent/snapshots/`

Snapshots auto-expire after 7 days.
