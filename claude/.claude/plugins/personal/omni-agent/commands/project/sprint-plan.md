---
description: Plan a new sprint with tasks, estimates, and dependencies
argument-hint: "[sprint-name or feature-focus]"
allowed-tools: Read, Write, Glob, Grep, Task, TodoWrite
---

# Sprint Planning

Create or update a sprint plan based on project context and user requirements.

**Input**: "$ARGUMENTS"

## Workflow

1. **Gather Context**
   - Read CLAUDE.md, README.md, or project docs for context
   - Check `.claude/project/` for existing tasks and sprints
   - Review recent git commits for velocity estimation if available

2. **Launch Project Manager Agent**
   - Use Task tool to spawn `project-manager` agent
   - Provide gathered context and user's sprint focus
   - Request structured sprint plan with story point estimates

3. **Create Artifacts**
   - Write sprint plan to project directory
   - Create TodoWrite items for immediate session tracking
   - Identify dependencies and blockers

4. **Present Summary**
   - Display sprint goal and committed tasks
   - Show total story points and capacity
   - Highlight any risks or blockers

## Output Requirements

- Sprint should follow INVEST criteria
- Tasks should have clear acceptance criteria
- Story point estimates using Fibonacci (1, 2, 3, 5, 8)
- Flag any tasks > 8 points for splitting
