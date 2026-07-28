---
title: "Build, Post Build & Memory"
sidebar_position: 204
---





## Introduction

We cover different ways and levels to troubleshoot farming issues.

## Build Troubleshooting

In this section, we cover notions such as how to wipe disks, how to set the BIOS configurations and more.

### Set the BIOS

You need to set the BIOS properly for your 3Node to boot with Zero-OS.

The basic information is available [here](../3node_building/set_bios_uefi#the-essential-features-of-biosuefi-for-a-3node).

### BIOS Troubleshooting

You might have to try UEFI first and if it doesn't work, try BIOS. Usually when this is the case (UEFI doesn't work with your current computer), the following message will be shown:

> Initializing Network Devices...

And then... nothing. This means that you are still in the BIOS of the hardware and boot is not even started yet. When this happens, try the BIOS mode of your computer. 

### When running wipefs to wipe my disks on Linux, I get a shell error, "Probing Initialized Failed", or the wipe appears to do nothing. Is there a fix?

Follow the procedure in [Wipe All the Disks](../3node_building/wipe_all_disks), which releases the disk before wiping it and then verifies the result. The most common causes are below, with the disk `sda` as an example.

* **The disk is busy.** Ubuntu's *Try Mode* automatically mounts partitions it finds and can activate swap on them. A disk that is mounted, in use as swap, or held by a software RAID array or an LVM volume group cannot be wiped. Release it first:
  * ```
    sudo swapoff /dev/sda1 && sudo umount /dev/sda1
    sudo mdadm --stop --scan
    sudo vgchange -an
    ```
  * To find what is still holding the disk: `cat /proc/mdstat`, `sudo dmsetup ls`, `sudo swapon --show`, `lsblk -o NAME,MOUNTPOINTS`
* **Only the disk was wiped, not its partitions.** Wipe the partition signatures first, then the disk itself:
  * ```
    sudo wipefs -af /dev/sda1 /dev/sda2
    sudo sgdisk --zap-all /dev/sda
    sudo wipefs -af /dev/sda
    ```
* **You are wiping your boot USB by accident.** Identify the disk you booted from before wiping anything:
  * ```
    lsblk -no PKNAME "$(findmnt -no SOURCE /cdrom 2>/dev/null || findmnt -no SOURCE /run/live/medium 2>/dev/null)"
    ```
* **`sgdisk: command not found`.** Install it with `sudo apt update && sudo apt install -y gdisk`.

Always confirm the result with `sudo wipefs -n /dev/sda`, which reports remaining signatures without changing anything. It must print nothing.

### Disk Not Recognized by Zero-OS

If you're having trouble getting your disks recognized by Zero-OS, some farmers have had success enabling AHCI mode for SATA in their BIOS.

### Onboard Storage

If you are using a server with onboard storage and are having issues, there are many ways to troubleshooting this. 

You can use the on board storage on a server without RAID. You can [re-flash](https://fohdeesha.com/docs/perc)  the RAID card, turn on HBA/non-RAID mode, or install a different card. There is no need for RAID with ThreeFold farming.

It's usually easy to set servers such as a HP Proliant with the HBA mode. For Dell servers, you can either cross-flash the RAID controller with an “IT-mode-Firmware” (see this [video](https://www.youtube.com/watch?v=h5nb09VksYw)) or get a DELL H310-controller (which has the non-RAID option). Otherwise, you can install a NVME SSD with a PCIe adaptor, and turn off the RAID controller.




### When I tried to boot my 3Node, at some point the screen went black, with or without a blinking hyphen or dash. What could cause this and what could I do to resolve the issue?

There is a possibility that this happens because you are booting your 3Node on a HDD. A 3Node needs a minimum of 500GB of SSD to work properly.

Also, make sure that you are using the correct boot option (Legacy BIOS or UEFI) in Settings and that it corresponds to the correct booting image on the ThreeFold Bootstrap page.

This problem often arises when you plug your disks in the wrong controller. For example, try unplugging the disks from the SAS controller, and plug them in the SATA controller. Also, disable the SAS controller if needed.

In a Legacy BIOS boot, make sure Legacy is enabled and disable *Data Execution Prevention* if possible.

Also, it might have to do with your RAID controller configuration. Make sure this is properly set. For example, configuring all the HDD disks into one logical disk can fix this problem, or re-flashing the RAID card can also help.



### I  get the error Certificate is not yet valid when booting my 3Node server, what can I do?

Make sure your firmware is up to date. If necessary, reinstall it. You might have to install and then re-install the firmware if your system is very old. 



### My SSD is sometimes detected as HDD by Zero-OS when there is a reboot. Is there a fix or a way to test the SSD disk?

If your SSD disk shows as HDD, usually you can reboot the 3Node and Z-OS adjusts correctly.

Anyone experiencing frequently this issue where Z-OS sometimes detects an SSD as HDD can try the following:

* Boot up a live Ubuntu Desktop image
* Run the benchmark utility within the Disks app
* Check if the seektime of the disk is sufficient for Z-OS
  * If the seektime is above 0.5ms, Z-OS will consider your SSD as HDD

**Detailed Steps:**

* Boot a Ubuntu Linux live USB
* Install **gnome-disks** if it isn't already installed:
  * ```
    sudo apt install gnome-disks
    ```
* Open the application launcher and search for **Disks**
* Select your disk
* Click on the tree dots menu
* Select **Benchmark Disk...**
  * Use the default parameters
    * **Transfer rate**: This is not relevant for our current test
      * You can set to it to minimum (e.g. 2)
  * **Sample size**: 10 MB is sufficient
* Check the average access time on the [ThreeFold repository](https://www.github.com/threefoldtech/seektime)
  * Check seek time for HDD and SSD
    * A SSD needs to be \<=0.5ms
* If the result is above 0.5ms, this is why Z-OS doesn't recognize the disk properly
  * You can then run diagnostics (e.g. smartmontools)
    * If this is not fixable, you should change disk (e.g. take a more performing disk)

Note: The green dots on the output represent seektime and that's what Z-OS is looking at. Specifically, it checks that the average seektime is below 0.5ms. If the seektime is above this, Z-OS will consider your SSD as HDD.

### My 3Node uses only PCIe adapters and SSD NVME disks. Do I need the RAID controller on? 

The onboard RAID controller is not linked to your PCIe SSDs. In this case, you can switch the RAID controller off.


### My 3Node has 2 ethernet ports in the back, with one written AMT above, what does it mean? Can I use this port to connect my 3Node to the ThreeFold Grid?

First, let's define the term AMT. It means: Active Management Technology. Without going into too much details, it is to remotely access servers via the network at the BIOS level. Thus, you should plug the ethernet cable in the port next to AMT, and not into the AMT port. You can explore AMT properties if you want remote access to your server.


### When I boot my Dell server, I get the message: All of the disks from your previous configuration are gone... Press any key to continue or 'C' to load the configuration utility. What can I do?

Many changes to your server can lead to this message. 

Usually, the easiest solution is to reset the disk configuration in iDRAC's configuration utility.

What can causes this message:

1. During a new installation, the cables connecting to your external storage are not wired to the correct ports.
2. Your RAID adapter has failed.
3. Your SAS cables are not plugged properly or are malfunctioning.

Note: Resetting the configuration will destroy all data on all virtual disks. Make sure you know what you are doing! In doubt, ask the TF community.

### When booting a 3Node, how to fix the error: "no disks: registration failed"?

There can be many different fixes for this error. Here are some troubleshooting tips to test separately:

* In BIOS, enable AHCI
* Make sure to [wipe the disks](../3node_building/wipe_all_disks) of the 3Nodes
* If the 3Node has a RAID Controller:
  * Disabled the RAID controller, OR;
  * [Flash the RAID controller](https://fohdeesha.com/docs/perc) (i.e. crossflashing), OR;
  * Change the controller to a Dell H310 controller (for Dell servers)
* Try the command **badblocks** (replace **sda** with your specific disk). Note that this command will delete all the data on the disk
  * ```
    sudo badblocks -svw -b 512 -t 0x00 /dev/sda
    ```

### I have trouble connecting the 3Node to the Grid with a 10GB NIC card. What can I do?

As of now, Zero-OS sometimes has trouble with 10GB NIC card. The easiest solution to this is to connect your 3Node with the 1GB NIC card. This should solve the issue. More fine tuning might be needed to get your 3Node to work with a 10GB NIC card. Future Zero-OS version might solve this issue.

### What does it mean when I see, during the 3Node boot, the message: error = context deadline exceeded?

In general, this message means that the ThreeFold Grid asked something to your 3Node, and your 3Node could not respond fast enough. It is usually necessary to read the following error message to understand the situation more specifically.

### How can I fix the error messages: "context deadline exceeded" accompanied with "node is behind acceptable delay with timestamp"?

This often indicates that the real-time clock of the system is not synced with current time. There have been different fixes reported to this issue.

You can boot the node using a Ubuntu live image to sync the hardware time. After that, you can reboot the node and it should boot normally.

You can fix this manually in the BIOS. Go to the BIOS settings and adjust the **Time** and **Date** settings.

You can also try to adjust the clock by NTP over the network, if it applies to your case.

### I try to boot a 3Node, but I get the error: "No Route to Host on Linux". What does it mean?

There are many potential answers to this. Perhaps the Host is offline, the service isn't running. This is usually the reason with TF Grid. It means the Grid is not responsive. In this case, try to boot the 3Node later. If it persists ask TF Support.

There can also be other reasons. You might have connected to the wrong port. Perhaps you have configured iptables to block connections on that port. Your DNS might be improperly configured. You might have an Incorrect Network or Host Configuration. Many troubleshoots are possible. Here's a [good place to start](https://www.maketecheasier.com/fix-no-route-to-host-error-linux/).



### How can I fix the error: "Network configuration succeed but Zero-OS kernel could not be downloaded" when booting a 3Node?

To fix the error "Network configuration succeed but Zero-OS kernel could not be downloaded", you can try to restart the router and reboot the 3Node. This usually fixes the issue. If this doesn't work, check if the router is still functional. The cause of this issue might be that your router is broken.



### Using SAS disks, I get the error; "No ssd found, failed to register". What can I do to fix this?

First make sure to wipe the disks and then boot your 3Node. If you've wiped the disks and it doesn't work, it's been reported that using the command "diskpart clean command" on Windows can fix this issue.


### When booting a 3Node, I get the message: failed to register node: failed to create node: failed to submit extrinsic: Invalid Transaction: registration failed. What could fix this?

The most probable fix to this error is simply to properly [wipe your disks](../3node_building/wipe_all_disks).


### I did a format on my SSD disk, but Zero-OS still does not recognize them. What's wrong?

Formatting is one thing, but to boot properly, Zero-OS needs to work on a completely wiped disk. Thus, make sure you [wipe your disks](../3node_building/wipe_all_disks). Formatting is not enough.

### My 3Node doesn't boot properly without a monitor plugged in. What can I do?

First, try to disable the "Halt On" mode in BIOS. If you do not have this option, try simply enabling Legacy Support (Dell BIOS for example). If this doesn't work, try to plug in a Dummy Plug/Headless Ghost/Display Emulator in your 3Node. This will simulate a plugged monitor. This should fix the problem.




### My 3Node won't boot without disabling the Secure Boot option, is it safe?

In the case where you want to boot Zero-OS, disabling Secure Boot option is safe. With Secure Boot disabled, it can be easier or even necessary when it comes to booting Zero-OS. Secure Boot is used when you want to lock the BIOS/UEFI settings.




### When booting the 3Node, I get the error Network interface detected but autoconfiguration failed. What can I do?

First make sure your network cable is plugged in and that your DHCP is working and responding. If you change the NIC port of the ethernet cable, make sure to reboot the 3Node so Zero-OS can change the NIC port attribution.

Some farmers reported that this got fixed by simply powering off the 3Node(s), the router and modem for 2 minutes then powering it all back on. Resetting the modem and router (switch on the hardware) in the process can also help.

If this doesn't work, try to upgrade the firmware of the NIC and the motherboard. If this still doesn't work, the NIC card might be broken. Try with another NIC card.


### When I try to boot my 3Node, the fans start spinning fast with a loud noise and the screen is black. What can I do to resolve this?

There may be several causes to this issue. You can try to remove all the RAM sticks, to clean the dust and then to reseat the RAM sticks. If it still doesn't resolve the issue, you can check the RAM sticks one by one to see if one is malfunctioning. This often resolves the issue. Also, some cables might not be properly connected.



### When booting Zero-OS with IPV6 configurations, I get the errors (1) dial tcp: address IPV6-address too many columns in address and (2) no pools matches key: not routable. What can I do to fix this issue?

This usually means that the IPV6 attributed is not valid. It is also often caused when the DNS configuration does not resolve IPV6 correctly.

To fix this issue, it is often necessary to adjust the IPV6 settings related to the router and the modem. Confirming with your Internet service provider (ISP) that the IPV6 settings are properly configured could also be necessary to fix the issue.



### I try to boot a 3Node, but I get the message no route with default gateway found. What does it mean?

First, let's see the main terms. Default gateway acts as an access point to other networks, in this case the TF Grid, when there is a back and forth exchange of data packets.

While the last question implied a communication problem from the Grid, this error message usually means that the 3Node has communication problem. In short, it has difficulty reaching the TF Grid. There are many ways to troubleshoot this error. First, let's give the most direct solution. Make sure you have a direct connection with your Internet Service Provider (ISP): your 3Node should be connected to a router or a switch via an ethernet cable. Wifi doesn't work. Make sure your DHCP is set correctly.

If the problem persists, check the default gateway of your 3Node and then make sure your router can reach it. 


### When booting a 3Node, Zero-OS downloads fine, but then I get the message: error no route with default gateway found, and the message: info check if interface has a cable plugged in. What could fix this?

Make sure you have network stack enabled in BIOS. If so, check you ethernet port and make sure that it's clean. Also make sure the ethernet rj45 connectors are clean on both ends. If that does not work, verify the state of your SATA cables. If all this doesn't work, download and re-install Zero-OS.




### How can I update Dell and HP servers to Intel E5-2600v2, E5-2400v2 and E5-4600v2, when applicable?

There are many ressources online with steps on how to do this. You can check this [youtube video](https://www.youtube.com/watch?v=duzrULLtonM) on Dell and HP servers, as welll as this [documentation](https://ixnfo.com/en/hp-proliant-gen8-update-to-support-cpu-e5-2600v2-e5-2400v2-e5-4600v2.html) for HP Proliant Gen8.



### How can I update the firmware and driver of a Dell PowerEdge server?

Dell has excellen documentation for this. Read [this](https://www.dell.com/support/kbdoc/en-us/000128194/updating-firmware-and-drivers-on-dell-emc-poweredge-servers) for the detailed steps.



### When I boot a 3Node in UEFI mode, it gets stuck at: Initializing Network Device, is there a way to fix this?

In short, booting the 3Node in BIOS mode instead of UEFI mode usually fixes this issue.

You can make bootable USB with the USB option of the [Zero-OS bootstrap image page](https://bootstrap.grid.tf/). Make sure to boot your server using BIOS and not UEFI. In the boot sequence, make the USB as your first choice to boot.



### When I boot my 3Node, it gets stuck during the Zero-OS download. It never reaches 100%. What can I do to fix this issue?

Here are some ways to troubleshoot your 3Node when it cannot download Zero-OS completely (to 100%):

* Sometimes, just rebooting the 3Node and/or trying a little bit later can work.
* It can help to reboot the modem and the router. 
* Make sure your BIOS/UEFI is up to date. Updating the BIOS/UEFI can help. 
* It can also help to set the correct date and time.



### When booting a 3Node, I get the error=“context deadline exceeded” module=network error=failed to initialize rmb api failed to initialized admin mw: failed to get farm: farm not found: object not found. What can I do to fix this issue?

Usually, the simple fix to this issue is to make sure that your bootstrap image is on the same network as your farm. For example, if you created your farm on the Main net, you should use a Main net Zero-OS bootstrap image.

## Basic Post Build Troubleshooting

In this section, we cover notions such as how to reboot node or a router, how to check the network signal path and more.

### Reboot a 3Node

To reboot your 3Node, simply turn if off manually then turn it back on.

### Reboot a Router

- Locate the power cord of your router and unplug it from the power outlet.
- Wait for at least 30 seconds to allow the router to completely shut down.
- Plug the power cord back into the power outlet.
- Wait for the router to boot up again. This may take around 2-5 minutes.
- Once the router is back up, check your internet connection to see if it’s working properly.

### Reboot a Modem with the Reset Button

- Find the reset button on the back or bottom of the modem.
- Press and hold the reset button for 30 seconds.
- Release the button when the power light turns another color (usually amber/orange).
- Wait for the modem to fully reboot and the lights to stabilize.

### My 3Nodes go offline after a modem reboot. Is there a way to prevent this?

Yes, there are many ways to prevent this. An easy solution is to set the DHCP server to reserve local IPs for the 3Nodes MAC addresses.

This problem is also preventable if your router stays online during the modem reboot. 

Indeed, rebooting the 3Nodes is necessary when there are local IP changes, as 3Nodes are addressed a local IP addresses when they are booted.

The DHCP will addresses any local IP address that is available when you are booting a 3Node. Reserving local IP addresses is a good TF farming practice.



### When I try to access iDRAC on a web browswer, even with protected mode off, I get the error The webpage cannot be found, what can I do?

Open iDRAC in the Internet Explorer emulator extension (IE Tab) in Chrome, then update iDRAC. It should work elsewhere then. Sometimes, it will be needed to add "ST1=code" at the end of the IE Tab url.



### When I boot my 3Node, it reaches the Welcome to Zero-OS window, but it doesn't boot properly and there's an error message: failed to load object : type substrate..., what can I do?

Usually simply rebooting the 3Node fixes this problem.

### I want redundancy of power for my 3 nodes. I have two PSU on my Dell server. What can I do?

Make sure you enable the Hot Spare feature. This feature is accessible in iDRAC Settings - Power Configuration. Other servers might have this function, with a different name and configuration. Check the server's manual for more details.

### I switch the ethernet cable to a different port when my 3Node was running. Internet connection is lost. What can I do?

When your 3Node boots, Zero-OS marks the NIC port. This means you cannot change NIC port when your 3Node is running. You can either put back the ethernet cable in the initial NIC port, or reboot the 3Node. At boot, Zero-OS will marks the new NIC port as the main entry.


## Advanced Post Build Troubleshooting

In this section, we cover notions such as how to connect a screen and look for errors, how to address certain errors, etc.

### Access the Error/Log Screen

To access the error/log screen, connect a monitor to your 3Node and on the Zero-OS console, hit alt-F2 to open up the Error/Log Screen, and hit alt-F3 to go back to the main screen. 

### Can I use a VGA to HDMI adaptor to connect a TV screen or monitor to the 3Node? I tried to boot a 3Node with a VGA to HDMI adaptor but the boot fails, what can I do?

This might work, but it has been reported by farmers that Zero-OS might have difficulties booting when this is done with a VGA/HDMI adaptor on a TV screen. This is most likely due to the TV screen not supporting the output once the system loaded into Zero-OS. The easy fix to this issue is to use a standard computer monitor with a VGA plug.


### My 3Node is running on the Grid, but when I plugged in the monitor, it states: Disabling IR #16. Is there a problem?

In general, you can simply ignore this error statement. This error is linked to the Nvidia binary driver. It simply means that your 3Node lost connection with the graphic card (by unplugging and replugging the monitor for example).

### Address Certain Errors

Once you had access to the error/log screen and took notes of the errors, you can look for fixes in the manual. This troubleshooting section is a good place to look for solutions.

If you could not find any fixes to your issues, go to the next section to ask for further assistance.

## Memory Troubleshooting

### Can I use different type of RAM for the same 3Node?

No. Always use the same type of RAM per 3Node. If you use RDIMM, go all RDIMM, etc. Check your hardware specifications to make sure you have the right type of memory.



### How can I know if the memory I am buying is correct for my specific hardware?

To be sure, look into the owner's manual of your specific computer.

In general, you can go to [Memory.net](https://memory.net/) and look for your specific computer model. As general steps, select your computer's system in *By system*, then select the series and then select the specific model of the series. You will then see available memories to buy from memory.net. You can also simply read the documentation at the bottom. The memory type supported by your computer will be explained. Then you can buy the memory needed from any other computer store. 

For servers, you can check with Cloudninja's documentation [here](https://cloudninjas.com/pages/server-memory). Search for your specific hardware and look for the compatible memory. This reference is good for rack and tower servers.



### What do the terms RDIMM, LDIMM, UDIMM, LRDIMM, FBDIMM mean when it comes to RAM memory sticks?

Well first, the DIMM means dual inline memory module. 

* U stands for or unregistered (or unbuffered). 

* R stands for registered memory.

* LR stands for load-reduced. 

* FB stands for fully-buffered.



### What is the difference between ECC and non-ECC memory?

ECC means error correction code memory. This type of memory can detect and correct data corruption. Non-ECC mostly cannot detect nor correct, but some can detect, but never correct data corruption. Check your hardware specifications to make sure you have the right type of memory (ECC or non-ECC).


### How can I change the RAM memory sticks on my 3Nodes? How can I achieve dual channel configuration with sticks of RAM?

First, always use RAM sticks of the same size and type. It should be noted on your motherboard which slots to populate first. As a general guide, there is usually 2 slots A and B, with each 2 memory stick entries. You must then install the ram sticks on A1 and B1 in order to achieve dual channel, then A2 and B2 if you have more (visual order: A1 A2 B1 B2).

> Example: You want to start with your largest sticks, evenly distributed between both processors and work your way down to your smallest. Let's take an example with 2 processors as well as 4x 16GB sticks and 4x 8GB sticks. The arrangement would be A1-16GB, B1-16GB, A2-16GB, B2-16GB, A3-8GB, B3-8GB, A4-8GB, B4-8GB. Avoid odd numbers as well. You optimally want pairs. So if you only have 5x 8GB sticks, only install 4 until you have an even 6.



### What does RAM mean?

RAM means random access memory. Those type of memory can be read and changed in any order.




### What does DIMM mean when it comes to RAM sticks?

It means *dual in-line memory module*. This type of computer memory is natively 64 bits, enabling fast data transfer. 



### I have 24 DIMMS ram slots on my server. Can I use them all?

Be careful when installing memory on a server. Always check your server's documentation to make sure your RAM sticks combination are correct. 

For example, on the Dell R720, you can have 24x16gb RAM ECC sticks, but it can only handle 16 Quad ranked DIMMs. In this case, you can fill up all slots with registered DIMMs if you have a maximum of 4 quad DIMMS ranked on each CPU.


## Get Further Assistance

If you've read this whole section and tried different troubleshooting methods to no avail, do not lose hope! You can get further assistance and we will most surely resolve your issues.

You can contact the [ThreeFold support team](https://threefoldfaq.crisp.help/en/) and raise a ticket to get further assistance.

Also, you can ask questions on the [ThreeFold Forum](https://forum.threefold.io/) or on the [ThreeFold Farmer Telegram Channel](https://t.me/threefoldfarmers).
