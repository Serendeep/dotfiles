---
description: Optimize prompts using Lyra (delegates to lyra plugin)
argument-hint: "[prompt-to-optimize]"
allowed-tools: Skill
---

# Prompt Optimization

Optimize prompts using the specialized Lyra plugin.

**Prompt**: "$ARGUMENTS"

## About

This command delegates to the existing Lyra plugin for prompt engineering and optimization. Lyra is a specialized prompt optimization tool that can:

- Improve prompt clarity and specificity
- Add structure for better responses
- Optimize for specific use cases
- Apply prompt engineering best practices

## Workflow

1. **Delegate to Lyra**
   Use Skill tool to invoke `lyra:lyra`:
   ```
   skill: "lyra:lyra"
   args: "[user's prompt]"
   ```

2. **Return Optimized Prompt**
   Display Lyra's optimization with explanations

## Why Delegate?

The Lyra plugin is a dedicated prompt engineering tool. Rather than duplicating its functionality, omni-agent integrates with it for prompt optimization needs while focusing on complementary capabilities like project management, code review, and system administration.

## Direct Usage

You can also invoke Lyra directly:
```
/lyra:lyra [your prompt]
```
