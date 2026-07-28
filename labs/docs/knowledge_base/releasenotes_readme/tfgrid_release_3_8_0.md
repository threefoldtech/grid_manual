---
title: "TFGrid v3.8.0"
sidebar_position: 370
---

# ThreeFold Grid v3.8.0 Release Note

Release Note of ThreeFold Grid v3.8.0.
Live on Testnet 02/02/2023

This release note includes updates, improvements and fixes of numerous grid components as described below:

## The Components

- TFChain v2.2.0
- ZOS v3.4.0
- TF Weblets v1.6.0
- TF Dashboard v1.3.0
- TFGrid Client v1.5.0
- TFGrid Proxy v1.6.5
- Terraform v1.6.0

## Upgrades and Improvements

### TFChain v2.2.0
- Added [Third Party Billing Services](https://github.com/threefoldtech/ledger_chain/blob/development/substrate-node/pallets/pallet-smart-contract/service_consumer_contract_flow.md), allowing defining contracts between TFChain users for a service and the billing.
- Reworked billing flow, see  [details here](https://github.com/threefoldtech/ledger_chain/issues/269).
- Infrastructure wise, we have integrated [Firesquid](https://docs.subsquid.io/), which is showing promising improvements in regards of the storage and data syncing.
- Added Bugfixes around data validations and improving migrations

### ZOS v3.4.0
This release was mainly focused on the stabilization of ZOS, Monitoring Support, upgrading components and fixing bugs as described below:
- Vector and Node-exporter support for [monitoring](https://metrics.grid.tf/) 
- Bugfixes / hardening around uptime reports, capacity reports and QSFS workloads cleanup
- Added fixes for Grace Period regression
- Added fixes for ZOS Nodes Recovery after Network Outages
- Uptime reports rework: allowing it to happen every 40 minutes, instead of evey 2 hours
- Added Grace Period Workload Regression fixes

[3.4 milestone](https://github.com/threefoldtech/zos/milestone/11) for more details

### TF Weblets v1.6.0
- Support [Algorand](https://www.algorand.com/) solution deployment 
- Simplified Weblet's Profile Manager
- Support [Mastodon](https://joinmastodon.org/) solution deployment
- Upgraded [Discourse](https://www.discourse.org/) solution deployment support
- Various bugfixes and [UI Improvements](https://github.com/orgs/threefoldtech/projects/172/views/6)

For more detailed information on this component release, please see [TF Weblets v1.6.0 Milestone](https://github.com/threefoldtecharchive/grid_weblets/milestone/10)

### TF Dashboard v1.3.0
- Fixed broken 'Filter by Farm ID'
- Added fixes on HRU Filter
- Added Validation function on recipient's TFT address 
- Added updates to sidebar icons 
- Improved new farm addition function
- Added node filters validations fix
- Support filtering nodes by farm name 
- Added Monitoring dashboard 

For more detailed information on this component release, please see [TF Dashboard v1.3.0 Milestone](https://github.com/threefoldtecharchive/tfgrid_dashboard/milestone/12)

### TFGrid Client 1.5.0
- Added ZLogs workload support
- Added documentation updates

### Terraform 1.6.0
- Capacity planning upgrade
- Added Kubernetes token validation function

## TFGrid Proxy v1.6.5
- Added fixes on dedicated nodes reservation
- Added fixes on TCP connection leaks 
- Added Swagger Docs fixes
- Added Updates to stats endpoint 
- Added new queries for total resources
- Added more parameters to /nodes enpoint for filter by twin_id and node_id

For more detailed information on this component release, please see [TFGrid Proxy v1.6.5 Milestone](https://github.com/threefoldtecharchive/tfgridclient_proxy/milestone/5)
