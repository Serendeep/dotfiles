---
description: Generate LaTeX document templates
argument-hint: "[type: article|report|thesis|presentation|cv|letter]"
allowed-tools: Read, Write, Task
---

# LaTeX Template Generator

Generate complete, ready-to-use LaTeX document templates.

**Type**: "$ARGUMENTS"

## Available Templates

### article
Basic academic article with sections, abstract, bibliography

### report
Technical report with chapters, table of contents, appendices

### thesis
Full thesis template with front matter, chapters, bibliography

### presentation
Beamer presentation with modern theme

### cv
Professional CV/resume template

### letter
Formal letter template

## Workflow

1. **Launch LaTeX Expert**
   Use Task tool to spawn `latex-expert` agent with template request

2. **Generate Template**
   - Complete preamble with essential packages
   - Proper document structure
   - Placeholder content
   - Comments explaining customization

3. **Write File**
   Save template to specified location or display

## Output

- Complete, compilable LaTeX document
- All required packages listed
- Clear comments for customization
- Compilation instructions
