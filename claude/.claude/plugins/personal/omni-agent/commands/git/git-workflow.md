---
description: Advanced git operations guidance (rebase, cherry-pick, bisect)
argument-hint: "[operation: rebase|cherry-pick|bisect|stash|branch] [args]"
allowed-tools: Bash, Task
---

# Git Workflow Helper

Guidance for advanced git operations with safety checks.

**Operation**: "$ARGUMENTS"

## Operations

### rebase [target-branch]
Interactive rebase guidance with:
- Squash/fixup recommendations
- Conflict resolution help
- Recovery instructions

### cherry-pick [commit(s)]
Cherry-pick commits with:
- Range support (A..B)
- Conflict handling
- No-commit option

### bisect [good-commit]
Binary search for bugs:
- Start bisect session
- Guide through marking
- Automate with scripts

### stash [push|pop|list|apply]
Stash management:
- Save with message
- Apply without removing
- Branch from stash

### branch [strategy]
Branch strategy recommendations:
- GitFlow
- Trunk-based
- GitHub Flow

## Workflow

1. **Parse Operation**
   Determine git operation needed

2. **Check Current State**
   ```bash
   git status
   git log --oneline -5
   ```

3. **Launch Git Expert**
   Use Task tool to spawn `git-expert` agent with:
   - Current state
   - Requested operation
   - Any arguments

4. **Provide Guidance**
   - Step-by-step commands
   - Explanation of each step
   - Recovery/rollback instructions

## Safety

- Always shows current state before changes
- Provides rollback instructions
- Warns about rewriting shared history
