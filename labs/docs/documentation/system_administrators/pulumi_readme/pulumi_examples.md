---
title: "Deployment Examples"
sidebar_position: 229
---





## Introduction

[Pulumi](https://www.pulumi.com/) is an infrastructure as code platform that allows you to use familiar programming languages and tools to build, deploy, and manage cloud infrastructure.

We present here the basic steps to test the examples within the [ThreeFold Pulumi](https://github.com/threefoldtech/grid_pulumi) plugin repository. Once you've set the plugin and exported the necessary variables, the deployment process from one example to another is very similar.

Please note that the Pulumi plugin for ThreeFold Grid is not yet officially published. We look forward to your feedback on this project.

## Check All the Examples

In the manual, we cover some basic examples of Pulumi deployments on the grid. 

You can access all the Pulumi deployment examples on the ThreeFold Pulumi repository [here](https://github.com/threefoldtech/grid_pulumi/tree/development/examples).

## Prerequisites

There are a few things to set up before exploring Pulumi. Since we will be using the examples in the ThreeFold Pulumi repository, we must clone the repository before going further.

* [Install Pulumi](./pulumi_install) on your machine
* Clone the **Pulumi-ThreeFold** repository
  * ```
    git clone https://github.com/threefoldtech/grid_pulumi
    ```
* Change directory
  * ```
    cd ./pulumi-threefold
    ```

## Set the Environment Variables

You can export the environment variables before deploying workloads.

* Export the network (**dev**, **qa**, **test**, **main**). Note that we are using the **dev** network by default.
  * ```
    export NETWORK="Enter the network"
    ```
* Export your mnemonics. 
  * ```
    export MNEMONIC="Enter the mnemonics"
    ```
* Export the SSH_KEY (public key).
  * ```
    export SSH_KEY="Enter the public Key"
    ```

## Test the Plugin

Once you've properly set the prerequisites, you can test many of the examples by simply going into the proper repository and running **make run**.

The different examples that work simply by running **make run** are the following:

* virtual_machine
* kubernetes
* network
* zdb
* gateway_name

We give an example with **virtual_machine**.

* Go to the directory **virtual_machine**
  * ```
    cd examples/virtual_machine
    ```
* Deploy the Pulumi workload with **make**
  * ```
    make run
    ```

Note: To test **gateway_fqdn**, you will have to update the fqdn in **Pulumi.yaml** and create an A record for your domain pointing to the gateway IP.


## Destroy the Deployment

You can destroy your Pulumi deployment at any time with the following make command:

```
make destroy
```   