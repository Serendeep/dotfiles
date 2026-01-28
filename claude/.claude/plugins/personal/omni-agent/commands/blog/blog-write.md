---
description: Write a complete blog post draft from outline
argument-hint: "<topic-or-outline-file> [--section all|intro|body|conclusion] [--voice casual|formal]"
allowed-tools: Read, Write, WebSearch, Task, Glob, TodoWrite
---

# Blog Post Writer

Write a complete blog post draft following the established voice and style.

**Arguments**: "$ARGUMENTS"

## Options

### --section
- `all` (default): Write complete post
- `intro`: Hook + TL;DR only
- `body`: Main content sections
- `conclusion`: Closing reflection only

### --voice
- `casual` (default): Full conversational style with personality
- `formal`: Slightly more reserved, fewer em-dashes, suitable for external publications

## Workflow

1. **Load Context**
   - Read outline file if path provided
   - If topic string only, generate quick outline first
   - Load any associated research files from same directory

2. **Launch Content Writer Agent**
   Use Task tool to spawn `content-writer` agent with:
   - Outline structure
   - Research materials
   - Section scope
   - Voice setting

3. **Writing Process**
   Agent follows these steps:

   a. **Hook** (first)
     - Draft 2-3 opening variations
     - Select strongest rhetorical question approach
     - Example: "Have you ever [common experience] and wondered [deeper question]?"

   b. **TL;DR**
     - Summarize value in 2-3 sentences
     - Ensure it's genuinely useful to skimmers

   c. **Body Sections**
     - Follow outline structure
     - Apply code + explanation pattern (sandwich code with context)
     - Insert em-dashes for rhythm
     - Use we/you direct address throughout

   d. **Closing**
     - Connect to broader implications
     - End with reflection or provocation
     - Avoid summary repetition

4. **Quality Pass**
   - Check all code blocks have context
   - Verify voice consistency
   - Ensure parenthetical citations are in place
   - Confirm title promises are delivered

5. **Output**
   ```markdown
   ---
   title: "[Title]"
   date: [YYYY-MM-DD]
   tags: [tag1, tag2]
   description: "[Meta description for SEO - 150-160 chars]"
   draft: true
   ---

   [Complete blog post content]

   ---
   <!-- Writing Notes -->
   Word Count: [X]
   Reading Time: [Y min]
   Sources Cited: [N]
   Code Blocks: [M]
   ```

## Voice Examples

### Casual (default)
> "Have you ever stared at a loading spinner and wondered—genuinely wondered—why we keep building apps that break the moment you step into an elevator?"

### Formal
> "The assumption that applications require constant connectivity deserves scrutiny. What happens when we invert this expectation?"

## Example Usage

```
/omni-agent:blog-write ./outlines/flutter-offline.md
/omni-agent:blog-write "Edge AI deployment patterns" --section intro
/omni-agent:blog-write ./outlines/crdt-explainer.md --voice formal
```
