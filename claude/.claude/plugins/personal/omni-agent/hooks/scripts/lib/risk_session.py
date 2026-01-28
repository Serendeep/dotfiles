"""
Omni-Agent Session Risk Accumulation

Tracks cumulative risk score across a Claude Code session:
- YELLOW events: +1 point
- RED events: +3 points
- At 10 points: all YELLOW auto-escalates to RED (deny)
- At 20 points: 60-second cooldown — ALL tools denied

State stored at: ~/.claude/omni-agent/sessions/<session_id>.json
Sessions auto-expire after 24h, stale files cleaned after 48h.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_DIR = Path.home() / ".claude" / "omni-agent" / "sessions"
ESCALATION_THRESHOLD = 10
COOLDOWN_THRESHOLD = 20
COOLDOWN_SECONDS = 60
SESSION_EXPIRY_HOURS = 24
STALE_CLEANUP_HOURS = 48


def _get_session_id() -> str:
    """Get session ID from environment or fallback to PPID."""
    sid = os.environ.get("CLAUDE_SESSION_ID", "")
    if sid:
        return sid
    return str(os.getppid())


def _session_path(session_id: str = None) -> Path:
    """Get path to session state file."""
    if session_id is None:
        session_id = _get_session_id()
    return SESSIONS_DIR / f"{session_id}.json"


def _load_session(session_id: str = None) -> dict:
    """Load session state or create new."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = _session_path(session_id)
    if path.exists():
        try:
            data = json.loads(path.read_text())
            # Check expiry
            created = data.get("created_at", "")
            if created:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                age_hours = (datetime.now(timezone.utc) - created_dt).total_seconds() / 3600
                if age_hours > SESSION_EXPIRY_HOURS:
                    # Expired — start fresh
                    return _new_session()
            return data
        except (json.JSONDecodeError, ValueError, KeyError):
            return _new_session()
    return _new_session()


def _new_session() -> dict:
    """Create new session state."""
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "score": 0,
        "events": [],
        "cooldown_until": None,
    }


def _save_session(data: dict, session_id: str = None):
    """Save session state."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = _session_path(session_id)
    path.write_text(json.dumps(data, indent=2))


def record_event(level: str, tool: str, reason: str):
    """Record a risk event.

    Args:
        level: "yellow" (+1pt) or "red" (+3pt)
        tool: tool name that triggered the event
        reason: human-readable reason
    """
    session = _load_session()
    points = 3 if level == "red" else 1
    session["score"] += points
    session["events"].append({
        "time": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "tool": tool,
        "reason": reason,
        "points": points,
    })
    # Keep last 200 events
    session["events"] = session["events"][-200:]

    # Check if cooldown should activate
    if session["score"] >= COOLDOWN_THRESHOLD and not session.get("cooldown_until"):
        session["cooldown_until"] = (
            datetime.now(timezone.utc).timestamp() + COOLDOWN_SECONDS
        )

    _save_session(session)


def should_escalate() -> bool:
    """Check if YELLOW should auto-escalate to RED (score >= 10)."""
    session = _load_session()
    return session["score"] >= ESCALATION_THRESHOLD


def is_in_cooldown() -> tuple:
    """Check if session is in cooldown (score >= 20).

    Returns:
        (is_cooled_down: bool, remaining_seconds: int)
    """
    session = _load_session()
    cooldown_until = session.get("cooldown_until")
    if cooldown_until is None:
        return False, 0
    now = datetime.now(timezone.utc).timestamp()
    if now < cooldown_until:
        remaining = int(cooldown_until - now)
        return True, remaining
    # Cooldown expired — reset it (but keep score)
    session["cooldown_until"] = None
    _save_session(session)
    return False, 0


def get_session_info() -> dict:
    """Get current session info for display."""
    session = _load_session()
    return {
        "session_id": _get_session_id(),
        "score": session["score"],
        "escalation_active": session["score"] >= ESCALATION_THRESHOLD,
        "cooldown_active": session.get("cooldown_until") is not None,
        "event_count": len(session["events"]),
        "created_at": session.get("created_at", ""),
    }


def cleanup_old_sessions():
    """Remove session files older than STALE_CLEANUP_HOURS."""
    if not SESSIONS_DIR.exists():
        return
    now = time.time()
    cutoff = STALE_CLEANUP_HOURS * 3600
    for path in SESSIONS_DIR.glob("*.json"):
        try:
            age = now - path.stat().st_mtime
            if age > cutoff:
                path.unlink()
        except OSError:
            pass
