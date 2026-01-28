# dotfiles

My Arch Linux + Hyprland setup, managed with [GNU Stow](https://www.gnu.org/software/stow/). Running on an ASUS ROG laptop.

Built on top of [omarchy](https://omarchy.com/) -- a Hyprland-based desktop environment that handles the base config, theming, and window management defaults. Everything here is my customization layer on top of that.

## What's here

- **Hyprland** window manager config (workspace rules, scratchpads, custom keybindings)
- **Waybar** with custom modules (Spotify, Docker, git branch, pomodoro timer, cava visualizer, network speed)
- **Neovim** via LazyVim with all colorscheme plugins eager-loaded for hot-reloading
- **Four custom omarchy themes** (twilight-haven, aether, monokai-dark, nes) with matching wallpaper sets
- **Spicetify** with a TwilightHaven Spotify theme
- **13 custom scripts** in `~/.local/bin` -- scratchpad manager, project switcher, waybar modules, etc.
- **Three terminal configs** (Ghostty, Alacritty, Kitty) all using Starship prompt
- Shell setup with zsh + zinit, zoxide, atuin, fzf, eza, bat, ripgrep
- Package lists auto-refreshed on every commit via a pre-commit hook

## Key bindings

These are my additions on top of omarchy's defaults. Omarchy handles the standard stuff (window tiling, workspaces, screenshots, clipboard, app launcher).

| Keys | What it does |
|---|---|
| `Super + Return` | Terminal (in current directory) |
| `Super + Shift + B` | Browser |
| `Super + Shift + N` | Editor (neovim) |
| `Super + Shift + M` | Spotify |
| `Super + Shift + T` | btop |
| `Super + Shift + D` | lazydocker |
| `Super + Shift + O` | Obsidian |
| `Super + Shift + /` | 1Password |
| `` Super + ` `` | Terminal scratchpad |
| `Super + M` | Monitor scratchpad (btop) |
| `Super + ;` | Music scratchpad (Spotify) |
| `Super + Alt + P` | Pomodoro toggle |
| `Super + Alt + N` | Quick capture note |
| `Super + Alt + B` | Quick build |
| `Super + Ctrl + P` | Project switcher |

Web apps (Super+Shift + letter): A = ChatGPT, C = Calendar, E = Email, Y = YouTube, X = Twitter, P = Google Photos.

## Structure

Each top-level directory is a stow package. Stow creates symlinks from your home directory into the repo, so editing `~/.zshrc` actually edits `~/.dotfiles/shell/.zshrc`.

```
shell/           .zshrc, .bashrc, .bash_profile, .zprofile
git/             .gitconfig (sanitized -- no safe dirs or credential store)
hypr/            Hyprland config (11 .conf files)
waybar/          config.jsonc + style.css
walker/          app launcher config
terminals/       alacritty, kitty, ghostty
starship/        prompt config
nvim/            full LazyVim setup (theme.lua excluded -- managed by omarchy)
omarchy-custom/  custom themes, wallpapers, branding, hooks
spicetify/       Spotify theming
systemd-user/    elephant.service, battery monitor
scripts/         13 custom scripts in ~/.local/bin
btop/            system monitor config
fastfetch/       system info display
cava/            audio visualizer
mise/            dev tool version manager
packages/        pacman + AUR + flatpak package lists
```

## Prerequisites

- Arch Linux (this isn't going to work on Ubuntu)
- [omarchy](https://omarchy.com/) installed
- `git` and an internet connection

Everything else gets installed by the script.

## Install

```bash
git clone https://github.com/Serendeep/dotfiles ~/.dotfiles
cd ~/.dotfiles
./install.sh
```

There's also `./install.sh --dry-run` if you want to see what it would do first.

The script handles: yay, stow, all packages from the saved lists, zinit, nvm, sdkman, systemd services, and spicetify theming. It uses `--needed` everywhere so it's safe to re-run.

## Things to know

**Omarchy manages some files.** Mako notifications config and the neovim `theme.lua` are symlinks controlled by omarchy's theme system. They're not in this repo on purpose -- changing themes through omarchy would just overwrite them.

**The gitconfig is sanitized.** I stripped out `[safe]` directory entries (machine-specific paths) and the `credential helper = store` line. The GitHub credential helper via `gh auth` is kept since that's the intended auth method.

**Stow uses `--no-folding`.** This means stow symlinks individual files, not entire directories. That way omarchy and other tools can still create new files in directories like `~/.config/hypr/` without conflicts.

**Package lists update automatically.** The pre-commit hook runs `update-package-lists.sh` before each commit, so the lists in `packages/` are always current. You can also run it manually.

## Updating package lists

```bash
cd ~/.dotfiles
./update-package-lists.sh
```

Or just commit anything -- the pre-commit hook does it for you.
