---
title: "Quick Guide"
sidebar_position: 199
---





## Introduction

In this guide, we show how to deploy the [Farmerbot](https://github.com/threefoldtech/tfgrid-sdk-go/tree/development/farmerbot) on a full VM running on the TFGrid. 

This guide can be done on bare metal or on a full VM running on the TFGrid. You need at least two 3Nodes on the same farm to make use of the Farmerbot.

This version of the Farmerbot also works with ARM64. This means that if you have a Pi 3, 4, or Zero 2 with a 64 bit OS, you can download the appropriate release archive and it will work properly.

Read the [Additional Information](farmerbot_information) section for further details concerning the Farmerbot. 

## Prerequisites

- The TFChain account associated with the farm should have at least 5 TFT (recommended is 50 TFT)

## Farmerbot Costs on the TFGrid

If you run the Farmerbot on a 3Node on the TFGrid, you will have to pay TFT to deploy on that 3Node. You can run a full VM at minimum specs for the Farmerbot, that is 1vcore, 15GB of SSD storage and 512MB of RAM. Note that you can use the Planetary Network. You do not need to deploy a 3Node with IPv4. The cost on main net for this kind of workload is around 0.175TFT/hour (as of the date 11-07-23).

Next to that, you will have to pay the transaction fees every time the Farmerbot has to wake up or shut down a node. This means that you need some TFT on the account tied to the twin of your farm. 

For the periodic wakeups, each node in the farm is shut down and powered on once a day, i.e. 30 times per month. Also, there is 10 random wakeups per month for each node. This means that each node is turned off and on 40 times per month in average. In that case, the average cost per month to power on nodes and shut them back down equals:

> average transaction fees cost per month = 0.001 TFT (extrinsic fee) * amount of nodes * 40 * 2 (1 for powering down, one for powering up)

## Enable Wake-On-Lan

For a 3Node to work properly with the Farmerbot, the parameter wake-on-lan must be enabled. Enabling wake-on-lan on your 3Node may differ depending on your computer model. Please refer to the documentation of your computer if needed. 

Usually the feature will be called Wake-on-Lan and you need to set it as "enabled" in the BIOS/UEFI settings.

Here are some examples to guide you:

* Racker Server, Dell R720
  * Go into `System Setup -> Device Settings -> NIC Port -> NIC Configuration`
    * Set Wake-on-Lan to `Enable`
* Desktop Computer, HP EliteDesk G1
  * Go to Power -> Hardware Power Management
    * Disable `S5 Maximum Power Saving`
  * Go to `Advanced -> Power-On Options`
    * Set `Remote Wake up Boot source` to `Remote Server`

> Hint: Check the Z-OS monitor screen and make sure that all the 3Nodes are within the same lan (e.g. all 3Nodes addresses are between 192.168.15.00 and 192.168.15.255).

For more information on WOL, [read this section](farmerbot_information#how-to-prepare-your-farm-for-the-farmerbot-with-wol).

## Deploy a Full VM

For this guide, we run the Farmerbot on a Full VM running on the TFGrid. Note that while you do not need to run the Farmerbot on the TFGrid, the whole process is very simple as presented here.

- Deploy a full VM on the TFGrid
- Update and upgrade the VM
    ```
    apt update && apt upgrade
    ```
- Reboot and reconnect to the VM
    ```
    reboot
    ```

## Farmerbot Setup

We present the different steps to run the Farmerbot using the binaries.

> For a script that can help automate the steps in this guide, [check this forum post](https://forum.threefold.io/t/new-farmerbot-install-script/4207).

### Download the Farmerbot Binaries

- Download the latest [ThreeFold tfgrid-sdk-go release](https://github.com/threefoldtech/tfgrid-sdk-go/releases) and extract the farmerbot for your specific setup (here we use `x86_64`). On the line `wget ...`, make sure to replace `<latest_release>` with the latest Farmerbot release.
    ```
    wget https://github.com/threefoldtech/tfgrid-sdk-go/releases/download/<latest_release>/tfgrid-sdk-go_Linux_x86_64.tar.gz
    tar xf tfgrid-sdk-go_Linux_x86_64.tar.gz farmerbot
    ```
- Move the Farmerbot
    ```
    mv farmerbot /usr/local/bin
    ```
- Remove the tar file
  ```
  rm tfgrid-sdk-go_Linux_x86_64.tar.gz
  ```

### Create the Farmerbot Files

- Create Farmerbot files directory
    ```
    cd ~
    mkdir farmerbotfiles
    ```
- Create the Farmerbot `config.yml` file ([see template below](#configuration-file-template-configyml))
    ```
    nano ~/farmerbotfiles/config.yml
    ```
- Create the environment variables file and set the variables ([see template below](#environment-variables-file-template-env))
    ```
    nano ~/farmerbotfiles/.env
    ```

### Run the Farmerbot

We run the Farmerbot with the following command:

```
farmerbot run -e ~/farmerbotfiles/.env -c ~/farmerbotfiles/config.yml -d
```

For farmers with **ed25519** keys, the flag `-k` should be used. Note that by default, the Farmerbot uses the **sr25519** keys.

```
farmerbot run -k ed25519 -e ~/farmerbotfiles/.env -c ~/farmerbotfiles/config.yml -d
```

For more information on the supported commands, the [Additional Information section](farmerbot_information#supported-commands-and-flags). You can also consult the [Farmerbot repository](https://github.com/threefoldtech/tfgrid-sdk-go/tree/development/farmerbot).

Once you've verified that the Farmerbot runs properly, you can stop the Farmerbot and go to the next section to set a Farmerbot service. This step will ensure the Farmerbot keeps running after exiting the VM.

### Set a systemd Service

It is highly recommended to set a Ubuntu systemd service to keep the Farmerbot running after exiting the VM.

* Create the service file
  * ```
    nano /etc/systemd/system/farmerbot.service
    ```
* Set the Farmerbot systemd service
    
    ```
    [Unit]
    Description=ThreeFold Farmerbot
    StartLimitIntervalSec=0

    [Service]
    Restart=always
    RestartSec=5
    ExecStart=/usr/local/bin/farmerbot run -a --continue-power-on-error -e /root/farmerbotfiles/.env -c /root/farmerbotfiles/config.yml -d

    [Install]
    WantedBy=multi-user.target     
    ```
* Enable the Farmerbot service
    ```
    systemctl daemon-reload
    systemctl enable farmerbot
    systemctl start farmerbot
    ```
* Verify that the Farmerbot service is properly running
    ```
    systemctl status farmerbot
    ```

### Check the Farmerbot Logs

You can get more details on the operation of the Farmerbot by inspecting the log file.

* View the log file
  ```
  journalctl -u <unit file name>
  ```
* View the log file with reverse output
  ```
  journalctl -ru <unit file name>
  ```
* View X lines from the log file
  ```
  journalctl -u <unit file name> -n X 
  ```
* View the log file since a given date
  ```
  journalctl -u <unit file name> --since <date>
  ```
* Create a log file with journalctl with the last 1000 lines
  ```
  journalctl -u farmerbot -n 1000 > farmerbot.log
  ```

### Stop the Farmerbot

You can stop the farmerbot with the following command:

```
systemctl stop farmerbot
```

After stopping the farmerbot, any nodes in standby mode will remain in standby. To bring them online, use this command:

```
farmerbot start all -e /root/farmerbotfiles/.env --farm <farm_id>
```

## Farmerbot Files

### Configuration File Template (config.yml)

In this example, the farm ID is 1, we are setting the Farmerbot with 4 nodes and the node 1 never shuts down, we set a periodic wakeup at 1:00PM.

Note that the timezone of the farmerbot will be the same as the time zone of the machine the farmerbot running inside. By default, a full VM on the TFGrid will be set in UTC.

```
farm_id: 1
included_nodes:
  - 1
  - 2 
  - 3 
  - 4  
never_shutdown_nodes:
  - 1
power:
  periodic_wake_up_start: 01:00PM
```

Note that if the user wants to include all the nodes within a farm, they can simply omit the `included_nodes` section. In this case, all nodes of the farm will be included in the Farmerbot, as shown in the example below. If you are proceeding like this, make sure that you don't have any unused node IDs on your farm, as the Farmerbot would try to wake up nodes that aren't running anymore on the grid.

```
farm_id: 1  
never_shutdown_nodes:
  - 1
power:
  periodic_wake_up_start: 01:00PM
```

For more information on the configuration file, refer to the [Additional Information section](farmerbot_information#yaml-configuration-file-template).

You can also consult the [Farmerbot repository](https://github.com/threefoldtech/tfgrid-sdk-go/tree/development/farmerbot).

### Environment Variables File Template (.env)

The network can be either `main`, `tets`, `dev` or `qa`. The following example is with the main network.

```
MNEMONIC_OR_SEED="word1 word2 word3 ... word12"
NETWORK="main"
```

## Running Multiple Farmerbots on the Same VM

You can run multiple instances of the Farmerbot on the same VM.

To do so, you need to create a directory for each instance of the Farmerbot. Each directory should contain the configuration and variables files as shown above. Once you've set the files, you can simply execute the Farmerbot `run` command to start each bot in each directory.

It's recommended to use distinct names for the directories and the services to easily differentiate the multiple farmerbots running on the VM.

For example, the directory tree of two Farmerbots could be:

```
└── farmerbotfiles
    ├── farmerbot1
    │   ├── .env
    │   └── config.yml
    └── farmerbot2
        ├── .env
        └── config.yml
```

For example, the services of two Farmerbots could be named as follows:

```
farmerbot1.service
farmerbot2.service
```

## Questions and Feedback

This guide is meant to get you started quickly with the Farmerbot. That being said, there is a lot more that can be done with the Farmerbot.

For more information on the Farmerbot, please refer to the [Additional Information section](./farmerbot_information). You can also consult the [official Farmerbot Go repository](https://github.com/threefoldtech/tfgrid-sdk-go/tree/development/farmerbot).

If you have any questions, you can ask the ThreeFold community for help on the [ThreeFold Forum](https://forum.threefold.io/) or on the [ThreeFold Farmers Chat](https://t.me/threefoldfarmers) on Telegram.

> This is the new version of the Farmerbot written in Go. If you have any feedback and issues, please let us know!