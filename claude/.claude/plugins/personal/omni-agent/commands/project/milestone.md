---
description: Define and track project milestones
argument-hint: "[create|update|list|progress] [milestone-name]"
allowed-tools: Read, Write, Glob, TodoWrite
---

# Milestone Management

Define project milestones with measurable goals and track progress.

**Action**: "$ARGUMENTS"

## Actions

### create [name]
Create a new milestone. Will prompt for:
- Target date
- Success criteria
- Related tasks/sprints
- Dependencies

### update [name]
Update milestone details or progress

### list
Show all milestones with status

### progress [name]
Show detailed progress for a specific milestone

## Milestone Structure

```markdown
## Milestone: [Name]
**Target**: YYYY-MM-DD
**Status**: Not Started | In Progress | At Risk | Completed

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Progress
- Tasks Completed: X/Y
- Story Points Done: X/Y
- Blocking Issues: N

### Risks
- Risk 1: [Description]
```

## Integration

- Milestones can span multiple sprints
- Progress is calculated from linked tasks
- Alerts when milestone is at risk
