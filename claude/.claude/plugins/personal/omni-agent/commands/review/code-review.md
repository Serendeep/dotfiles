---
description: Comprehensive code review with security analysis and improvement suggestions
argument-hint: "[staged|commit|branch|HEAD~N|file-path]"
allowed-tools: Bash, Read, Glob, Grep, Task
---

# Code Review

Perform thorough CodeRabbit-style code review with multi-dimensional analysis.

**Scope**: "$ARGUMENTS" (default: staged changes)

## Workflow

1. **Determine Scope**
   - `staged` or empty: `git diff --staged`
   - `commit`: `git diff HEAD~1`
   - `branch`: `git diff main...HEAD`
   - `HEAD~N`: Last N commits
   - Path: Review specific files

2. **Get the Diff**
   ```bash
   git diff [appropriate flags based on scope]
   ```

3. **Launch Review Agents**
   Use Task tool to spawn in parallel:
   - `code-reviewer`: General code quality, patterns, maintainability
   - `security-analyst`: Security vulnerabilities, OWASP checks

4. **Aggregate Results**
   - Combine findings from both agents
   - Deduplicate overlapping issues
   - Prioritize by severity

5. **Generate Report**
   Present structured review with:
   - Critical issues (must fix)
   - Important issues (should fix)
   - Suggestions (consider)
   - Positive observations

## Output Format

```markdown
# Code Review: [Scope Description]

**Files Changed**: X | **Lines**: +Y/-Z
**Risk Level**: Low/Medium/High/Critical

## Critical Issues (N)
[Details with file:line references and fix suggestions]

## Important Issues (N)
[Details]

## Suggestions (N)
[Details]

## Positive Observations
[What's done well]

## Recommendation
- [ ] Approve
- [ ] Request Changes
- [ ] Needs Discussion
```
