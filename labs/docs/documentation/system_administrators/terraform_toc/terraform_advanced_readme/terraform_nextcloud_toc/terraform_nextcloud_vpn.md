---
title: "Nextcloud 2-Node VPN Deployment"
sidebar_position: 269
---





# Introduction

This guide is a proof-of-concept to show that, using two VMs in a WireGuard VPN, it is possible to, on the first VM, set a Nextcloud AIO instance on the TFGrid, set on it a daily backup and update with Borgbackup, and, on the second VM, set a second daily backup of the first backup. This means that we have 2 virtual machines, one VM with the Nextcloud instance and the Nextcloud backup, and another VM with a backup of the Nextcloud backup. 

This architecture leads to a higher redundancy level, since we can afford to lose one of the two VMs and still be able to retrieve the Nextcloud database. Note that to achieve this, we are creating a virtual private network (VPN) with WireGuard. This will connect the two VMs and allow for file transfers. While there are many ways to proceed, for this guide we will be using [ssh-keygen](https://linux.die.net/man/1/ssh-keygen), [Rsync](https://linux.die.net/man/1/rsync) and [Cron](https://linux.die.net/man/1/crontab).

Note that, in order to reduce the deployment cost, we set the minimum CPU and memory requirements for the Backup VM. We do not need high CPU and memory for this VM since it is only used for storage.

Note that this guide also make use of the ThreeFold gateway. For this reason, this deployment can be set on any two 3Nodes on the TFGrid, i.e. there is no need for IPv4 on the 2 nodes we are deploying on, as long as we set a gateway on a gateway node.

This guide also includes a comprehensive recovery section that provides step-by-step instructions for restoring your Nextcloud instance from Borgbackup files in case of deployment failure. With these recovery procedures, you can quickly rebuild your Nextcloud environment with minimal data loss.

For now, let's see how to achieve this redundant deployment with Rsync!

# 2-Node Terraform Deployment

For this guide, we are deploying a Nextcloud AIO instance along a Backup VM, enabling daily backups of both VMs. The two VMs are connected by a WireGuard VPN. The deployment will be using the [Nextcloud FList](https://github.com/threefoldtech/zos_images/tree/development/tfgrid3/nextcloud) available in the **tf-images** ThreeFold repository. 

## Create the Terraform Files

For this guide, we use two files to deploy with Terraform. The first file contains the environment variables and the second file contains the parameters to deploy our workloads.

To facilitate the deployment, only the environment variables file needs to be adjusted. The **main.tf** file contains the environment variables (e.g. **var.size** for the disk size) and thus you do not need to change this file. Of course, you can adjust the deployment based on your preferences. That being said, it should be easy to deploy the Terraform deployment with the main.tf as is.

For this example, we will be deploying the Nextcloud instance with a ThreeFold gateway and a gateway domain. Other configurations are possible.

### Variables File

* Copy the following content and save the file under the name `credentials.auto.tfvars`:

```
mnemonic = "..."
SSH_KEY = "..."
network = "main"

size_vm1 = "50"
cpu_vm1 = "2"
memory_vm1 = "4096"

size_vm2 = "50"
cpu_vm2 = "1"
memory_vm2 = "512"

gateway_id = "50"
vm1_id = "5453"
vm2_id = "12"

deployment_name = "nextcloudgatewayvpn"
nextcloud_flist = "https://hub.grid.tf/tf-official-apps/threefoldtech-nextcloudaio-latest.flist"
```

Make sure to add your own seed phrase and SSH public key. Simply replace the three dots by the content. Note that you can deploy on a different node than node 5453 for the **vm1** node. If you want to deploy on another node than node 5453 for the **gateway** node, make sure that you choose a gateway node. To find a gateway node, go on the [ThreeFold Dashboard](https://dashboard.grid.tf/) Nodes section of the Explorer and select **Gateways (Only)**.

Obviously, you can decide to increase or modify the quantity for the CPU, memory and size variables. Note that we set the minimum CPU and memory parameters for the Backup VM (**vm2**). This will reduce the cost of the deployment. Since the Backup VM is only used for storage, we don't need to set the CPU and memory higher.

### Main File

* Copy the following content and save the file under the name `main.tf`:

```
variable "mnemonic" {
  type = string
  default = "your mnemonic"
}

variable "network" {
  type = string
  default = "main"
}

variable "SSH_KEY" {
  type = string
  default = "your SSH pub key"
}

variable "deployment_name" {
  type = string
}

variable "size_vm1" {
  type = string
}

variable "cpu_vm1" {
  type = string
}

variable "memory_vm1" {
  type = string
}

variable "size_vm2" {
  type = string
}

variable "cpu_vm2" {
  type = string
}

variable "memory_vm2" {
  type = string
}

variable "nextcloud_flist" {
  type = string
}

variable "gateway_id" {
  type = string
}

variable "vm1_id" {
  type = string
}

variable "vm2_id" {
  type = string
}


terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    }
  }
}

provider "grid" {
    mnemonic = var.mnemonic
    network = var.network
}

data "grid_gateway_domain" "domain" {
  node = var.gateway_id
  name = var.deployment_name
}

resource "grid_network" "net" {
    nodes = [var.gateway_id, var.vm1_id, var.vm2_id]
    ip_range = "10.1.0.0/16"
    name = "network"
    description = "My network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
  node = var.vm1_id
  network_name = grid_network.net.name

  disks {
    name = "data"
    size = var.size_vm1
  }

  vms {
    name = "vm1"
    flist = var.nextcloud_flist
    cpu = var.cpu_vm1
    memory = var.memory_vm1
    rootfs_size = 15000
    entrypoint = "/sbin/zinit init"
    env_vars = {
      SSH_KEY = var.SSH_KEY
      GATEWAY = "true"
      IPV4 = "false"
      NEXTCLOUD_DOMAIN = data.grid_gateway_domain.domain.fqdn
    }
    mounts {
        name = "data"
        mount_point = "/mnt/data"
    }
  }
}

resource "grid_deployment" "d2" {
  disks {
    name = "disk2"
    size = var.size_vm2
  }
  node         = var.vm2_id
  network_name = grid_network.net.name

  vms {
    name       = "vm2"
    flist      = "https://hub.grid.tf/tf-official-vms/ubuntu-22.04.flist"
    cpu        = var.cpu_vm2
    mounts {
        name = "disk2"
        mount_point = "/disk2"
    }
    memory     = var.memory_vm2
    entrypoint = "/sbin/zinit init"
    env_vars = {
      SSH_KEY = var.SSH_KEY
    }
    planetary = true
  }
}

resource "grid_name_proxy" "p1" {
  node            = var.gateway_id
  name            = data.grid_gateway_domain.domain.name
  backends        = [format("http://%s:80", grid_deployment.d1.vms[0].ip)]
  network         = grid_network.net.name
  tls_passthrough = false
}

output "wg_config" {
  value = grid_network.net.access_wg_config
}

output "vm1_ip" {
  value = grid_deployment.d1.vms[0].ip
}

output "vm2_ip" {
  value = grid_deployment.d2.vms[0].ip
}


output "fqdn" {
  value = data.grid_gateway_domain.domain.fqdn
}
```

## Deploy the 2-Node VPN

We now deploy the 2-node VPN with Terraform. Make sure that you are in the correct folder containing the main and variables files.

* Initialize Terraform:
  *  ```
     terraform init
     ```

* Apply Terraform to deploy Nextcloud:
  *  ```
     terraform apply
     ```

Note that, at any moment, if you want to see the information on your Terraform deployment, write the following:
  * ```
    terraform show
    ```

# Nextcloud Setup

* Access Nextcloud Setup
  * Once you've deployed Nextcloud, you can access the Nextcloud Setup page by pasting on a browser the URL displayed on the line `fqdn = "..."` of the `terraform show` output. For more information on this, [read this page](../../../../dashboard/deploy/applications/nextcloud.md).
* Create a backup and set a daily backup and update
  * Make sure to create a backup with `/mnt/backup` as the mount point, and set a daily update and backup for your Nextcloud VM. For more information, [read this page](../../../../dashboard/deploy/applications/nextcloud.md).

> Note: By default, the daily Borgbackup is set at 4:00 UTC. If you change this parameter, make sure to adjust the moment the Rsync backup is done.

# Nextcloud VM Prerequisites

We need to install a few things on the Nextcloud VM before going further.

* Update the Nextcloud VM
  * ```
    apt update
    ```
* Install ping on the Nextcloud VM if you want to test the VPN connection (Optional)
  * ```
    apt install iputils-ping -y
    ```
* Install Rsync on the Nextcloud VM
  * ```
    apt install rsync
    ```
* Install nano on the Nextcloud VM
  * ```
    apt install nano
    ```
* Install Cron on the Nextcloud VM
  * apt install cron

# Prepare the VMs for the Rsync Daily Backup

* Test the VPN (Optional) with [ping](../../../computer_it_basics/cli_scripts_basics#test-the-network-connectivity-of-a-domain-or-an-ip-address-with-ping)
  * ```
    ping <WireGuard_VM_IP_Address>
    ```
* Generate an SSH key pair on the Backup VM
  * ```
    ssh-keygen
    ```
* Take note of the public key in the Backup VM
  * ```
    cat ~/.ssh/id_rsa.pub
    ```
* Add the public key of the Backup VM in the Nextcloud VM
  * ```
    nano ~/.ssh/authorized_keys
    ```

> Make sure to put the Backup VM SSH public key before the public key already present in the file **authorized_keys** of the Nextcloud VM.

# Create a Cron Job for the Rsync Daily Backup

We now set a daily cron job that will make a backup between the Nextcloud VM and the Backup VM using Rsync.

* Open the crontab on the Backup VM
  * ```
    crontab -e
    ```
* Add the cron job at the end of the file
  * ```
    0 8 * * * rsync -avz --no-perms -O --progress --delete --log-file=/root/rsync_storage.log root@10.1.3.2:/mnt/backup/ /mnt/backup/ 
    ```

> Note: By default, the Nextcloud automatic backup is set at 4:00 UTC. For this reason, we set the Rsync daily backup at 8:00 UTC.

> Note: To set Rsync with a script, [read this documentation](../../../computer_it_basics/file_transfer#automate-backup-with-rsync). 

# Recovery from Borgbackup

If your Nextcloud deployment fails but you have access to your Borgbackup files, you can restore your entire instance following these recovery procedures.

## 1. Deploy a New Nextcloud Instance

First, deploy a new Nextcloud AIO instance following the Terraform deployment steps presented in this guide. Do not start the containers yet.

## 2. Access Your Backup Files

You have two options to access your backup files:

- **From Primary VM Backup**: If your first VM failed but you can still access the backup files in `/mnt/backup/borg`
- **From Secondary VM Backup**: If you have the Rsync backup from your secondary VM

## 3. Prepare for Restoration

You'll need:
- The Borg repository (the backup files folder)
- The encryption password that was shown in the AIO interface when you created your first backup

## 4. Restore from the AIO Interface

1. On your new Terraform deployment, access the AIO interface at port 8080 (e.g., `https://ip.address.of.this.server:8080`)
2. During the initial setup, select "Restore former AIO instance from backup"
3. Enter the encryption password from your old backup
4. Specify the path to the backup folder (without the "borg" part), for example:
   - If your backup is at `/mnt/backup/borg`, enter `/mnt/backup`
   - If you copied your backup to a new location, provide that path
5. Click "Submit location and password"
6. Choose the latest backup from the dropdown and click "Restore selected backup"
7. Wait for the restoration process to complete
8. Start the containers through the AIO interface

## 5. Verification

After restoration is complete:
1. Access your Nextcloud instance through your domain
2. Verify that your files, users, and applications are properly restored
3. Check that all services are working correctly
4. Configure a new backup schedule to ensure continued data protection

## Troubleshooting Recovery

If you encounter issues during recovery:

- **Incorrect Password**: Double-check the encryption password is correct (it's case-sensitive)
- **Backup Path Issues**: Ensure the path points to the directory containing the "borg" folder, not the "borg" folder itself
- **Permission Problems**: If using a copied backup, ensure the permissions are set correctly with `chown -R 33:0` and `chmod -R 750`
- **Database Errors**: If you see database errors after restore, try running maintenance commands through the Nextcloud container:
  ```
  sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ maintenance:repair
  ```

By following these steps, you should be able to successfully recover your Nextcloud deployment from your Borgbackup files, ensuring minimal data loss in case of a deployment failure.