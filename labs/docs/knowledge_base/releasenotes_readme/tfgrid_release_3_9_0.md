---
title: "TFGrid v3.9.0"
sidebar_position: 369
---

# ThreeFold Grid v3.9.0 Release Note

Release Note of ThreeFold Grid v3.9.0.

- Live on Mainnet 12/04/2023
- Live on Testnet 23/03/2023


This release is mainly around power management/capacity planning orchestrated by the farmerbot based on Wake-on Lan (WOL) and the reliable message bus (RMB) and the toolings update to utilize both. It also includes several other updates, improvements and fixes of numerous grid components as described below:

## The Components

- TFChain v2.3.0
- ZOS v3.6.0
- TF Farmerbot v1.0.0
- TF Weblets v1.7.0
- TF Dashboard v1.4.0
- TF Gridclient v2.0.0
- TF Gridproxy v1.7.0
- Terraform v1.8.x
- RMB-RS v1.0.2
- TFChain-GraphQL v2.9.0

## Upgrades and Improvement Highlights

Below are some of the highlights of TFGrid v3.9.0 component upgrades and improvements.
Feel free to check [TFGrid v3.9.0 Project](https://github.com/orgs/threefoldtech/projects/172) for a more detailed overview of the TFGrid v3.9.0 release.


### RMB-RS v1.0.2

Reliable Message Bus Relay (RMB-RS) is a secure communication panel that allows bots to communicate together in a chat-like way. It makes it very easy to host a service or a set of functions to be used by anyone, even if your service is running behind NAT.

- Guarantee authenticity of the messages. You are always sure that the received message is authentic from the sender.
- End-to-end encryption support.
- Support for third-party hosted Relays. Anyone can host a Relay and people can use it safely since there is no way messages can be inspected while using e2e. That's similar to home servers by matrix.

See [Specifications](https://github.com/threefoldtech/zos_rmb/blob/main/docs/readme.md) for more information.

> Below is the list of the __Public Relay Addresses__ hosted by Threefold:

- Dev: wss://relay.dev.grid.tf
- QA: wss://relay.qa.grid.tf
- Test: wss://relay.test.grid.tf 
- Main: wss://relay.grid.tf 

__Impacted Clients:__

- [RMB-SDK-TS](https://github.com/threefoldtecharchive/rmb_sdk_ts/releases/tag/v1.1.1)
- [RMB-SDK-GO](https://github.com/threefoldtecharchive/rmb-sdk-go/releases/tag/v1.0.0)


### TFChain v2.3.0

On this release, we modified the twin objects on TFChain and removed the notion of an `IP`. We added 2 fields (`Relay` and `PK`) onto the twins.

- __Relay__: an RMB Relay Address which a client can connect to (See RMB changes)
- __PK__: a public key for an encryption key which can be used to encrypt messages on the Public Relay, if not set, traffic will be unencrypted.

__Impacted Clients:__

- [Grid3_Client_RS](https://github.com/threefoldtecharchive/grid3_client_rs/releases/tag/v0.2.0)

### TFChain-GraphQL v2.9.0

An important note for users, that multiple steps would be required to upgrade your TFChain-GraphQL into the latest v2.9.0 release, as described below:

1. Restart the ingester from scratch using the new config
2. Restart the processor from scratch using the new code

Please make sure all data is wiped before restarting both services.

### TF Famerbot v1.0.0

TF Farmerbot is a new component that aim as a power management solution that would allow farmer to setup to enable Wake-on-LAN mechanism on their farms.

## Other Component Changelogs

### TFChain v2.3.0

- Fixed locked balances
- Added extra field to twin for publickey
- Fixed serial number validation was blocking nodes from registration
- Added fixes on Farming policies on Testnet 
- Allow farms to Add public IP ranges
- Support power management and capacity planning
- Fixed TFT price on mainnet
- Reworked migrations
- Set node's last uptime when the node send an uptime event
- Disable twin deletion
- Bug fixes around data validations, and more.

Please follow [this milestone](https://github.com/threefoldtech/ledger_chain/milestone/11) for more.

### ZOS v3.6.0

- Support Switching dhcpd from udhcpd
- WOL support
- Power Management support
- Fixed gateways backend validation
- Added number of workloads and deployments to zos reported statistics
- Support the new RMB and Relay
- Provide clearer messaging during twin registration

Please follow [this milestone](https://github.com/threefoldtech/zos/milestone/12) for more details

### TF Farmerbot v1.0.0

- Initial Release
- Added Support for Power Management feature
- Added Support for Capacity Planning feature

### TF Weblets v1.7.0

- NEW Wordpress solution
- NEW Umbrel solution
- Added live button support
- Better error reporting mechanism
- Support Mnemonics field editing
- Removed flash messages after successfull deployment

Please follow [this milestone](https://github.com/threefoldtecharchive/grid_weblets/milestone/9) for more details

### TF Dashboard v1.4.0

- Public IP validation
- RenameD 'Swap' page to 'Bridge'
- Support setting Relay and Public Key
- Added filter by Country validation
- Filter farms by pricing policy support
- Resource pricing calculator discount distinction between shared and dedicated nodes

Please follow [this milestone](https://github.com/threefoldtecharchive/tfgrid_dashboard/milestone/13) for more details

### TF GridClient v2.0.0

- Added Support for RMB and Public Key of Twins
- Added Support for Farmerbot
- Added pricing calculator module
- Support service contracts
- Added size property to QSFS model
- HTTP server mode allows configuration file for user credentials
- Added fixes on 'Filter nodes by farmID' featue

### Terraform v1.8.x

- Added Support for RMB and RMB Relay
- Added Support for deployment using direct client 
- Added Support for parallel deployment of resources
- Expand resources and data sources documentation

Please follow [this milestone](https://github.com/threefoldtech/terraform-provider-grid/milestone/16) for more details

## RMB v1.0.2

The new version of RMB written in Rust

- Added Federation support
- Added Signing and end-to-end encryption
- RMB-Peer for compatibility
- Added Ratelimiting support

## TFGrid Proxy v1.7.0

- Removed the proxying features, obsoleted by the new RMB.

Please follow [this milestone](https://github.com/threefoldtecharchive/tfgridclient_proxy/milestone/6) for more details



