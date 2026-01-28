---
description: Create or enhance academic papers with proper LaTeX formatting
argument-hint: "[template: ieee|acm|springer|thesis] [section: abstract|intro|method|results|all]"
allowed-tools: Read, Write, Task, Glob
---

# Academic Paper Assistant

Create or improve academic papers with proper LaTeX formatting.

**Arguments**: "$ARGUMENTS"

## Templates

### ieee
IEEE conference/journal format with IEEEtran class

### acm
ACM publication format with acmart class

### springer
Springer LNCS format

### thesis
Thesis/dissertation format with report class

## Sections

- `abstract`: Write/improve abstract
- `intro`: Introduction section
- `method`: Methodology/approach
- `results`: Results and discussion
- `all`: Generate complete paper structure

## Workflow

1. **Parse Arguments**
   Determine template and section from input

2. **Launch LaTeX Expert**
   Use Task tool to spawn `latex-expert` agent with:
   - Template requirements
   - Section focus
   - Existing content (if editing)

3. **Generate Content**
   - Proper document class and packages
   - Semantic structure
   - BibLaTeX setup for citations

4. **Output**
   - Compilable LaTeX code
   - Required package list
   - Compilation instructions

## Example Usage

```
/omni-agent:latex-paper ieee intro
/omni-agent:latex-paper thesis method
/omni-agent:latex-paper acm all
```
