"""
Omni-Agent Content-Addressed File Snapshot Storage

Creates pre-modification snapshots for rollback capability:
- Content-addressed: duplicate files share one snapshot
- Git-tracked files: stores git blob reference (lightweight)
- Non-git files: stores full file bytes as .snap file
- Skips files > 10MB or non-existent files (new file creates)

Storage: ~/.claude/omni-agent/snapshots/
Index:   ~/.claude/omni-agent/snapshots/index.json
"""

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOTS_DIR = Path.home() / ".claude" / "omni-agent" / "snapshots"
INDEX_FILE = SNAPSHOTS_DIR / "index.json"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
GIT_TIMEOUT = 2  # seconds
SNAPSHOT_EXPIRY_DAYS = 7


def _ensure_dir():
    """Ensure snapshots directory exists."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def _load_index() -> dict:
    """Load snapshot index."""
    _ensure_dir()
    if INDEX_FILE.exists():
        try:
            return json.loads(INDEX_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"snapshots": {}}


def _save_index(index: dict):
    """Save snapshot index."""
    _ensure_dir()
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def _hash_bytes(data: bytes) -> str:
    """Compute SHA256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def _is_git_tracked(file_path: str) -> bool:
    """Check if a file is tracked by git."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", file_path],
            capture_output=True, timeout=GIT_TIMEOUT,
            cwd=str(Path(file_path).parent)
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def _get_git_blob_ref(file_path: str) -> str | None:
    """Get git blob reference for the current version of a file."""
    try:
        # Get the relative path from repo root
        root_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=GIT_TIMEOUT,
            cwd=str(Path(file_path).parent)
        )
        if root_result.returncode != 0:
            return None
        repo_root = root_result.stdout.strip()
        rel_path = str(Path(file_path).resolve().relative_to(repo_root))

        result = subprocess.run(
            ["git", "rev-parse", f"HEAD:{rel_path}"],
            capture_output=True, text=True, timeout=GIT_TIMEOUT,
            cwd=repo_root
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ValueError):
        pass
    return None


def create_snapshot(file_path: str) -> str | None:
    """Create a pre-modification snapshot of a file.

    Args:
        file_path: Absolute path to the file to snapshot

    Returns:
        Hash string if snapshot created, None if skipped
    """
    path = Path(file_path)

    # Skip non-existent files (new file creation)
    if not path.exists():
        return None

    # Skip files over size limit
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return None
    except OSError:
        return None

    _ensure_dir()
    index = _load_index()

    # Try git blob reference first (lightweight)
    if _is_git_tracked(file_path):
        blob_ref = _get_git_blob_ref(file_path)
        if blob_ref:
            # Use git blob ref as the hash key
            snap_hash = f"git:{blob_ref}"
            index["snapshots"][snap_hash] = {
                "type": "git_blob",
                "blob_ref": blob_ref,
                "file_path": str(path.resolve()),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            _save_index(index)
            return snap_hash

    # Fallback: store full file bytes
    try:
        data = path.read_bytes()
    except OSError:
        return None

    content_hash = _hash_bytes(data)
    snap_file = SNAPSHOTS_DIR / f"{content_hash}.snap"

    # Content-addressed: skip writing if already exists
    if not snap_file.exists():
        snap_file.write_bytes(data)

    index["snapshots"][content_hash] = {
        "type": "file",
        "file_path": str(path.resolve()),
        "size": len(data),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_index(index)
    return content_hash


def get_snapshot_content(snap_hash: str) -> bytes | None:
    """Retrieve snapshot content by hash.

    Args:
        snap_hash: Hash from create_snapshot()

    Returns:
        File bytes or None if not found
    """
    if snap_hash.startswith("git:"):
        blob_ref = snap_hash[4:]
        try:
            result = subprocess.run(
                ["git", "cat-file", "-p", blob_ref],
                capture_output=True, timeout=GIT_TIMEOUT
            )
            if result.returncode == 0:
                return result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        return None

    snap_file = SNAPSHOTS_DIR / f"{snap_hash}.snap"
    if snap_file.exists():
        try:
            return snap_file.read_bytes()
        except OSError:
            pass
    return None


def cleanup_old_snapshots():
    """Remove snapshot entries and files older than SNAPSHOT_EXPIRY_DAYS."""
    if not SNAPSHOTS_DIR.exists():
        return

    index = _load_index()
    now = time.time()
    cutoff = SNAPSHOT_EXPIRY_DAYS * 86400
    active_hashes = set()
    to_remove = []

    for snap_hash, info in index.get("snapshots", {}).items():
        created = info.get("created_at", "")
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            age = now - created_dt.timestamp()
            if age > cutoff:
                to_remove.append(snap_hash)
            else:
                if not snap_hash.startswith("git:"):
                    active_hashes.add(snap_hash)
        except (ValueError, TypeError):
            to_remove.append(snap_hash)

    # Remove expired entries from index
    for h in to_remove:
        index["snapshots"].pop(h, None)
    _save_index(index)

    # Remove orphaned .snap files
    for snap_file in SNAPSHOTS_DIR.glob("*.snap"):
        file_hash = snap_file.stem
        if file_hash not in active_hashes:
            try:
                snap_file.unlink()
            except OSError:
                pass
