---
title: "TFGrid v3.14.0"
sidebar_position: 364
---

# ThreeFold Grid v3.14.0 Release Note

## ZOS

- Stricter health checks for filtering nodes to deploy on. [#2153](https://github.com/threefoldtech/zos/issues/2153)
- Don't send uptime reports when the zos node can't resolve grid services. [#2213](https://github.com/threefoldtech/zos/issues/2213)
- Network tests improvements. [#2163](https://github.com/threefoldtech/zos/issues/2163)
- Exposing last deployment date. [#2213](https://github.com/threefoldtech/zos/issues/2213)
- Supporting compressed kernels (also now supported by newer version from cloudhypervisor). [#2236](https://github.com/threefoldtech/zos/issues/2236)
- Zui became more responsive. [#2263](https://github.com/threefoldtech/zos/issues/2263)
- Updating node info if the zos IP changed. [#2242](https://github.com/threefoldtech/zos/issues/2242)
- Display the right size in the microvm (not the full node disk size). [#2007](https://github.com/threefoldtech/zos/issues/2007)
- Tools to debug images/flists if they're bootable in zos. [#2233](https://github.com/threefoldtech/zos/issues/2233)
- Zos able to download/mount flists over mycelium IPs
- Zos to support zdb over mycelium IPs
- Support HDD only nodes

## TFChain/GraphQL
- Runtime upgrades
- Support of HDD only nodes. [#967](https://github.com/threefoldtech/ledger_chain/issues/967)
- More validation for farms IPs
- Improvements of indexing (tft price and farm policy)

## Grid Proxy
- Sorting/querying by prices. [#608](https://github.com/threefoldtech/zos_sdk_go/issues/608)
- Filters by number of gpus, region, ipv6 
- Options for encoding and decoding for rmbpeer. [#507](https://github.com/threefoldtech/zos_sdk_go/issues/507)
- Add farm name/ rentable / rented information to the responses. [#612](https://github.com/threefoldtech/zos_sdk_go/issues/612) [#639](https://github.com/threefoldtech/zos_sdk_go/issues/639)
- Filtering nodes by multiple statuses

## Farmerbot
- Improved capacity planning to wakeup nodes
- Allowing farmers to specify the priority to wakeup nodes

## Pulumi
- Support mycelium 
- Add more examples

## sdk-go
- Support volume workload