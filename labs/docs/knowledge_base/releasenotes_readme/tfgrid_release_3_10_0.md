---
title: "TFGrid v3.10.0"
sidebar_position: 368
---

# ThreeFold Grid v3.10.0 Release Note

Release Note of ThreeFold Grid v3.10.0.

- Deployed on Mainnet on 3rd July 2023.

## Components and Services

The following components and services have been upgraded in this release:

- TFChain
- ZOS
- Terraform
- TFGrid-SDK-GO
- TF Gridclient
- TF Gridproxy
- RMB
- TF Weblets
- TF Playground
- TF-Grid-CLI
- Gridify
- TFGrid-SDK-TS

## Upgrades and Improvement Highlights

Below are some of the key highlights of the TFGrid v3.10.0 component upgrades and improvements.

### TFChain 2.4.0

- Addressed syncing issues.
- Introduced the attachment of solution provider IDs to contracts.
- Enabled the bonding of a stash account to a twin.
- Implemented various bug fixes.

### ZOS 3.7.1

- Restructured the capacity to enhance dynamism.
- Added support for proxying traffic to private networks using WireGuard-based gateways.
- Introduced support for cloud-based consoles.
- Resolved various issues related to error messages, user validations, and error handling.

### Terraform 1.9

- Added support for WireGuard-based gateway options.
- Implemented proper timeout handling for deployments.
- Introduced gateway node validation before submitting deployments.
- Resolved various bugs and issues.

### TFGrid-SDK-GO 0.8.0

- Consolidated multiple Go projects into a single repository for simplified administration and quicker releases.
- Extracted reusable code from the Terraform project and created a standalone library for creating new platforms or plugins.

#### Grid-Client

- Enhanced the grid client to serve as the foundation layer for the Terraform plugin, enabling deployment of networks, virtual machines, and Kubernetes.

#### Grid-Proxy

- Added support for standby status for nodes powered off by the farmerbot.
- Enabled farm filtering based on requested resources.

#### RMB

- Improved the direct client's resilience to recover from close connections.

#### TF-Grid-CLI

- Introduced a simple tool for creating virtual machines and Kubernetes clusters. Note that `TF-Grid-CLI` is now `TFCMD`.
- Get started [here](../../documentation/developers/tfcmd/tfcmd.md).

#### Gridify

- An experimental project that allows developers to deploy their projects on ThreeFold as a platform with a single command, "gridify," using a Procfile in their code repository.
- Currently supported platforms include:
  - Go 1.18
  - Python 3.10.10
  - Node 16.17.1
  - NPM 8.10.0
  - Caddy
- Learn more [here](https://github.com/threefoldtech/zos_sdk_go/tree/development/gridify).

### TFGrid-SDK-TS 2.0.0

- Consolidated all components targeting web/TypeScript developers and frontend efforts into a single repository for easier management and rapid releases.
- Moved gridclient, dashboard, statistics websites, and other TypeScript-based projects to the new repository [here](https://github.com/threefoldtech/zos_sdk_ts).

#### Grid-Client

- Gateways now support WireGuard backends.
- Added support for hex secrets.
- Various fixes are detailed [here](https://github.com/orgs/threefoldtech/projects/192/views/12?filterQuery=repo%3A%22threefoldtech%2Ftfgrid-sdk-ts%22+label%3Agrid_client).

#### TF Dashboard

- Added support for IPv4 pricing in the resources calculator.
- Included TFT/USD exchange rate in the dashboard navbar.
- Introduced new standby status for nodes powered off by the farmerbot.
- In the explorer, a node monitoring page is now available.
- Fixed high CPU usage in the DAO Pages.
- Tracking improperly set serial number on nodes with a clear message.

#### TFGrid Weblets

- We are phasing out the TFGrid Weblets for a newer playground rewritten in vue3, however, we introduced some maintenance bugfixes.
- [Support umbrel on the grid](https://github.com/threefoldtech/grid_wiki/issues/1394).

### TF Playground v2.0.0

This release introduces a new playground with a more consistent user experience. Some components have been reworked for consistency.

- Simplified the profile manager, requiring only the provision of a mnemonic and a password for encryption on the device. Mnemonics are never shared or sent across the network.
- Real-time calculation of deployment costs.
- Ability to generate WireGuard configurations.
- Direct link to the monitoring page of a deployment’s hosting node.

## RMB 1.0.5

- Deprecated seed flag.