---
description: Run tests and analyze coverage
argument-hint: "[test-command] or [--report path/to/coverage]"
allowed-tools: Bash, Read, Task
---

# Coverage Analysis

Run tests with coverage and analyze results.

**Arguments**: "$ARGUMENTS"

## Workflow

1. **Detect Test Framework**
   Look for:
   - `package.json` (Jest, Vitest)
   - `pytest.ini`, `pyproject.toml` (pytest)
   - `Cargo.toml` (cargo test)
   - `go.mod` (go test)

2. **Run Tests with Coverage**
   Framework-specific commands:
   ```bash
   # JavaScript (Jest)
   npm test -- --coverage

   # Python (pytest)
   pytest --cov=src --cov-report=html

   # Go
   go test -cover ./...

   # Rust
   cargo tarpaulin
   ```

3. **Analyze Results**
   Launch `test-advisor` agent with coverage data

4. **Report**
   - Overall coverage percentage
   - Per-file breakdown
   - Uncovered lines/branches
   - Priority areas for new tests

## Output

```markdown
## Coverage Report

### Summary
- Line Coverage: X%
- Branch Coverage: X%
- Function Coverage: X%

### By File
| File | Lines | Branches | Uncovered |
|------|-------|----------|-----------|

### Priority Gaps
1. [File/function needing tests]
2. ...
```
