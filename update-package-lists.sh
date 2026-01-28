#!/usr/bin/env bash
# Refresh package lists from the current system

set -euo pipefail
cd "$(dirname "$0")"

pacman -Qqe | grep -v "$(pacman -Qqm)" > packages/explicit.txt
pacman -Qqm > packages/aur.txt
flatpak list --app --columns=application 2>/dev/null > packages/flatpak.txt || true

echo "Updated:"
echo "  $(wc -l < packages/explicit.txt) explicit packages"
echo "  $(wc -l < packages/aur.txt) AUR packages"
echo "  $(wc -l < packages/flatpak.txt) flatpak apps"
