---
description: Review a GitHub pull request
argument-hint: "[PR-number or PR-URL]"
allowed-tools: Bash, Read, Glob, Grep, Task
---

# Pull Request Review

Review a GitHub PR with comprehensive analysis.

**PR**: "$ARGUMENTS"

## Workflow

1. **Fetch PR Information**
   ```bash
   gh pr view [number] --json title,body,files,additions,deletions,commits
   gh pr diff [number]
   ```

2. **Analyze PR Context**
   - Read PR description and linked issues
   - Understand the purpose of changes
   - Check for breaking changes

3. **Launch Review Agents**
   Use Task tool to spawn:
   - `code-reviewer`: Code quality analysis
   - `security-analyst`: Security review

4. **Check PR Metadata**
   - Commit message quality
   - Test coverage indication
   - Documentation updates

5. **Generate Review**
   Structured review suitable for GitHub PR comment

## Output Format

```markdown
## PR Review: #[number] - [title]

### Summary
[Brief overview of the changes]

### Review

#### Code Quality
[Findings]

#### Security
[Findings]

#### Suggestions
[Improvements]

### Verdict
- [ ] **Approve**: Ready to merge
- [ ] **Request Changes**: Issues must be addressed
- [ ] **Comment**: Feedback only

---
*Reviewed by omni-agent*
```

## Integration

Can post review directly to GitHub with:
```bash
gh pr review [number] --comment --body "[review content]"
```
