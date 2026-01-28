# omni-agent

A comprehensive Claude Code plugin with multiple specialized capabilities and strict safety guardrails.

## Features

### Core Skills
- **Project Management**: Sprint planning, task tracking, milestone management
- **Code Review**: CodeRabbit-style reviews with security analysis (OWASP Top 10)
- **LaTeX Expert**: Academic writing, mathematical typesetting, bibliography management
- **Arch Linux Specialist**: System troubleshooting with Context7 documentation
- **Prompt Engineering**: Delegates to Lyra for optimization

### Additional Skills
- **Git Workflow Expert**: Rebasing, cherry-picking, conflict resolution
- **Testing Strategy Advisor**: Coverage analysis, test case generation
- **API Documentation Generator**: OpenAPI/Swagger spec creation
- **Architecture Diagrammer**: Mermaid/PlantUML diagram generation

### Safety Features
- **Strict Guardrails**: Blocks dangerous commands (rm -rf /, fork bombs)
- **Confirmation Required**: For sudo, system upgrades, deletions
- **Rollback Tracking**: Operation history for recovery
- **Warnings**: For potentially risky operations

## Commands

### Project Management
- `/omni-agent:sprint-plan [name]` - Plan a sprint
- `/omni-agent:task-track [action]` - Track tasks
- `/omni-agent:milestone [action]` - Manage milestones

### Code Review
- `/omni-agent:code-review [scope]` - Comprehensive review
- `/omni-agent:security-scan [scope]` - Security-focused analysis
- `/omni-agent:pr-review [number]` - Review a PR

### LaTeX
- `/omni-agent:latex-paper [template] [section]` - Write papers
- `/omni-agent:latex-math [equation]` - Typeset math
- `/omni-agent:latex-template [type]` - Generate templates

### Arch Linux
- `/omni-agent:arch-troubleshoot [issue]` - Diagnose issues
- `/omni-agent:pacman-help [operation]` - Package management help
- `/omni-agent:system-health [mode]` - Health check

### Git
- `/omni-agent:git-workflow [operation]` - Advanced git ops
- `/omni-agent:conflict-resolve [file]` - Resolve conflicts

### Testing
- `/omni-agent:test-strategy [path]` - Analyze testing needs
- `/omni-agent:coverage-analyze [command]` - Coverage report

### Documentation
- `/omni-agent:api-docs [path]` - Generate API docs
- `/omni-agent:diagram [type]` - Create diagrams

### Guardrails
- `/omni-agent:guardrails-configure [action]` - View guardrails
- `/omni-agent:rollback [action]` - Rollback operations

## Agents

The plugin includes 10 specialized agents:
1. `project-manager` - Sprint and task management
2. `code-reviewer` - Comprehensive code review
3. `security-analyst` - Security-focused review
4. `latex-expert` - LaTeX and academic writing
5. `arch-specialist` - Arch Linux administration
6. `git-expert` - Advanced git operations
7. `test-advisor` - Testing strategy
8. `api-documenter` - API documentation
9. `architect` - System diagrams
10. `rollback-advisor` - Recovery operations

## Guardrails

### Blocked (CRITICAL)
- `rm -rf /` - Recursive delete from root
- `dd if=... of=/dev/` - Direct disk write
- Fork bombs
- Piping remote content to shell
- Force push to main/master

### Requires Confirmation (RED)
- `sudo` commands
- `pacman -Syu` (system upgrade)
- Package removal
- Git push operations
- File deletions
- Credential file modifications

### Warnings (YELLOW)
- `chmod 777`
- Configuration changes
- Recursive ownership changes

## Installation

The plugin is installed in your personal marketplace at:
`~/.claude/plugins/personal/omni-agent/`

It is enabled in `~/.claude/settings.json`.

## License

MIT
