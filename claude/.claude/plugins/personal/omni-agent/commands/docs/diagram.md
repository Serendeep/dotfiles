---
description: Generate architecture diagrams from code
argument-hint: "[type: flow|sequence|class|erd|component|c4] [scope]"
allowed-tools: Read, Glob, Grep, Task
---

# Architecture Diagram Generator

Generate visual diagrams from codebase analysis.

**Arguments**: "$ARGUMENTS"

## Diagram Types

### flow
Flowchart showing process/logic flow

### sequence
Sequence diagram showing interactions over time

### class
Class diagram showing object structure

### erd
Entity-relationship diagram for database schema

### component
Component diagram showing system parts

### c4
C4 model diagram (context, container, component)

## Workflow

1. **Analyze Codebase**
   Based on diagram type:
   - `flow`: Analyze function logic
   - `sequence`: Find API calls, interactions
   - `class`: Parse class definitions
   - `erd`: Read database models
   - `component`: Map module dependencies

2. **Launch Architect**
   Use Task tool to spawn `architect` agent with:
   - Analysis results
   - Diagram type requested
   - Scope (files/modules)

3. **Generate Diagram**
   Output Mermaid or PlantUML code:
   ```mermaid
   [Diagram code]
   ```

## Output

- Mermaid code (can be rendered in markdown)
- PlantUML code (if requested)
- Explanation of components
- Suggestions for improvements
