---
description: Generate and validate blog topic ideas with trend research
argument-hint: "[niche: edge-ai|local-first|flutter|indie|career|oss] [--brainstorm|--validate <topic>]"
allowed-tools: WebSearch, Read, Write, Task, TodoWrite
---

# Blog Topic Generator

Generate research-backed blog topic ideas or validate a specific topic for blog.serendeep.tech.

**Arguments**: "$ARGUMENTS"

## Niches

### Primary (Deep Expertise)
- `edge-ai`: Edge AI, on-device inference, TinyML, quantization
- `local-first`: Local-first architecture, CRDTs, offline sync
- `flutter`: Flutter/Dart development, cross-platform mobile

### Adjacent (Broader Reach)
- `indie`: Indie hacking, bootstrapping, solo development
- `career`: Developer career, growth, sustainability
- `oss`: Open source contribution, maintenance, community

## Modes

### --brainstorm (default)
Generate 5-10 topic ideas with:
- Working title (demystification-style)
- Core thesis in one sentence
- Target audience
- Competitive landscape (existing coverage)
- Unique angle opportunity

### --validate <topic>
Validate a specific topic idea by:
- Searching for existing coverage
- Identifying gaps in current content
- Finding trending discussions
- Suggesting differentiation angles

## Workflow

1. **Parse Arguments**
   Determine niche and mode from "$ARGUMENTS"

2. **Research Phase**
   Use WebSearch to find:
   - Trending discussions (Reddit, HN, Twitter/X, dev.to)
   - Existing blog coverage on topic
   - Recent developments (last 6 months)
   - Pain points developers are expressing

3. **Analysis**
   - Map content gaps
   - Identify underserved angles
   - Check for saturation
   - Assess audience demand signals

4. **Generate Output**

   For brainstorm mode:
   ```markdown
   ## Topic Ideas for [Niche]

   ### 1. [Title in demystification style]
   **Thesis**: [One sentence core argument]
   **Audience**: [Who benefits most]
   **Existing Coverage**: [Brief landscape—what's already written]
   **Your Angle**: [What makes this different]
   **Demand Signals**: [Why now—evidence of interest]

   [Repeat for 5-10 ideas...]
   ```

   For validate mode:
   ```markdown
   ## Topic Validation: [Topic]

   ### Viability Score: [1-10]

   **Existing Coverage**
   - [Link 1]: [Brief summary]
   - [Link 2]: [Brief summary]

   **Gap Analysis**
   - What's missing: [...]
   - Your unique angle: [...]

   **Demand Signals**
   - [Evidence of interest]

   **Recommendation**
   [Go/No-Go with reasoning]
   ```

## Title Style Guide

Good titles promise demystification:
- "Demystifying [Topic]: What Actually Happens When..."
- "[Topic] Isn't Magic: A Practical Guide to..."
- "What No One Tells You About [Topic]"
- "[Topic] Without the Hype"
- "The Real Story Behind [Technology]"

## Example Usage

```
/omni-agent:blog-topic edge-ai --brainstorm
/omni-agent:blog-topic flutter --validate "Building offline-first Flutter apps with Drift"
/omni-agent:blog-topic indie
/omni-agent:blog-topic career --brainstorm
```
