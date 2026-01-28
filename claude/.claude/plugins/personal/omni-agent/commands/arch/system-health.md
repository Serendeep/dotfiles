---
description: Check Arch Linux system health and maintenance status
argument-hint: "[--full|--quick]"
allowed-tools: Bash, Task
---

# System Health Check

Comprehensive Arch Linux system health assessment.

**Mode**: "$ARGUMENTS" (default: quick)

## Quick Check

Fast assessment of critical items:
- Failed systemd services
- Pending .pacnew files
- Orphan packages
- Disk space

## Full Check

Comprehensive analysis:
- All quick check items
- Package integrity verification
- Journal errors
- Boot time analysis
- Security audit

## Workflow

1. **Run Health Checks**
   ```bash
   # Failed services
   systemctl --failed

   # Pacnew files
   find /etc -name "*.pacnew" 2>/dev/null

   # Orphan packages
   pacman -Qdt

   # Disk space
   df -h /

   # For full check:
   # Package integrity
   pacman -Qk 2>/dev/null | grep -v "0 missing"

   # Journal errors
   journalctl -p err -b --no-pager | tail -20
   ```

2. **Analyze Results**
   Launch `arch-specialist` if issues found

3. **Generate Report**
   ```markdown
   # System Health Report

   **Status**: Healthy | Needs Attention | Critical

   ## Services
   - Failed: N

   ## Packages
   - Orphans: N
   - Pacnew pending: N

   ## Disk
   - / usage: X%

   ## Recommendations
   - [Action items]
   ```

## Scheduled Maintenance

Recommend running:
- Quick check: Weekly
- Full check: Monthly
