---
title: "TFGrid v3.0.0 Alpha-2"
sidebar_position: 376
---

# ThreeFold Release Notes TFGrid 3.0.0 Alpha 2 (Live on testnet)

## TFChain v1.0.0

- DAO Requests
	- Becoming council member
	- Becoming a validator node
	- Pricing changes
	- Upgrading tfchain
	- Changing farming rewards

## Admin Portal v3.0.1-rc1

- Terms and conditions support
- Fix reasking for activation when the balance reaches 0
- Show amount of bridge deposit/withdraw fee
- Get more TFT button when connected to devnet
 
## tfchain explorer v3.0.0-rc19

- certification type filter
- adding certification type to nodes
- add zos version to node details
- update map to reflect the selected node 
- UX fixes for filters and data sorting 
- include version of tfchain, explorer, grid proxy 
- showing available resources
- showing online / offline nodes
- showing number of available IPs in a farm 
- adding favicon
- statistics page improvements

## ZOS v3.0.4

- public IPv6 support
- Min rootfs for more than 1 CU = 2GB, and anything less will be 500MB  
- Mainnet image
- Fix IPv6 rules that broke SLAAC
- Update SRU calculation
- bug don't wait for QSFS shutdown
- Update traefik version
- Fixing crashes caused by slow disks
- Avoid lsblk blocking for QSFS
- Decommission on too many QSFS metric fetches failure
https://github.com/threefoldtech/zos/releases

## Terraform v0.1.20
- Support for public IPv6
- Support planetary option for k8s


## grid3_client_ts v1.0.3
- Cert type for nodes
- public IPv6 support
- TwinServer command to be used from other langauges


## Weblets v1.2.0

- Support peertube
- Support funkwhale
- Remove rootfs specification from machine
- Support adding/deleting workers in kubernetes
- Add more images ubuntu, alpine, centos
- Updating the balance periodically 
- Adding access for nodes by default for hidden nodes issues
- Resolving issues 

### detailed projects list

- `https://github.com/threefoldtecharchive/grid_weblets/projects/1`
- `https://github.com/threefoldtecharchive/grid_weblets/projects/4`
- `https://github.com/threefoldtecharchive/grid_weblets/projects/6`
- `https://github.com/threefoldtecharchive/grid_weblets/projects/6`
- `https://github.com/threefoldtecharchive/grid_weblets/projects/7`
- `https://github.com/threefoldtecharchive/grid_weblets/projects/8`

`https://github.com/threefoldtecharchive/grid_weblets/releases`

## QSFS

TODO

## gridproxy v1.0.0-rc8

- generic performance improvements
- reduce caching time
- enable CORS in version 
- include certification types in nodes
- fix regression on nodes query 
- 

## Known Issues 3.0.0 Alpha 2

Following list is incomplete but gives some issues to think about.

- Weblets limitations
- QSFS integration is a work in progress
- ZOS and SSD performance [issue](https://github.com/threefoldtech/zos/issues/1467)
- Threefold Connect having [issues](https://circles.threefold.me/project/test-tfgrid3/issue/52) 
- Docker & ZOS containers [differences](https://github.com/threefoldtech/zos/issues/1483)
- ZOS workloads upgrade [issue](https://github.com/threefoldtech/zos/issues/1425)
- Terraform projects [don't reflect in the weblets](https://github.com/threefoldtech/terraform-provider-grid/issues/146)
- Can't detach public IP from a VM and removing it from a contract [issue](https://github.com/threefoldtech/ledger_chain/issues/175), please note you can still create each in separate contracts.

# ThreeFold Release Notes TFGrid 3.0.0 Alpha 1 (Live on mainnet)

- [TFgrid 3.0 announcement](https://forum.threefold.io/t/announcement-of-tfgrid-3-0/1132)
- [Whats new in TFGrid 3.0](https://forum.threefold.io/t/what-is-new-in-tfgrid-3-0/1133)
- [Roadmap](https://circles.threefold.me/project/despiegk-product_tfgrid3_roadmap/wiki/home)
- 
## TFChain

- Staking support (as the moment of this writing it's only on devnet now)
- KeyValue store support
- Bridging tokens from stellar to tfchain
- Smart contract for IT 
- Billing 
- Consumption Reports
- Discounts support

## Admin Portal

- Creation of twins
- Bridge from and to Stellar
- Farm Management
 

## Tfchain explorer

- Nodes view
- Gateways listing
- Farms information
- Resources/utilization
- Better filtering


## ZOS
- zmachine support
- Integration with latest subtsrate client event types
- public ipv6 support in VMs
- planetary support in VMs 
- upgrade to new file system RFS
- support for QSFS
- support for gateways
- capacity reporting to the blockchain support
- Support of SR25519
- Improvements in .zosrc creation
- Safer mechanism for environment variables and init arguments
- improvments in cleaning unused mounts

`https://github.com/threefoldtech/zos/releases`

## Terraform
- Support ZMachine
- Support Kubernetes
- Support QSFS
- Support Capacity Planning
- Support Gateways


## grid3_client_ts
- Support ZMachine
- Support Kubernetes
- Support QSFS
- Support Capacity Planning
- Support Gateways


## Weblets

- Support Profile manager
- Support Virtual machine
- Support CapRover
- Support Kubernetes
`https://github.com/threefoldtecharchive/grid_weblets/releases`
- Capacity planning deployment

## QSFS

TODO


- [TFgrid 3.0 announcement](https://forum.threefold.io/t/announcement-of-tfgrid-3-0/1132)
- [Whats new in TFGrid 3.0](https://forum.threefold.io/t/what-is-new-in-tfgrid-3-0/1133)
- [Roadmap](https://circles.threefold.me/project/despiegk-product_tfgrid3_roadmap/wiki/home)

## Known Issues 3.0.0 Alpha 1

Following list is incomplete but gives some issues to think about.

- Weblets limitations
- Public IP6 [support](https://github.com/threefoldtech/zos/pull/1488) in ZOS
- QSFS integration is a work in progress
- ZOS and SSD performance [issue](https://github.com/threefoldtech/zos/issues/1467)
- Threefold Connect having [issues](https://circles.threefold.me/project/test-tfgrid3/issue/52) 
- Docker & ZOS containers [differences](https://github.com/threefoldtech/zos/issues/1483)
- ZOS workloads upgrade [issue](https://github.com/threefoldtech/zos/issues/1425)
- Terraform projects [don't reflect in the weblets](https://github.com/threefoldtech/terraform-provider-grid/issues/146)
- Can't detach public IP from a VM and removing it from a contract [issue](https://github.com/threefoldtech/ledger_chain/issues/175), please note you can still create each in separate contracts.
