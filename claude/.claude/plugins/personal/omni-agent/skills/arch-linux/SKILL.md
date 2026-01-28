# Arch Linux Skill

Reference materials for Arch Linux system administration and troubleshooting.

## Package Management

### Pacman Quick Reference

```bash
# Sync & Update
pacman -Syu          # Full system upgrade (ALWAYS do first)
pacman -Syyu         # Force refresh + upgrade

# Install
pacman -S pkg        # Install package
pacman -U file.pkg   # Install local package

# Remove
pacman -R pkg        # Remove package only
pacman -Rs pkg       # Remove + orphaned deps
pacman -Rns pkg      # Remove + deps + configs

# Search
pacman -Ss query     # Search repos
pacman -Qs query     # Search installed
pacman -Si pkg       # Info from repos
pacman -Qi pkg       # Info installed

# Query
pacman -Ql pkg       # List files in package
pacman -Qo file      # Find owning package
pacman -Qdt          # List orphans
pacman -Qe           # Explicitly installed
pacman -Qm           # Foreign packages (AUR)

# Maintenance
pacman -Sc           # Clear old cache
pacman -Scc          # Clear all cache
paccache -r          # Keep last 3 versions
```

### AUR Helpers

```bash
# Install paru (recommended)
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si

# Paru usage (same as pacman)
paru -S pkg          # Install (repos + AUR)
paru -Sua            # Update AUR only
paru -Gc pkg         # Show AUR comments
```

## System Maintenance

### Regular Tasks

```bash
# Weekly
sudo pacman -Syu           # System update
paru -Sua                  # AUR updates
sudo paccache -r           # Clean cache

# Monthly
sudo journalctl --vacuum-time=2weeks
systemctl --failed
pacdiff                    # Handle .pacnew
```

### Handling .pacnew Files

```bash
# Find all
find /etc -name "*.pacnew" 2>/dev/null

# Interactive merge
sudo pacdiff

# Manual diff
diff /etc/file.conf /etc/file.conf.pacnew
```

## Systemd Service Management

```bash
# Control
systemctl start|stop|restart service
systemctl enable|disable service
systemctl status service

# Query
systemctl --failed              # Failed services
systemctl list-units --type=service

# Logs
journalctl -xeu service         # Service logs
journalctl -b                   # Current boot
journalctl -b -1                # Previous boot
journalctl -p err               # Errors only

# User services
systemctl --user enable service
```

## Common Issues

### Boot Recovery

```bash
# From live USB
mount /dev/nvme0n1p2 /mnt       # Root
mount /dev/nvme0n1p1 /mnt/boot  # EFI
arch-chroot /mnt

# Regenerate initramfs
mkinitcpio -P

# Reinstall bootloader (systemd-boot)
bootctl install

# Reinstall bootloader (GRUB)
grub-install --target=x86_64-efi --efi-directory=/boot
grub-mkconfig -o /boot/grub/grub.cfg
```

### Key/Database Issues

```bash
# Keyring issues
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --refresh-keys

# Database lock
sudo rm /var/lib/pacman/db.lck
```

### Graphics Drivers

```bash
# AMD
sudo pacman -S mesa vulkan-radeon libva-mesa-driver

# NVIDIA
sudo pacman -S nvidia nvidia-settings nvidia-utils

# Intel
sudo pacman -S mesa vulkan-intel intel-media-driver
```

### Network

```bash
# Check status
ip link
networkctl status

# Restart NetworkManager
sudo systemctl restart NetworkManager

# DNS
resolvectl status
```

### Audio (PipeWire)

```bash
# Install
sudo pacman -S pipewire pipewire-pulse pipewire-alsa wireplumber
systemctl --user enable pipewire pipewire-pulse wireplumber

# Check
wpctl status
pactl info
```

## Safety Rules

1. **ALWAYS** run `pacman -Syu` before installing
2. **NEVER** do partial upgrades (`pacman -Sy pkg`)
3. **CHECK** https://archlinux.org/news/ before updates
4. **BACKUP** before major changes
5. **HAVE** a live USB ready for recovery

## Useful Paths

| Path | Purpose |
|------|---------|
| `/etc/pacman.conf` | Pacman config |
| `/etc/pacman.d/mirrorlist` | Mirror list |
| `/var/cache/pacman/pkg/` | Package cache |
| `/var/log/pacman.log` | Pacman history |
| `/etc/mkinitcpio.conf` | Initramfs config |
| `/boot/loader/` | systemd-boot config |
