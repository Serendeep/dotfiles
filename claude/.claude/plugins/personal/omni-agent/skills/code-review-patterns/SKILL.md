# Code Review Patterns Skill

This skill provides reference materials for comprehensive code review.

## OWASP Top 10 (2021) Quick Reference

| Rank | Vulnerability | Key Checks |
|------|--------------|------------|
| A01 | Broken Access Control | Missing auth checks, IDOR, CORS misconfig |
| A02 | Cryptographic Failures | Hardcoded secrets, weak algorithms, HTTP |
| A03 | Injection | SQL, XSS, command, LDAP injection |
| A04 | Insecure Design | Missing threat modeling, rate limiting |
| A05 | Security Misconfiguration | Debug mode, default creds, verbose errors |
| A06 | Vulnerable Components | Outdated deps, known CVEs |
| A07 | Authentication Failures | Weak passwords, missing MFA |
| A08 | Data Integrity Failures | Unsigned updates, insecure deserialization |
| A09 | Logging Failures | Missing audits, log injection, PII in logs |
| A10 | SSRF | Unvalidated URLs, internal network access |

## Common Vulnerability Patterns

### SQL Injection
```python
# BAD
query = f"SELECT * FROM users WHERE id = {user_input}"

# GOOD
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_input,))
```

### XSS (Cross-Site Scripting)
```javascript
// BAD
element.innerHTML = userInput;

// GOOD
element.textContent = userInput;
// Or use DOMPurify for HTML
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Command Injection
```python
# BAD
os.system(f"echo {user_input}")

# GOOD
subprocess.run(["echo", user_input], shell=False)
```

## Code Quality Metrics

### Complexity Thresholds
- Cyclomatic Complexity: Flag > 10
- Cognitive Complexity: Flag > 15
- Function Length: Flag > 50 lines
- File Length: Flag > 500 lines
- Nesting Depth: Flag > 4 levels

### Clean Code Principles
1. **Single Responsibility**: One reason to change
2. **DRY**: Don't Repeat Yourself
3. **KISS**: Keep It Simple
4. **YAGNI**: You Ain't Gonna Need It
5. **Fail Fast**: Validate early

## Review Checklist

### Security
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] Output encoding for XSS
- [ ] Parameterized queries
- [ ] Proper authentication
- [ ] Authorization checks
- [ ] Secure communications (HTTPS)
- [ ] Sensitive data protected

### Code Quality
- [ ] Clear naming conventions
- [ ] No code duplication
- [ ] Proper error handling
- [ ] Adequate test coverage
- [ ] Documentation for public APIs
- [ ] No dead code
- [ ] Consistent formatting

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Efficient algorithms
- [ ] Resource cleanup
- [ ] Pagination for large datasets

## Supply Chain Attack Patterns

### Dependency Confusion
- Verify private packages are scoped (`@org/pkg` for npm, namespace for PyPI)
- Check for `--extra-index-url` in pip config (allows public registry fallback)
- Ensure package names don't collide with public registry names

### Typosquatting Detection

| Technique | Legitimate | Typosquat Example |
|-----------|-----------|-------------------|
| Character swap | `requests` | `reqeusts` |
| Homoglyph | `crypto` | `crypt0` |
| Hyphen/underscore | `python-dateutil` | `python_dateutil` |
| Scope confusion | `@angular/core` | `angular-core` |
| Plural/singular | `lodash` | `lodashs` |
| Prefix addition | `colors` | `node-colors` |

### Lockfile Integrity
- [ ] Lockfiles committed to repository
- [ ] No unexpected registry URL changes in lockfile
- [ ] Integrity hashes present and consistent
- [ ] Lockfile changes correspond to manifest changes

### Install Script Red Flags
```regex
# npm preinstall/postinstall hooks (check package.json)
"(pre|post)install":\s*"[^"]*"

# Python setup.py arbitrary execution
class\s+\w+Install.*cmdclass

# Cargo build scripts
build\s*=\s*"build\.rs"
```

**What to flag:**
- Any postinstall script that runs network requests
- Setup.py with `cmdclass` overrides
- Build scripts that download external resources

## Container Security Checklist

### Dockerfile Audit
- [ ] Base image pinned by digest (`FROM image@sha256:...`)
- [ ] Non-root user specified (`USER nonroot`)
- [ ] No secrets in ENV or ARG instructions
- [ ] `.dockerignore` excludes sensitive files
- [ ] Multi-stage build used (minimize final image)
- [ ] Package versions pinned in install commands
- [ ] No `COPY . .` without `.dockerignore`
- [ ] HEALTHCHECK instruction present

### Docker Compose Audit
- [ ] No `privileged: true`
- [ ] No `network_mode: host` (unless required)
- [ ] No full filesystem mounts (`volumes: /:/host`)
- [ ] No `cap_add: ALL`
- [ ] No `pid: host`
- [ ] Secrets use Docker secrets or env_file (not inline)
- [ ] Read-only root filesystem where possible (`read_only: true`)

## Cloud Security Patterns

### IAM Policy Audit
- [ ] No `Action: "*"` (wildcard actions)
- [ ] No `Resource: "*"` (wildcard resources)
- [ ] Follows least privilege principle
- [ ] Conditions restrict access scope (IP, time, MFA)
- [ ] No inline policies on users (use groups/roles)

### Storage Security
- [ ] No public-read or public-read-write ACLs
- [ ] Server-side encryption enabled
- [ ] Bucket policies restrict access
- [ ] Versioning enabled for critical data
- [ ] Access logging enabled

### Metadata Endpoint Protection
Cloud metadata endpoints to watch for (SSRF vectors):
- AWS: `169.254.169.254`, `fd00:ec2::254`
- GCP: `metadata.google.internal`
- Azure: `169.254.169.254` (with `Metadata: true` header)

Ensure user-controlled URLs cannot reach these endpoints.

## CI/CD Pipeline Security

### Pipeline Audit Checklist
- [ ] Secrets stored in CI platform's secret store (not in code)
- [ ] Branch protection rules enforce review
- [ ] Pipeline runs with minimal permissions
- [ ] Third-party actions/orbs are version-pinned
- [ ] Artifact integrity verified (checksums/signatures)
- [ ] No secrets printed in logs

### GitHub Actions Pinning
```yaml
# BAD - mutable tag
- uses: actions/checkout@v4

# GOOD - pinned to commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

### Pipeline Secrets Hygiene
```yaml
# BAD - secret in environment
env:
  API_KEY: ${{ secrets.API_KEY }}
run: echo $API_KEY  # Leaks to logs

# GOOD - pass as input, mask in logs
run: |
  echo "::add-mask::${{ secrets.API_KEY }}"
  ./deploy.sh
env:
  API_KEY: ${{ secrets.API_KEY }}
```
