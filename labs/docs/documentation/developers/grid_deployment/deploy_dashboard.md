---
title: "Deploy the Dashboard"
sidebar_position: 170
---



## Introduction

We show how to deploy the Dashboard (devnet) on a full VM. To do so, we set an SSH tunnel and use the VSCodium Remote Explorer function. We will then be able to use a source-code editor to explore the code and see changes on a local browser.

We also show how to provide a public access to the Dashboard by setting a gateway domain to your full VM deployment. Note that this method is not production-ready and should only be used to test the Dashboard.

## Prerequisites

- TFChain account with TFT
- [Deploy full VM with WireGuard connection](../../system_administrators/tfgrid3_getstarted/ssh_guide/advanced_methods/ssh_wireguard)
- [Make sure you can connect via SSH on the terminal](../../system_administrators/tfgrid3_getstarted/ssh_guide/ssh_openssh)

In this guide, we use WireGuard, but you can use other connection methods, such as [Mycelium](../../system_administrators/mycelium_toc/mycelium_toc.md).
  
## Create an SSH Tunnel

- Open a terminal and create an SSH tunnel
    ```
    ssh -4 -L 5173:127.0.0.1:5173 root@10.20.4.2
    ```

Simply leave this window open and follow the next steps.

If you use an IPv6 address, e.g. with Mycelium, set `-6` in the line above instead of `-4`.

## Editor SSH Remote Connection

You can connect via SSH through the source-code editor to a VM on the grid. In this example, WireGuard is set.

- Add the SSH Remote extension to [VSCodium](https://vscodium.com/)
- Add a new SSH remote connection
- Set the following (adjust with your own username and host)
  ``` 
  Host 10.20.4.2
      HostName 10.20.4.2
      User root
  ```
- Click on `Connect to host`

## Set the VM

We set the VM to be able to build the Dashboard.

```

apt update && apt install build-essential python3 -y

wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion

nvm install 18

npm install -g yarn

```

## Build the Dashboard

We now build the Dashboard.

Clone the repository, then install, build and run the Dashboard. Note that here it is called `playground`:

```

git clone https://github.com/threefoldtech/zos_sdk_ts

cd tfgrid-sdk-ts/

yarn install

make build

make run project=playground

```

You can then access the dev net Dashboard on your local browser.

To stop running the Dashboard, simply enter ̀`Ctrl-C` on the terminal window.


## Dashboard Public Access

> Note: This method is not production-ready. Use only for testing purposes.

Once you've tested the Dashboard with the SSH tunnel, you can explore how to access it from the public Internet. For this, we will create a gateway domain and bind the host to `0.0.0.0`.

On the Full VM page, [add a domain](../../dashboard/deploy/vm_intro/add_domain) to access your deployment from the public Internet.

- Under `Actions`, click on `Manage Domains`
- Go to `Add New Domain`
- Choose a gateway domain under `Select domain`
- Set the port 5173
- Click on `Add`

To run the Dashboard from the added domain, use this instead of the previous `make run` line:

```
cd packages/playground
yarn dev --host 0.0.0.0
```

You can then access the Dashboard from the domain you just created.

## Set the Network

You can set the network by running the configuration script. Simply set the network as the **MODE** (e.g. **main**, **test**, **dev**):

```
cd packages/playground/public
MODE=main ../scripts/build-env.sh
```

Once you've set the configuration file, you can build and run the Dashboard.

## Questions and Feedback

If you have any questions or feedback, please let us know by either writing a post on the [ThreeFold Forum](https://forum.threefold.io/), or by chatting with us on the [TF Grid Tester Community](https://t.me/threefoldtesting) Telegram channel.