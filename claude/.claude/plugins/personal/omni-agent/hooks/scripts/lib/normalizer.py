"""
Omni-Agent Command Normalization Engine

Transforms raw shell commands into canonical form for reliable pattern matching.
Defeats simple evasion techniques:
- Variable expansion ($HOME, ~)
- Flag splitting (rm -r -f → rm -rf)
- Path traversal (../../etc/passwd → /etc/passwd)
- Base64 encoded payloads

All operations are pure string/regex — no subprocess calls.
"""

import base64
import os
import re


def normalize_command(raw: str) -> str:
    """Run all normalizations on a raw command string. Returns canonical form."""
    result = raw
    result = expand_variables(result)
    result = normalize_flags(result)
    result = resolve_path_traversal(result)
    result = detect_base64(result)
    return result


def expand_variables(cmd: str) -> str:
    """Safe allowlist expansion of common shell variables to actual values."""
    home = os.path.expanduser("~")
    # Expand $HOME and ${HOME}
    cmd = cmd.replace("${HOME}", home)
    cmd = cmd.replace("$HOME", home)
    # Expand ~ at word boundaries (start of path)
    cmd = re.sub(r'(?<![\\])~(?=/|$|\s)', home, cmd)
    return cmd


def normalize_flags(cmd: str) -> str:
    """Merge separated single-char flags into combined form.

    Example: rm -r -f → rm -rf
    Only merges flags that are single-dash single-character groups.
    """
    # Match a command followed by multiple separated short flags
    # e.g., "rm -r -f" → "rm -rf"
    # e.g., "chmod -R -v" → "chmod -Rv"
    def merge_flags(match):
        prefix = match.group(1)  # command + space
        flags_str = match.group(2)  # the flag groups like "-r -f"
        # Extract individual flag characters
        chars = []
        for part in re.findall(r'-([a-zA-Z]+)', flags_str):
            chars.extend(list(part))
        if chars:
            return prefix + "-" + "".join(chars)
        return match.group(0)

    # Pattern: word followed by 2+ separated short flag groups
    # Matches: "rm -r -f", "rm -r -f -v", "chmod -R -v"
    result = re.sub(
        r'(\b\w+\s+)((?:-[a-zA-Z]+\s+)+-[a-zA-Z]+)',
        merge_flags,
        cmd
    )
    return result


def resolve_path_traversal(cmd: str) -> str:
    """Normalize path segments containing ../ using os.path.normpath."""
    def norm_path(match):
        path = match.group(0)
        if ".." in path:
            return os.path.normpath(path)
        return path

    # Match path-like segments (starts with /, ./, or ../)
    result = re.sub(
        r'(?:[/.][^\s]*\.\.[^\s]*)',
        norm_path,
        cmd
    )
    return result


def detect_base64(cmd: str) -> str:
    """Find base64-encoded payloads in echo|base64-d patterns and append decoded form.

    If a base64 payload is detected and decodable, appends it as:
    <original_command> __DECODED__:<decoded_string>
    """
    # Match patterns like: echo "BASE64" | base64 -d
    # or: echo BASE64 | base64 --decode
    pattern = r'echo\s+["\']?([A-Za-z0-9+/=]{4,})["\']?\s*\|\s*base64\s+(?:-d|--decode)'
    match = re.search(pattern, cmd)
    if match:
        encoded = match.group(1)
        try:
            decoded = base64.b64decode(encoded).decode("utf-8", errors="replace")
            # Only append if we got readable text
            if decoded and all(c.isprintable() or c.isspace() for c in decoded):
                return cmd + " __DECODED__:" + decoded
        except Exception:
            pass
    return cmd
