---
description: Diagnose and fix Arch Linux system issues
argument-hint: "[issue-description]"
allowed-tools: Bash, Read, Task, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Arch Linux Troubleshooting

Diagnose and resolve Arch Linux system problems using current documentation.

**Issue**: "$ARGUMENTS"

## Workflow

1. **Gather System Information**
   ```bash
   uname -r                              # Kernel version
   pacman -Q linux                       # Installed kernel
   journalctl -xb --no-pager | tail -50  # Recent boot logs
   systemctl --failed                    # Failed services
   ```

2. **Fetch Documentation**
   Use Context7 MCP to get current Arch Wiki docs:
   ```
   mcp__context7__resolve-library-id
   - libraryName: "archlinux"
   - query: "[issue description]"

   mcp__context7__query-docs
   - libraryId: [from above]
   - query: "[specific troubleshooting query]"
   ```

3. **Launch Arch Specialist**
   Use Task tool to spawn `arch-specialist` agent with:
   - System information gathered
   - Relevant documentation
   - User's issue description

4. **Present Solution**
   - Step-by-step resolution
   - Include safety warnings
   - Provide rollback instructions
   - Link to relevant Arch Wiki pages

## Safety

- Always suggests backups before major changes
- Warns about destructive operations
- Provides rollback procedures
- Never recommends partial upgrades
