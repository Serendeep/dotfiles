# LaTeX Typesetting Skill

Reference materials for LaTeX document creation and mathematical typesetting.

## Document Classes

| Class | Use Case | Key Features |
|-------|----------|--------------|
| `article` | Papers, short docs | Sections, no chapters |
| `report` | Technical reports | Chapters, title page |
| `book` | Books, theses | Chapters, front/back matter |
| `beamer` | Presentations | Slides, themes |
| `IEEEtran` | IEEE papers | Two-column, IEEE style |
| `acmart` | ACM papers | ACM formatting |

## Essential Packages

```latex
% Always useful
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{cleveref}

% Tables
\usepackage{booktabs}  % Professional tables
\usepackage{tabularx}  % Auto-width columns

% Code
\usepackage{listings}  % Basic
\usepackage{minted}    % Syntax highlighting

% Bibliography
\usepackage[backend=biber]{biblatex}
```

## Math Quick Reference

### Environments
```latex
% Numbered equation
\begin{equation}
  E = mc^2
\end{equation}

% Aligned equations
\begin{align}
  a &= b + c \\
  d &= e + f
\end{align}

% Unnumbered
\begin{equation*}
  x = y
\end{equation*}
```

### Common Symbols
| Symbol | LaTeX | Symbol | LaTeX |
|--------|-------|--------|-------|
| α | `\alpha` | ∞ | `\infty` |
| β | `\beta` | ∑ | `\sum` |
| γ | `\gamma` | ∏ | `\prod` |
| δ | `\delta` | ∫ | `\int` |
| ε | `\epsilon` | ∂ | `\partial` |
| θ | `\theta` | ∇ | `\nabla` |
| λ | `\lambda` | × | `\times` |
| μ | `\mu` | ÷ | `\div` |
| π | `\pi` | ± | `\pm` |
| σ | `\sigma` | ≤ | `\leq` |
| φ | `\phi` | ≥ | `\geq` |
| ω | `\omega` | ≠ | `\neq` |

### Structures
```latex
% Fractions
\frac{a}{b}  \dfrac{a}{b}  \tfrac{a}{b}

% Roots
\sqrt{x}  \sqrt[n]{x}

% Matrices
\begin{pmatrix} a & b \\ c & d \end{pmatrix}
\begin{bmatrix} a & b \\ c & d \end{bmatrix}

% Cases
f(x) = \begin{cases}
  0 & \text{if } x < 0 \\
  1 & \text{otherwise}
\end{cases}

% Limits
\lim_{x \to \infty} f(x)

% Sums and products
\sum_{i=1}^{n} x_i
\prod_{j=1}^{m} y_j
```

## Bibliography (BibLaTeX)

### Setup
```latex
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{references.bib}

% In document
\cite{key}
\textcite{key}
\parencite{key}

% At end
\printbibliography
```

### BibTeX Entry
```bibtex
@article{smith2024,
  author  = {Smith, John and Doe, Jane},
  title   = {Title of Paper},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  pages   = {1--20},
  doi     = {10.1234/example}
}
```

## Best Practices

1. Use `\[...\]` not `$$...$$` for display math
2. Use `\text{}` for words in math mode
3. Define custom commands for repetition
4. Use `siunitx` for units: `\SI{10}{\meter}`
5. Label everything: `\label{eq:main}`
6. Use `cleveref`: `\cref{eq:main}` → "Equation 1"

## Compilation

```bash
# Standard
pdflatex document.tex
biber document
pdflatex document.tex
pdflatex document.tex

# Automated
latexmk -pdf document.tex
```
