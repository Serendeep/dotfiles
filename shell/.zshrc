# Zsh interactive shell configuration

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Source omarchy defaults (aliases, functions)
source ~/.local/share/omarchy/default/bash/aliases
source ~/.local/share/omarchy/default/bash/functions

# Zinit initialization
source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"

# Essential plugins
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light Aloxaf/fzf-tab

# Load completions
autoload -Uz compinit && compinit
zinit cdreplay -q

# History settings
HISTSIZE=50000
SAVEHIST=50000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt SHARE_HISTORY
setopt EXTENDED_HISTORY
setopt INC_APPEND_HISTORY

# Key bindings (emacs style)
bindkey -e
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward
bindkey '^[[1;5C' forward-word
bindkey '^[[1;5D' backward-word
bindkey '^[[3~' delete-char

# Additional aliases
alias ls='eza --icons'
alias ll='eza -la --icons'
alias la='eza -a --icons'
alias lt='eza --tree --icons'
alias cat='bat'
alias grep='rg'

# NVM lazy loading (faster shell startup)
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" --no-use
alias node='unalias node npm npx 2>/dev/null; nvm use default >/dev/null; node'
alias npm='unalias node npm npx 2>/dev/null; nvm use default >/dev/null; npm'
alias npx='unalias node npm npx 2>/dev/null; nvm use default >/dev/null; npx'

# Zoxide (smart cd)
eval "$(zoxide init zsh)"
alias cd='z'
alias cdi='zi'

# Atuin shell history (magical search with Ctrl+R)
eval "$(atuin init zsh)"

# Starship prompt
eval "$(starship init zsh)"

# FZF integration
[ -f /usr/share/fzf/key-bindings.zsh ] && source /usr/share/fzf/key-bindings.zsh
[ -f /usr/share/fzf/completion.zsh ] && source /usr/share/fzf/completion.zsh

# Dart completions
[ -f ~/.config/.dart-cli-completion/zsh-config.zsh ] && source ~/.config/.dart-cli-completion/zsh-config.zsh

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
export PATH="$HOME/.local/bin:$PATH"
