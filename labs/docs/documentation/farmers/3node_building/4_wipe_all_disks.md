---
title: "4. Wipe All the Disks"
sidebar_position: 177
---



## Introduction

In this section, we explain how to wipe all the disks of your 3Node.



## Main Steps

It only takes a few steps to wipe all the disks of a 3Node.

1. Create a Linux bootstrap image
2. Boot Linux in *Try Mode*
3. Wipe All the Disks

ThreeFold runs its own OS, which is Zero-OS. You thus need to start with completely wiped disks. Note that ALL disks must be wiped. Otherwise, Zero-OS won't boot.

An easy method is to download a Linux distribution and wipe the disks by running simple commands on the command-line interface.

We will show how to do this with Ubuntu 24.04. LTS. This distribution is easy to use and it is thus a good introduction to Linux, in case you haven't yet explored this great operating system.


## 1. Create a Linux Bootstrap Image

[Download the Ubuntu 24.04 ISO file](https://releases.ubuntu.com/24.04/) and burn the ISO image on a USB key. Make sure you have enough space on your USB key. You can also use other Linux Distro such as [GRML](https://grml.org/download/), if you want a lighter ISO image.

The process is the same as in section [Burning the Bootstrap Image](./bootstrap_image#balenaetcher-mac-linux-windows), but with the Linux ISO instead of the Zero-OS bootstrap image. [BalenaEtcher](https://www.balena.io/etcher/) is recommended as it formats your USB in the process, and it is available for MAC, Windows and Linux.


## 2. Boot Linux in *Try Mode*

When you boot the Linux ISO image, make sure to choose *Try Mode*. Otherwise, it will install Linux on your computer. You do not want this.

If you are using GRML, simply boot the USB key with the GRML bootstrap image, select GRML then press `q` to enter the shell mode. Once this is done, the next steps are similar to the Ubuntu method: you will use `lsblk` and `wipefs` commands to identify and wipe the disks.

## 3. Wipe All the Disks

We will now remove the partition table and every filesystem signature from the disks. This is what Zero-OS needs in order to boot and claim the disks.

> **Important:** This destroys all data on the disks. Make sure you have no important data on your disks, or that you have copies of it, before proceeding.

Once Linux is booted, open the terminal.

### 3.1 Identify Your Disks

First, list the disks:

```
lsblk -o NAME,SIZE,TYPE,TRAN,FSTYPE,MOUNTPOINTS
```

The types of disk you can see are:

- `sdX`
  - SATA type
  - e.g. `sda`
  - Note: It can be an SSD disk or a USB key
- `nvmeXnY`
  - NVMe type
  - e.g. `nvme0n1`

**Before going further, find the USB key you are currently running from.** It is the disk that shows `/cdrom`, `/rofs` or `/run/live/medium` in the `MOUNTPOINTS` column, and it usually shows `usb` in the `TRAN` column. Never wipe that disk: you are booted from it.

You can also ask Linux directly which disk you booted from:

```
lsblk -no PKNAME "$(findmnt -no SOURCE /cdrom 2>/dev/null || findmnt -no SOURCE /run/live/medium 2>/dev/null)"
```

### 3.2 Wipe One Disk at a Time

This is the recommended method: you name one disk explicitly, so there is no risk of wiping the wrong one.

Set the disk you want to wipe, then run the block below as is. Replace `/dev/sda` with your disk (e.g. `/dev/nvme0n1`).

```
DISK=/dev/sda
PARTS=$(lsblk -lnpo NAME "$DISK" | tail -n +2)

# 1. Release the disk (a busy disk cannot be wiped)
[ -n "$PARTS" ] && sudo swapoff $PARTS 2>/dev/null
[ -n "$PARTS" ] && sudo umount  $PARTS 2>/dev/null
sudo mdadm --stop --scan 2>/dev/null
sudo vgchange -an        2>/dev/null

# 2. Wipe it
[ -n "$PARTS" ] && sudo wipefs -af $PARTS
sudo sgdisk --zap-all "$DISK"
sudo wipefs -af "$DISK"

# 3. Make the kernel re-read the disk
sudo partprobe "$DISK"
sudo udevadm settle
```

Each part matters:

- **Release the disk.** Ubuntu's *Try Mode* automatically mounts partitions it finds and can activate swap on them. A disk that is mounted, in use as swap, or held by a software RAID array or an LVM volume group cannot be wiped. This is the single most common reason a wipe appears to do nothing.
- **`wipefs` on the partitions, then the disk.** Wiping only the disk leaves the filesystem signatures that live inside each partition. Those can reappear later.
- **`sgdisk --zap-all`** removes both the primary GPT header at the start of the disk and the backup GPT header at the end, plus the MBR.
- **`partprobe` and `udevadm settle`** make the kernel re-read the disk, so the verification below shows the real state rather than a cached one.

> If you get `sgdisk: command not found`, install it with `sudo apt update && sudo apt install -y gdisk`, then run the block again.

Repeat this for every disk in the machine, then verify each one.

### 3.3 Verify the Disk Is Wiped

Do not skip this step. A wipe can fail without printing an obvious error.

```
lsblk -o NAME,SIZE,TYPE,FSTYPE,PTTYPE,MOUNTPOINTS "$DISK"
sudo wipefs -n "$DISK"
sudo fdisk -l "$DISK"
```

The disk is properly wiped when **all three** of these are true:

- `lsblk` shows only the disk itself, with **no partition lines** underneath it, and the `FSTYPE` and `PTTYPE` columns are empty.
- `sudo wipefs -n "$DISK"` prints **nothing at all**. This command only reports signatures, it does not change anything. Any line it prints is a signature still on the disk.
- `sudo fdisk -l "$DISK"` shows the disk size but reports no partition table and lists no partitions.

If any signature is still reported, run the wipe block from section 3.2 again, then check the [Troubleshooting](#35-troubleshooting) section below.

### 3.4 Wipe All Disks at Once

Once you are comfortable with the steps above, you can wipe every disk in one go. This method detects the USB key you booted from and skips it.

**First, do a dry run.** This only prints what would happen and changes nothing:

```
LIVE=$(lsblk -no PKNAME "$(findmnt -no SOURCE /cdrom 2>/dev/null || findmnt -no SOURCE /run/live/medium 2>/dev/null)" 2>/dev/null)
echo "Live USB detected as: ${LIVE:-NONE}"

for d in $(lsblk -dno NAME,TYPE | awk '$2=="disk" && $1 !~ /^(zram|loop|ram)/ {print $1}'); do
  if [ "$d" = "$LIVE" ]; then echo "  SKIP  /dev/$d  (this is your Linux USB)"
  else                        echo "  WIPE  /dev/$d"; fi
done
```

Read that list carefully. Every disk marked `WIPE` will be erased, and your Linux USB must be marked `SKIP`.

If `Live USB detected as: NONE` is printed, the detection failed. **Do not run the next block** — wipe the disks one at a time using section 3.2 instead.

If the list is correct, run the wipe:

```
if [ -z "$LIVE" ]; then
  echo "Live USB not detected. Use the one-disk-at-a-time method instead."
else
  # Release any software RAID array or LVM volume group first,
  # otherwise the disks they hold are busy and cannot be wiped.
  sudo mdadm --stop --scan 2>/dev/null
  sudo vgchange -an        2>/dev/null

  for d in $(lsblk -dno NAME,TYPE | awk '$2=="disk" && $1 !~ /^(zram|loop|ram)/ {print $1}'); do
    [ "$d" = "$LIVE" ] && continue
    DISK=/dev/$d
    echo "=== Wiping $DISK ==="
    PARTS=$(lsblk -lnpo NAME "$DISK" | tail -n +2)
    [ -n "$PARTS" ] && sudo swapoff $PARTS 2>/dev/null
    [ -n "$PARTS" ] && sudo umount  $PARTS 2>/dev/null
    [ -n "$PARTS" ] && sudo wipefs -af $PARTS
    sudo sgdisk --zap-all "$DISK"
    sudo wipefs -af "$DISK"
    sudo partprobe "$DISK"
  done
  sudo udevadm settle
fi
```

Then verify every disk:

```
for d in $(lsblk -dno NAME,TYPE | awk '$2=="disk" && $1 !~ /^(zram|loop|ram)/ {print $1}'); do
  echo "=== /dev/$d ==="
  sudo wipefs -n "/dev/$d"
done
```

Every disk except your Linux USB must print nothing.

### 3.5 Troubleshooting

**`Device or resource busy`, or the wipe seems to do nothing.**

Something is still holding the disk. Find out what:

```
cat /proc/mdstat          # software RAID arrays
sudo dmsetup ls           # LVM / device-mapper
sudo swapon --show        # active swap
lsblk -o NAME,MOUNTPOINTS # anything still mounted
```

Then stop it (`sudo mdadm --stop --scan`, `sudo vgchange -an`, `sudo swapoff -a`, `sudo umount ...`) and wipe again.

**`sgdisk: command not found`.**

Install it: `sudo apt update && sudo apt install -y gdisk`.

**The disk still shows partitions after wiping.**

The kernel has not re-read the partition table. Run `sudo partprobe "$DISK"` and `sudo udevadm settle`. If it persists, reboot into *Try Mode* again and re-check with `sudo wipefs -n "$DISK"`.

**The disks do not appear at all in `lsblk`.**

The machine likely has a hardware RAID controller presenting the disks as a RAID volume instead of individual disks. Zero-OS needs direct access to each disk. Set the controller to HBA / IT mode, or replace it. See the [farming troubleshooting section](../farming_troubleshooting/farming_troubleshooting_tips) of the manual for more on RAID controllers.

**Zero-OS still refuses to boot after wiping.**

Make sure you wiped *every* disk in the machine, not just the one you intend to use, and verify each with `sudo wipefs -n`. More build and post-build troubleshooting is available in the [farming troubleshooting section](../farming_troubleshooting/farming_troubleshooting_tips) of the manual.
