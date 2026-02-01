---
title: "Web Gateway - Hetzner"
sidebar_position: 2
---

# Web Gateway on Hetzner Cloud

## Overview
This guide explains how to deploy a ThreeFold Zero-OS (ZOS) gateway inside a Hetzner Cloud VM. While this setup isn't recommended for general workloads or ThreeFold VMs, it's useful for gateway deployments due to Hetzner's reliable infrastructure and good bandwidth availability.

## Prerequisites
- Hetzner Cloud account with completed KYC and payment method
- Created Hetzner project
- SSH key (optional but recommended)
- Basic Linux command line knowledge

## Hardware Requirements
- Minimum 4GB RAM
- 100GB SSD storage
- Public IPv4 address

## Step 1: Create Hetzner Cloud VM

1. Log into Hetzner Cloud Console
2. Create a new server with these specifications:
   - Location: Choose your preferred datacenter
   - OS Image: Any (will be overwritten)
   - Server Type: CPX21 (4GB RAM) or higher
   - Storage: 
     - Primary disk: 80GB (default)
     - Additional volume: 100GB
   - Networking:
     - Enable Public IPv4
     - IPv6 optional
   - File system: Any (will be overwritten)

## Step 2: Boot into Rescue Mode

1. Select the server in Hetzner Console
2. Click "Rescue" tab
3. Enable rescue mode and power cycle
4. Connect via SSH:
```bash
ssh root@<your-server-ip>
```

## Step 3: Prepare Boot Image

1. Clone the ThreeFold IPXE fork:
```bash
git clone https://github.com/threefoldtech/ipxe.git
```

2. Install required package:
```bash
apt install liblzma-dev
```

3. Build IPXE:
```bash
cd ipxe/src
make
```

## Step 4: Generate Boot Script

1. Visit https://bootstrap.grid.tf
2. Enter Expert Mode
3. Configure:
   - Farm ID: Your farm ID
   - Network: mainnet
   - Extra kernel arguments: `version=v3light`
   - Kernel: `zos-v3light-generic`
   - Format: IPXE Boot Script
4. Generate IPXE boot script
5. Copy the generated URL and preprend  `https://bootstrap.grid.tf`

## Step 5: Create Boot Image

1. Download the boot script using the generated URL from above:
```bash
wget <bootstrap-url> -O zos.ipxe
```

2. Create USB boot image:
```bash
make bin/ipxe.usb EMBED=zos.ipxe
```

## Step 6: Write Boot Image to Disk

1. Wipe the disks on the server (e.g. with `sdb`)
```bash
wipefs -af /dev/sdb
```

2. Write the boot image:
```bash
dd if=bin/ipxe.usb of=/dev/sda
```

3. Reboot

```bash
reboot
```

You can then go to the Hetzner console and see the Z-OS image loading. On this page, you can see the gateway IP address:

```
net0/ip
net0/dns
net0/gateway
```

## Next Step

Then you can follow the steps in the manual to properly set your public configuration and DNS.

- [Set Up the Public Config](../../../dashboard/farms/your_farms)
- [Set Up a Gateway Domain](../gateway_domain.md)
