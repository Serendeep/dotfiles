---
description: Help resolve git merge conflicts
argument-hint: "[file-path] or [--all]"
allowed-tools: Bash, Read, Edit, Task
---

# Conflict Resolution Helper

Guide through resolving git merge/rebase conflicts.

**Target**: "$ARGUMENTS"

## Workflow

1. **Identify Conflicts**
   ```bash
   git diff --name-only --diff-filter=U
   ```

2. **Analyze Conflict**
   For each conflicted file:
   - Read the file to understand conflicts
   - Show ours vs theirs differences
   - Identify the nature of conflict

3. **Launch Git Expert**
   Use Task tool to spawn `git-expert` agent with:
   - Conflicted files
   - Conflict content
   - Context of the merge/rebase

4. **Guide Resolution**
   - Explain each conflict
   - Suggest resolution strategy:
     - Accept ours
     - Accept theirs
     - Manual merge
   - Show resolved content

5. **Complete**
   ```bash
   git add [resolved-files]
   git commit  # or git rebase --continue
   ```

## Resolution Strategies

### Accept Ours
```bash
git checkout --ours <file>
```

### Accept Theirs
```bash
git checkout --theirs <file>
```

### Manual Merge
Edit file to combine changes appropriately

### Use Merge Tool
```bash
git mergetool
```
