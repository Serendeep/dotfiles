---
description: Get help with pacman package management
argument-hint: "[operation: install|remove|search|update|clean|query]"
allowed-tools: Bash, Task, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Pacman Help

Guide for Arch Linux package management with pacman and AUR helpers.

**Operation**: "$ARGUMENTS"

## Operations

### install [package]
How to install packages from official repos or AUR

### remove [package]
Safely remove packages with dependency handling

### search [query]
Search for packages in repos and AUR

### update
System update guidance and best practices

### clean
Clean package cache and orphans

### query
Query installed packages, files, dependencies

## Workflow

1. **Parse Operation**
   Determine what pacman help is needed

2. **Fetch Current Documentation**
   Use Context7 MCP for latest pacman documentation

3. **Launch Arch Specialist**
   If complex operation, spawn `arch-specialist` agent

4. **Provide Guidance**
   - Exact commands to run
   - Explanation of flags
   - Common pitfalls to avoid
   - Safety considerations

## Quick Reference

```bash
# Install
sudo pacman -S package       # From repos
paru -S package              # From AUR

# Remove
sudo pacman -Rs package      # With unused deps
sudo pacman -Rns package     # With deps and configs

# Update
sudo pacman -Syu             # Full system upgrade

# Search
pacman -Ss query             # Search repos
paru -Ss query               # Search repos + AUR

# Query
pacman -Qi package           # Info on installed
pacman -Ql package           # List files
pacman -Qo /path/to/file     # Which package owns
```
