---
description: Typeset complex mathematical equations in LaTeX
argument-hint: "[equation description or formula to typeset]"
allowed-tools: Read, Write, Task
---

# Mathematical Typesetting

Convert mathematical expressions to proper LaTeX notation.

**Input**: "$ARGUMENTS"

## Capabilities

- Complex equations and formulas
- Aligned multi-line equations
- Matrices and arrays
- Theorem environments
- Custom operators
- Symbol lookup

## Workflow

1. **Understand the Math**
   Parse the user's description or informal notation

2. **Launch LaTeX Expert**
   Use Task tool to spawn `latex-expert` agent focused on:
   - Mathematical typesetting
   - Proper notation conventions
   - Required packages

3. **Generate LaTeX**
   - Proper environment (equation, align, gather)
   - Correct symbols and operators
   - Good formatting and spacing

## Example Inputs

- "integral from 0 to infinity of e^(-x^2)"
- "3x3 matrix with elements a_ij"
- "piecewise function f(x) = 0 if x<0, 1 otherwise"
- "sum from i=1 to n of x_i squared"

## Output Format

```latex
% Required packages
\usepackage{amsmath}

% The equation
\begin{equation}
  [LaTeX code]
\end{equation}
```
