#!/usr/bin/env bash
# Bootstrap a fresh Arch install from these dotfiles
#
# Usage: ./install.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
STOW_PACKAGES=(
  shell git hypr waybar walker terminals starship nvim
  omarchy-custom spicetify systemd-user scripts btop
  fastfetch cava mise
)

info()  { echo -e "\033[1;34m::\033[0m $*"; }
warn()  { echo -e "\033[1;33m::\033[0m $*"; }
ok()    { echo -e "\033[1;32m::\033[0m $*"; }
fail()  { echo -e "\033[1;31m::\033[0m $*"; exit 1; }

run() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# --- Prerequisites ---

command -v git >/dev/null || fail "git is required"

info "Checking for yay..."
if ! command -v yay >/dev/null; then
  info "Installing yay..."
  run bash -c '
    tmpdir=$(mktemp -d)
    git clone https://aur.archlinux.org/yay-bin.git "$tmpdir/yay-bin"
    cd "$tmpdir/yay-bin"
    makepkg -si --noconfirm
    rm -rf "$tmpdir"
  '
fi
ok "yay is available"

# --- Stow ---

info "Installing stow..."
run sudo pacman -S --needed --noconfirm stow
ok "stow installed"

# --- Packages ---

info "Installing explicit packages..."
if [[ -f "$DOTFILES_DIR/packages/explicit.txt" ]]; then
  run sudo pacman -S --needed --noconfirm - < "$DOTFILES_DIR/packages/explicit.txt" || warn "Some packages may have failed"
fi

info "Installing AUR packages..."
if [[ -f "$DOTFILES_DIR/packages/aur.txt" ]]; then
  run yay -S --needed --noconfirm - < "$DOTFILES_DIR/packages/aur.txt" || warn "Some AUR packages may have failed"
fi

info "Installing Flatpak apps..."
if [[ -f "$DOTFILES_DIR/packages/flatpak.txt" ]] && command -v flatpak >/dev/null; then
  while IFS= read -r app; do
    [[ -z "$app" ]] && continue
    run flatpak install -y flathub "$app" || warn "Failed to install $app"
  done < "$DOTFILES_DIR/packages/flatpak.txt"
fi

# --- Zinit ---

info "Checking zinit..."
ZINIT_HOME="$HOME/.local/share/zinit/zinit.git"
if [[ ! -d "$ZINIT_HOME" ]]; then
  info "Installing zinit..."
  run bash -c "
    mkdir -p \"\$(dirname $ZINIT_HOME)\"
    git clone https://github.com/zdharma-continuum/zinit.git \"$ZINIT_HOME\"
  "
fi
ok "zinit is available"

# --- Stow packages ---

info "Stowing dotfiles..."
cd "$DOTFILES_DIR"
for pkg in "${STOW_PACKAGES[@]}"; do
  if [[ -d "$pkg" ]]; then
    run stow --no-folding --adopt -t "$HOME" "$pkg" && ok "  $pkg" || warn "  $pkg failed"
  fi
done

# Restore sanitized gitconfig (--adopt overwrites it)
run git checkout -- git/.gitconfig 2>/dev/null || true

# --- Git hooks ---

info "Configuring git hooks..."
run git config core.hooksPath .githooks
ok "hooks configured"

# --- NVM ---

info "Checking nvm..."
export NVM_DIR="$HOME/.config/nvm"
if [[ ! -d "$NVM_DIR" ]]; then
  info "Installing nvm..."
  run bash -c 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash'
fi
ok "nvm is available"

# --- SDKMAN ---

info "Checking sdkman..."
if [[ ! -d "$HOME/.sdkman" ]]; then
  info "Installing sdkman..."
  run bash -c 'curl -s https://get.sdkman.io | bash'
fi
ok "sdkman is available"

# --- Systemd user services ---

info "Enabling systemd user services..."
run systemctl --user daemon-reload
run systemctl --user enable --now elephant.service || warn "elephant.service failed"
run systemctl --user enable --now omarchy-battery-monitor.timer || warn "battery-monitor timer failed"
ok "services enabled"

# --- Spicetify ---

info "Applying spicetify theme..."
if command -v spicetify >/dev/null; then
  run spicetify config current_theme TwilightHaven 2>/dev/null || true
  run spicetify apply 2>/dev/null || warn "spicetify apply failed (Spotify may need to be running)"
fi

ok "All done! Log out and back in for shell changes to take effect."
