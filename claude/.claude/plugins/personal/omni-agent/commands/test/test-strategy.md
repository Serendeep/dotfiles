---
description: Analyze code and suggest testing strategy
argument-hint: "[path-to-analyze] or [--coverage-report]"
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Testing Strategy Advisor

Analyze code and recommend testing approach.

**Target**: "$ARGUMENTS"

## Analysis Types

### Code Analysis (default)
Analyze code structure and suggest tests:
- Identify testable units
- Recommend test types
- Generate test case suggestions

### --coverage-report
Analyze existing coverage and identify gaps

## Workflow

1. **Analyze Target**
   - Read source files
   - Identify functions/classes
   - Map dependencies

2. **Check Existing Tests**
   ```bash
   # Find test files
   find . -name "*test*" -o -name "*spec*"
   ```

3. **Launch Test Advisor**
   Use Task tool to spawn `test-advisor` agent with:
   - Source code structure
   - Existing test coverage
   - Framework in use

4. **Generate Recommendations**
   - Test cases by priority
   - Coverage improvement suggestions
   - Framework-specific patterns

## Output

```markdown
## Test Strategy: [Target]

### Current State
- Test Files: N
- Estimated Coverage: X%

### Gap Analysis
[Areas lacking tests]

### Recommended Test Cases
[Prioritized list with code examples]
```
