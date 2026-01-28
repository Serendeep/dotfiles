---
description: Create a structured outline for a blog post
argument-hint: "<topic> [--format tutorial|opinion|explainer] [--research-file path]"
allowed-tools: Read, Write, WebSearch, Task, Glob, TodoWrite
---

# Blog Outline Generator

Create a detailed outline for a blog post with structural guidance.

**Arguments**: "$ARGUMENTS"

## Formats

### --format tutorial
How-to structure with code blocks planned:
- Hook -> TL;DR -> Context -> Prerequisites -> Steps -> Gotchas -> Reflection

### --format opinion
Thought leadership structure:
- Hook -> Thesis -> Evidence -> Counterarguments -> Synthesis -> CTA

### --format explainer (default)
Deep dive structure:
- Hook -> TL;DR -> Foundation -> Layers -> Implications -> Further Reading

## Workflow

1. **Gather Context**
   - Read research file if provided via --research-file
   - Quick WebSearch for additional context if needed
   - Check for prior related content in workspace

2. **Launch Content Writer**
   Use Task tool to spawn `content-writer` agent with:
   - Topic and format
   - Research materials
   - Request for structured outline

3. **Generate Outline**
   ```markdown
   # [Working Title - demystification style]

   **Format**: [tutorial|opinion|explainer]
   **Target Length**: [word count estimate]
   **Target Audience**: [who]

   ## Outline

   ### 1. Hook (100-150 words)
   - Opening question/observation: [specific suggestion]
   - Problem framing: [what tension to establish]

   ### 2. TL;DR (50-75 words)
   - Core value prop: [what reader gets]
   - Key takeaway: [one sentence]

   ### 3. [Section Name] (X words)
   - Point A
     - Supporting detail
     - [CODE BLOCK: description of what to show]
   - Point B

   [Continue for all sections...]

   ### N. Closing Reflection (100-150 words)
   - Broader implication: [theme]
   - Provocative question: [what to leave them with]

   ## Code Blocks Planned
   1. [File:line] — [What it demonstrates]
   2. [File:line] — [What it demonstrates]

   ## Sources to Cite
   - [Source 1 for Point X]
   - [Source 2 for Point Y]
   ```

4. **Validate Structure**
   Ensure outline follows content-writer agent's quality checklist:
   - Rhetorical question opening
   - Useful TL;DR
   - Code sandwich pattern planned
   - Philosophical closing

## Example Usage

```
/omni-agent:blog-outline "Building offline-first Flutter apps" --format tutorial
/omni-agent:blog-outline "Why local-first is the future" --format opinion --research-file ./research/local-first.md
/omni-agent:blog-outline "Understanding CRDTs" --format explainer
```
