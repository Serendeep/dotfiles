---
description: Deep research for a specific blog topic with source evaluation
argument-hint: "<topic-or-title> [--depth shallow|deep] [--output file-path]"
allowed-tools: WebSearch, Read, Write, Task, Glob, TodoWrite
---

# Blog Topic Research

Conduct comprehensive research for a blog post topic.

**Arguments**: "$ARGUMENTS"

## Research Depth

### --depth shallow (default)
Quick research pass (~10 searches):
- Top 5 existing articles on topic
- Key statistics and claims to cite
- Common misconceptions to address
- 2-3 expert voices to reference

### --depth deep
Comprehensive research (~25 searches):
- All shallow research plus:
- Academic/technical papers
- GitHub repos and real implementations
- Conference talks and podcasts
- Historical context and evolution
- Contrary viewpoints

## Workflow

1. **Parse Topic**
   Extract key concepts and search terms from "$ARGUMENTS"

2. **Search Strategy**
   Execute searches in categories:
   - `[topic] tutorial 2024 2025`
   - `[topic] best practices`
   - `[topic] problems challenges`
   - `[topic] vs alternatives`
   - `[topic] real world example`
   - `[topic] site:github.com`
   - `[topic] site:arxiv.org` (for deep)

3. **Source Evaluation**
   For each source:
   - Assess authority (author credentials, publication)
   - Check recency (prefer < 12 months for tech)
   - Extract key claims and data points
   - Note quotable passages

4. **Synthesis**
   - Identify consensus views
   - Find contrarian perspectives
   - Map the debate landscape
   - Extract citation-worthy facts

5. **Output**
   ```markdown
   # Research Brief: [Topic]

   ## Key Takeaways
   - [3-5 main findings]

   ## Core Sources
   | Source | Authority | Key Insight |
   |--------|-----------|-------------|
   | [Link] | [Rating]  | [Insight]   |

   ## Statistics & Data Points
   - [Fact 1] (Source: [link])
   - [Fact 2] (Source: [link])

   ## Expert Quotes
   > "[Quote]" — [Name, Title]

   ## Common Misconceptions
   - Misconception: [X]
   - Reality: [Y]

   ## Gaps & Opportunities
   - [What's not covered well]

   ## Suggested Citations
   - [Parenthetical citation format ready to use]
   ```

6. **Save Output**
   If --output specified, write to file path
   Otherwise display in response

## Example Usage

```
/omni-agent:blog-research "ONNX Runtime on mobile devices"
/omni-agent:blog-research "CRDTs for local-first apps" --depth deep
/omni-agent:blog-research "Flutter state management 2024" --output ./research/flutter-state.md
```
