---
description: Security-focused code analysis for vulnerabilities and compliance
argument-hint: "[scope: staged|commit|branch|path] [--owasp] [--secrets]"
allowed-tools: Bash, Read, Glob, Grep, Task
---

# Security Scan

Dedicated security analysis focusing on vulnerabilities, secrets, and compliance.

**Arguments**: "$ARGUMENTS"

## Scan Types

### Default Scan
Comprehensive security review including:
- OWASP Top 10 vulnerabilities
- Hardcoded secrets/credentials
- Authentication/authorization issues
- Input validation problems

### --owasp
Focus specifically on OWASP Top 10 categories

### --secrets
Focus on detecting exposed secrets:
- API keys
- Database credentials
- Private keys
- JWT secrets

## Workflow

1. **Determine Scope**
   Parse scope from arguments (default: entire codebase)

2. **Launch Security Analyst**
   Use Task tool to spawn `security-analyst` agent with:
   - Scope of files to analyze
   - Specific focus areas from flags

3. **Pattern Scanning**
   Use Grep for known vulnerability patterns:
   - SQL injection risks
   - XSS vulnerabilities
   - Command injection
   - Credential patterns

4. **Generate Report**
   SARIF-compatible output with:
   - Severity ratings (Critical/High/Medium/Low)
   - CWE references
   - Remediation guidance

## Output Format

```markdown
# Security Scan Report

**Scan Date**: YYYY-MM-DD HH:MM
**Scope**: [Description]
**Risk Score**: X/100

## Critical Findings (N)
[CVE-style reporting with fix guidance]

## High Findings (N)
...

## Compliance Checklist
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Parameterized queries used
...
```
