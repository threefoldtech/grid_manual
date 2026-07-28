---
title: "Installation"
sidebar_position: 73
---



## Introduction

We present here the general steps required to install and use the ThreeFold Grid Client.

The [Grid Client](https://github.com/threefoldtech/zos_sdk_ts/tree/development/packages/grid_client) is written using [TypeScript](https://www.typescriptlang.org/) to provide more convenience and type-checked code. It is used to deploy workloads like virtual machines, kubernetes clusters, quantum storage, and more.

## Mycelium Network

Note that you can use the [Mycelium network](../../system_administrators/mycelium_toc/mycelium_toc.md) to connect to your deployments. To do so, make sure that the Mycelium network is properly set up for the deployments. You can consult the different examples that include the Mycelium network to understand this further.

## Prerequisites

To install the Grid Client, you will need the following on your machine:

- [Node.js](https://nodejs.org/en) ^18
- npm 8.2.0 or higher
- may need to install libtool (**apt-get install libtool**)

> Note: [nvm](https://nvm.sh/) is the recommended way for installing node.

To use the Grid Client, you will need the following on the TFGrid:

- A TFChain account
- TFT in your wallet

If it is not the case, please visit the [Get started section](../../system_administrators/tfgrid3_getstarted/tfgrid3_getstarted.md).

## Installation

### External Package

To install the external package, simply run the following command:

```bash
yarn add @threefold/grid_client
```

> Note: For the **qa**, **test** and **main** networks, please use @2.1.1 version.

### Local Usage

To use the Grid Client locally, clone the repository then install the Grid Client:

- Clone the repository
  - ```bash
    git clone https://github.com/threefoldtech/zos_sdk_ts
    ```
- Install the Grid Client
  - With yarn
      -   ```bash
          yarn install
          ```
  - With npm
      -   ```bash
          npm install
          ```

> Note: In the directory **grid_client/scripts**, we provided a set of scripts to test the Grid Client.

## Getting Started

You will need to set the client configuration either by setting the json file manually (**scripts/config.json**) or by using the provided script (**scripts/client_loader.ts**). 

### Client Configuration

Make sure to set the client configuration properly before using the Grid Client.

- **network**: The network environment (**dev**, **qa**, **test** or **main**).

- **mnemonic**: The 12 words mnemonics for your account. 
  - Learn how to create one [here](../../dashboard/wallet_connector).

- **storeSecret**: This is any word that will be used for encrypting/decrypting the keys on ThreeFold key-value store.

- **ssh_key**: The public SSH key set on your machine.

> Note: Only networks can't be isolated, all projects can see the same network.

## Generate the Documentation

The easiest way to test the installation is to run the following command with either yarn or npm to generate the Grid Client documentation:

* With yarn
  * ```
    yarn run serve-docs
    ```
* With npm
  * ```
    npm run serve-docs
    ```

> Note: You can also use the command **yarn run** to see all available options.

## How to Run the Scripts

You can explore the Grid Client by testing the different scripts proposed in **grid_client/scripts**.

- Update your customized deployments specs if needed
- Run using [ts-node](https://www.npmjs.com/ts-node)
  - With yarn
    - ```bash
      yarn run ts-node --project tsconfig-node.json scripts/zdb.ts
      ```
  - With npx
    - ```bash
      npx ts-node --project tsconfig-node.json scripts/zdb.ts
      ```

## Reference API

While this is still a work in progress, you can have a look [here](https://threefoldtech.github.io/tfgrid-sdk-ts/packages/grid_client/docs/api/index).
