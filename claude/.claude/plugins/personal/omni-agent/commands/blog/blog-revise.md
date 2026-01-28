---
description: Revise and improve a blog post draft
argument-hint: "<draft-file> [--focus voice|structure|clarity|seo|all] [--feedback \"...\"]"
allowed-tools: Read, Write, WebSearch, Task, Glob, Grep, TodoWrite
---

# Blog Post Revision

Revise and improve a blog post draft with targeted feedback.

**Arguments**: "$ARGUMENTS"

## Focus Areas

### --focus voice
- Check conversational tone consistency
- Verify we/you direct address
- Assess em-dash usage and rhythm
- Ensure opening uses rhetorical question pattern
- Validate closing has reflection, not just summary

### --focus structure
- Verify TL;DR is genuinely useful
- Check progressive complexity flow
- Validate code + explanation pattern
- Assess section transitions
- Check heading hierarchy

### --focus clarity
- Identify jargon without explanation
- Find sentences that could be simpler
- Check paragraph length (aim for 3-4 sentences)
- Verify code blocks are properly introduced
- Remove hedging language ("somewhat", "fairly", "basically")

### --focus seo
- Optimize title for search (< 60 chars, keyword early)
- Check meta description (150-160 chars)
- Verify heading keywords
- Suggest internal/external links
- Check image alt text if applicable

### --focus all (default)
Run all revision passes in sequence

## Workflow

1. **Load Draft**
   Read the draft file from "$ARGUMENTS"

2. **Analysis Phase**
   For each focus area:
   - Identify issues against checklist
   - Categorize by severity
   - Prepare specific suggestions

3. **Launch Content Writer Agent**
   Use Task tool to spawn `content-writer` agent with:
   - Draft content
   - Focus areas
   - User feedback (if provided via --feedback)
   - Request for revision report

4. **Generate Revision Report**
   ```markdown
   # Revision Report: [Title]

   ## Summary
   - Overall quality: [1-10]
   - Primary issues: [list]
   - Revision effort: [light|moderate|heavy]

   ## Voice Analysis
   - [ ] Conversational tone: [pass/fail with notes]
   - [ ] Direct address (we/you): [pass/fail]
   - [ ] Em-dash rhythm: [pass/fail]
   - [ ] Opening hook: [pass/fail]
   - [ ] Closing reflection: [pass/fail]

   ## Structure Analysis
   - [ ] TL;DR utility: [pass/fail]
   - [ ] Progressive complexity: [pass/fail]
   - [ ] Code explanation pattern: [pass/fail]

   ## Specific Issues

   ### Issue 1: [Title]
   **Location**: Line X
   **Current**: "[problematic text]"
   **Suggested**: "[improved text]"
   **Reasoning**: [why this change]

   [Repeat for all issues...]

   ## Revised Draft
   [Full revised draft if changes are significant]
   ```

5. **Apply Revisions**
   Write revised version to same file or new file with `-revised` suffix

## Anti-Pattern Checklist

Remove or fix these if found:
- [ ] "In today's fast-paced world..." (generic opening)
- [ ] Passive voice ("It was discovered...")
- [ ] Hedging ("Some might argue...")
- [ ] Code without context
- [ ] Conclusion that repeats intro
- [ ] "Simply" or "just" (dismissive)
- [ ] "Basically" or "essentially" (filler)

## Example Usage

```
/omni-agent:blog-revise ./drafts/flutter-offline.md
/omni-agent:blog-revise ./drafts/crdt-post.md --focus voice
/omni-agent:blog-revise ./drafts/edge-ai.md --feedback "Needs more code examples in section 3"
/omni-agent:blog-revise ./drafts/career-post.md --focus seo
```
