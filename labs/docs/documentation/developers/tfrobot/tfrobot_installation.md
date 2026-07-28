---
title: "Installation"
sidebar_position: 108
---



## Introduction

This section covers the basics on how to install TFROBOT (`tfrobot`). 

TFROBOT is available as binaries. Make sure to download the latest release and to stay up to date with new releases.

## Mycelium Network

Note that you can use the [Mycelium network](../../system_administrators/mycelium_toc/mycelium_toc.md) to connect to your deployments. To do so, make sure that the Mycelium network is properly set up for the deployments. You can consult the different examples that include the Mycelium network to understand this further.

## Installation

To install TFROBOT, simply download and extract the TFROBOT binaries to your path. 

- Create a new directory for `tfgrid-sdk-go`
  ```
  mkdir tfgrid-sdk-go
  cd tfgrid-sdk-go
  ```
- Download latest release from [releases](https://github.com/threefoldtech/zos_sdk_go/releases)
  - ```
    wget https://github.com/threefoldtech/zos_sdk_go/releases/download/v0.14.4/tfgrid-sdk-go_Linux_x86_64.tar.gz
    ```
- Extract the binaries
  - ```
    tar -xvf tfgrid-sdk-go_Linux_x86_64.tar.gz
    ```
- Move `tfrobot` to any `$PATH` directory:
    ```bash
    mv tfrobot /usr/local/bin
    ```