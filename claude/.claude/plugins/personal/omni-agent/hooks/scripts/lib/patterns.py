"""
Omni-Agent Pattern Definitions

Centralized pattern lists for guardrail matching across all tiers:
- BLOCKED (CRITICAL): Always denied, no bypass
- CONFIRM (RED): Denied with explanation
- WARN (YELLOW): Allowed with system warning
- NETWORK_SENSITIVE: Warn on network + sensitive file combinations
"""

# =============================================================================
# CRITICAL: These are ALWAYS blocked — no exceptions
# =============================================================================
BLOCKED_PATTERNS = {
    "bash": [
        # Recursive deletes from critical paths
        (r'rm\s+-[rf]*\s+/', "Recursive delete from root directory"),
        (r'rm\s+-[rf]*\s+~/', "Recursive delete from home directory"),
        (r'rm\s+-[rf]*\s+\*', "Recursive delete with wildcard"),
        # Disk and filesystem
        (r'dd\s+if=.*of=/dev/', "Direct disk write operation"),
        (r'mkfs\.', "Filesystem format operation"),
        (r':\s*\(\s*\)\s*\{', "Potential fork bomb detected"),
        (r'>\s*/dev/sd[a-z]', "Direct device overwrite"),
        (r'chmod\s+-R\s+777\s+/', "Insecure permissions on root"),
        # Remote code execution
        (r'curl.*\|\s*(ba)?sh', "Piping remote content to shell"),
        (r'wget.*\|\s*(ba)?sh', "Piping remote content to shell"),
        (r'eval\s+"\$\(curl', "Eval of remote content"),
        # System file overwrites
        (r'>\s*/etc/passwd', "Overwriting passwd file"),
        (r'>\s*/etc/shadow', "Overwriting shadow file"),
        # Force push to protected branches
        (r'--force\s+.*push.*main', "Force push to main branch"),
        (r'--force\s+.*push.*master', "Force push to master branch"),
        (r'push\s+.*--force.*main', "Force push to main branch"),
        (r'push\s+.*--force.*master', "Force push to master branch"),
        # Destructive git operations
        (r'git\s+clean\s+-[a-zA-Z]*f[a-zA-Z]*d|git\s+clean\s+-[a-zA-Z]*d[a-zA-Z]*f', "git clean -fd removes untracked files and directories"),
        # File truncation
        (r'truncate\s+-s\s*0', "Truncating file to zero bytes"),
        # Reverse shells
        (r'nc\s+.*-e\s+/bin/', "Reverse shell via netcat"),
        (r'bash\s+-i\s+>&\s*/dev/tcp/', "Bash reverse shell"),
        (r'socat\s+.*exec:', "Reverse shell via socat"),
        (r'python[23]?\s+-c\s+.*socket.*connect', "Python reverse shell"),
        # Kernel modules
        (r'\bmodprobe\s+', "Loading kernel module"),
        (r'\binsmod\s+', "Inserting kernel module"),
        (r'\brmmod\s+', "Removing kernel module"),
        # Firewall manipulation
        (r'\biptables\s+', "Firewall rule modification"),
        (r'\bnft\s+', "Nftables rule modification"),
        (r'\bufw\s+(allow|deny|delete|reset)', "UFW firewall modification"),
        # Base64-to-shell pipes
        (r'base64\s+-d\s*\|\s*(ba)?sh', "Base64 decoded content piped to shell"),
        (r'base64\s+--decode\s*\|\s*(ba)?sh', "Base64 decoded content piped to shell"),
    ]
}

# =============================================================================
# RED: Denied with explanation (was "confirm" — now actually blocks)
# =============================================================================
CONFIRM_PATTERNS = {
    "bash": [
        (r'sudo\s+', "Elevated privileges requested"),
        (r'pacman\s+-Syu', "Full system upgrade"),
        (r'pacman\s+-Rns', "Package removal with dependencies"),
        (r'systemctl\s+(stop|disable|mask)', "Stopping/disabling system service"),
        (r'rm\s+-[rf]', "Recursive/force delete operation"),
        (r'git\s+push', "Pushing to remote repository"),
        (r'git\s+reset\s+--hard', "Hard reset — will lose changes"),
        (r'git\s+checkout\s+--\s+\.', "Discarding all local changes"),
        (r'pip\s+install.*--system', "System-wide pip install"),
        (r'npm\s+install\s+-g', "Global npm install"),
        (r'docker\s+system\s+prune', "Docker cleanup operation"),
        (r'docker\s+rm', "Docker container removal"),
        (r'reboot|shutdown|poweroff', "System power operation"),
        # Scheduled tasks
        (r'\bcrontab\s+', "Crontab modification"),
        (r'\bat\s+', "Scheduling job with at"),
        # Process killing
        (r'\bkill\s+', "Killing process"),
        (r'\bkillall\s+', "Killing all processes by name"),
        (r'\bpkill\s+', "Killing processes by pattern"),
        # Debugging/tracing
        (r'\bstrace\s+', "System call tracing"),
        (r'\bltrace\s+', "Library call tracing"),
    ],
    "file": [
        (r'\.env$', "Environment file modification"),
        (r'\.env\.', "Environment file modification"),
        (r'credentials', "Credentials file modification"),
        (r'secret', "Secrets file modification"),
        (r'password', "Password file modification"),
        (r'\.ssh/', "SSH configuration modification"),
        (r'/etc/', "System configuration modification"),
        (r'\.gnupg/', "GPG configuration modification"),
    ]
}

# =============================================================================
# YELLOW: Warn but proceed
# =============================================================================
WARN_PATTERNS = {
    "bash": [
        (r'chmod\s+777', "Overly permissive file permissions"),
        (r'chown\s+-R', "Recursive ownership change"),
        (r'find.*-exec.*rm', "Find with delete execution"),
        (r'xargs.*rm', "Piped delete operation"),
    ],
    "file": [
        (r'config', "Configuration file modification"),
        (r'\.json$', "JSON configuration modification"),
        (r'\.yaml$', "YAML configuration modification"),
        (r'\.yml$', "YAML configuration modification"),
    ]
}

# =============================================================================
# NETWORK SENSITIVE: Warn when network tools access sensitive paths
# =============================================================================
NETWORK_SENSITIVE_PATTERNS = [
    # Pattern: (network_cmd_regex, sensitive_path_regex, reason)
    (r'\b(curl|wget|http)\b', r'\.(env|pem|key|p12|pfx|jks)', "Network tool accessing sensitive file"),
    (r'\b(curl|wget)\b.*-d\s+@', r'\.', "Uploading file contents via network"),
    (r'\b(curl|wget)\b.*--data.*@', r'\.', "Uploading file contents via network"),
    (r'\b(curl|wget)\b', r'(credentials|secrets?|passwords?|tokens?|\.ssh/|\.gnupg/)', "Network tool referencing sensitive path"),
]

# =============================================================================
# Task agent dangerous instruction patterns
# =============================================================================
TASK_DANGEROUS_PATTERNS = [
    (r'rm\s+-rf', "Destructive delete in agent prompt"),
    (r'\bsudo\b', "Privilege escalation in agent prompt"),
    (r'curl.*\|\s*(ba)?sh', "Remote code execution in agent prompt"),
    (r'disable\s+guard', "Attempting to disable guardrails"),
    (r'bypass\s+check', "Attempting to bypass safety checks"),
    (r'ignore\s+safety', "Attempting to ignore safety measures"),
    (r'skip\s+guard', "Attempting to skip guardrails"),
    (r'turn\s+off\s+(guard|safe)', "Attempting to disable safety"),
]
