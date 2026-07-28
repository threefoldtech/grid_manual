---
title: "Zero-OS Advantages"
sidebar_position: 356
---

## Introduction

We present the many advantages of Zero-OS.

## Zero-OS Installation

The Zero-OS is delivered to the 3Nodes over the internet network (network boot) and does not need to be installed.

### 3Node Install

1. Acquire a computer (server).
2. Configure a farm on the TFGrid explorer.
3. Download the bootloader and put on a USB stick or configure a network boot device.
4. Power on the computer and connect to the internet.
5. Boot! The computer will automatically download the components of the operating system (Zero-OS).

The actual bootloader is very small. It brings up the network interface of your computer and queries TFGeid for the remainder of the boot files needed.

The operating system is not installed on any local storage medium (hard disk, ssd). Zero-OS is stateless.

The mechanism to allow this to work in a safe and efficient manner is a ThreeFold innovation called our container virtual filesystem. 



## Unbreakable Storage

- Unlimited history
- Survives network, datacenter or node breakdown
- No silent corruption possible
- Quantum safe (data cannot be decrypted by quantum computers) as long as quantum computer has no access to the metadata
- Self-healing & autocorrecting


If you deploy a container with simple disk access, you don’t have it. 
Performance is around 50MB/second, if a bit more CPU is given for the distributed storage encoder, we achieve this performance. 


## Zero Hacking Surface

Zero does not mean is not possible but we use this term to specificy that we minized the attack surface for hackers.

- There is no shell/server interface on zero-os level (our operating system)
- There are no hidden or unintended processes running which are not prevalidatedOne comment: still ssh server running with keys of a few people on each server, not yet disabled. To be disabled in the near future, now still useful to debug but it is a backdoor. The creation of a new primitive where the farmer agrees to give access to administrators under analysis. This way, when a reservation is sent to a node, a ssh server is booted up with chosen key to allow admins to go in. 

## Zero Boot

> Zero Boot = Zero-OS boot process

ZOS Boot is a boot facility that allows 3nodes to boot from network boot servers located in the TF Grid.  This boot mechanism creates as little as possible operational and administration overhead.  ZOS Boot is a crucial part for enabling autonomy by *not* having the operating system installed on local disks on 3nodes.  With a boot network facility and no local operating system files you immediate erase a number of operational and administration tasks:

- to install the operating system to start with
- to keep track of which systems run which version of the operating system (especially in large setups this is a complicated and error prone task)
- to keep track of patches and bug fixes that have been applied to systems

That's just the administration and operational part of maintaining a server estate with local installed operating system.  On the security side of things the benefits are even greater:
- many hacking activities are geared towards adding to or changing parts of the operating system files.  This is a threat from local physical access to servers as well as over the network.  When there are no local operating system files installed this threat does not exist.
- accidental overwrite, delete or corruption of operating system files.  Servers run many processes and many of these processes have administrative access to be able to do what they need to do.  Accidental deletion or overwrites of crucial files on disk will make the server fail a reboot.
- access control.  I there is no local operating system installed access control, user rights etc etc. are unnecessary functions and features and do not have to be implemented.

### How

In this image from fs, a small partition is mounted in memory to start booting the machine, it gets IPXE (downloads what it needs), and then 0-OS boots. 
After that, going to the hub, downloading different lists. 

There is 1 main flist that triggers downloads of multiple flists.
In there all the components/daemons that do part of the 0-OS. 
Also the download of the zos-bins, i.e. external binaries are triggered this way (https://hub.grid.tf/tf-zos-bins). 

The core components of zero-os can be found in: [Zero-OS repo](https://github.com/threefoldtech/zos/tree/master/bins/packages) =  If something changes in the directory, a workflow is triggered to rebuild the full flist and push it to the hub. 
    
When a node discovers there is a new version of one of these lists on the hub, it downloads it, restarts the daemon with the new version. 
Over the lifetime of the node, it keeps pulling on the hub directories to check whether new daemons/flists/binaries are available and whether things need get upgraded.

### Features

The features of ZOS Boot are:

- no local operating system installed
- network boot from the grid to get on the grid
- decreased administrative and operational work, allowing for autonomous operations
- increased security
- increased efficiency (deduplication, only one version of the OS stored for thousands of servers)
- all server storage space is available for enduser workloads (average operating system size around 10GB)
- bootloader is less than 1MB in size and can be presented to the servers as a PXE script, USB boot device, ISO boot image.

    
## Deterministic Deployment

- flists concept (deduped vfilesystem, no install, ...)
    
The Dedupe filesystem flist uses fuse = interface which allows you to create the file system interface in user space, it is a virtual filesystem. 
Metadata is exposed. The system sees the full tree of the image, but data itself not there, data is downloaded whenever they are accessed.
     
There are multiple ways to create an flist: 
   - Convert an existing docker image which is hosted on the docker hub
   - Push an archive like a tjz on the hub
   - A library and CLI tool exist to build the flist from scratch: doing it this way, the directory is locally populated, and the flist is then created from the CLI tool. 
   - A [GitHub action](https://github.com/threefoldtech/zos_flist_publish) allows to build a flist directly from GitHub action, useful for developers on GitHub 

Be aware that the flist system works a bit differently than the usual deployment of containers (dockers), which doesn't do mounting of volumes from your local disk into container for configuration. 
With flists you need to modify your image to get configuration from environment. This is basically how docker was originally intended to be used. 

  - Smart contract for IT
    The smart contract for IT concept is applicable to any workload: containers, VMs, all gateways primitives, volumes, kubernetes and network.
    It is a static agreement between farmer and user about deployment of an IT workload. 
      
  - no dynamic behavior for deployment at runtime
    
  - no process can start unless the files are 100% described on flist level
  
## Zero-OS Protect

- The operating system of the 3node (Zero-OS) is made to exist in environments without the presence of technical knowhow. 3nodes are made to exist everywhere where network meet a power socket. The OS does not have a login shell and does not allow people to log in with physical access to a keyboard and screen nor does it allows logins over the network. There is no way the 3node accepts user initiated login attempts.
- For certified capacity a group of known strategic vendors are able to lock the [BIOS](https://en.wikipedia.org/wiki/BIOS) of their server range and make sure no-one but them can unlock and change features present in the BIOS. Some vendors have an even higher degree of security and can store private keys in chips in side the computer to provider unique identification based on private keys or have mechanisms to check wether the server has been opened / tampered with in the transportation from the factory / vendor to the Farmer. All of this leads to maximum protection on the hardware level.
- 3nodes boot from a network facility. This means that they do not have local installed operating system files. Also they do not have a local username / password file or database. Viruses and hackers have very little work with if there are no local files to plant viruses or trojan horses in. Also the boot facility provides hashes for the files sent to the booting 3node so that the 3node can check wether is receives the intended file, no more man in the middle attacks.
- The zos_fs provides the same hash and file check mechanism. Every application file presented to a booting container has a hash describing it and the 3node on which the container is booting can verify if the received file matches the previously received hash.
- Every deployment of one or more applications starts with the creation of a (private) [znet](./network_toc/znet.md). This private overlay network is single tenant and not connected to the public internet. Every application or service that is started in a container in this overlay network is connection to all of the other containers via a point to point, encrypted network connection.