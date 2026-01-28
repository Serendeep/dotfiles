---
description: Create, update, or view project tasks
argument-hint: "[create|update|list|status] [task-details]"
allowed-tools: Read, Write, Glob, TodoWrite
---

# Task Tracking

Manage project tasks with status tracking and priority management.

**Action**: "$ARGUMENTS"

## Actions

### create [description]
Create a new task with the given description. Will prompt for:
- Priority (P0-P3)
- Story points estimate
- Dependencies
- Acceptance criteria

### update [task-id] [field] [value]
Update a task field. Fields: status, priority, estimate, assignee

### list [filter]
List tasks. Filters: all, todo, in_progress, blocked, done

### status
Show summary of all tasks by status

## Task Format

Tasks are stored in structured format and can be:
- Written to `.claude/project/tasks.json` for persistence
- Tracked in current session via TodoWrite

## Integration

- Works with `sprint-plan` command for sprint context
- Updates are reflected in sprint velocity calculations
