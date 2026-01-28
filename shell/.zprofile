# Zsh login shell - Environment variables

# Source omarchy environment
source ~/.local/share/omarchy/default/bash/envs

# XDG base directories
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"

# NVM
export NVM_DIR="$HOME/.config/nvm"

# Android SDK
export ANDROID_HOME="$HOME/Android"
export PATH="$ANDROID_HOME/flutter/bin:$PATH"
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"
export PATH="$ANDROID_HOME/platform-tools:$PATH"
export PATH="$ANDROID_HOME/emulator:$PATH"

# Dart/Flutter
export PATH="$PATH:$HOME/.pub-cache/bin"

# PNPM
export PNPM_HOME="$HOME/.local/share/pnpm"
[[ ":$PATH:" != *":$PNPM_HOME:"* ]] && export PATH="$PNPM_HOME:$PATH"

# Shorebird
export PATH="$HOME/.config/shorebird/bin:$PATH"

# Editor
export EDITOR=nvim
export VISUAL=nvim
