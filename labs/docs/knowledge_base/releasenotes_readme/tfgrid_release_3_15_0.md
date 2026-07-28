---
title: "TFGrid v3.15.0"
sidebar_position: 363
---

# ThreeFold Grid v3.15.0 Release Note

## ZOS

- Mycelium upgrade 0.5.4 [#2398](https://github.com/threefoldtech/zos/issues/2398)
- ZDB upgrade 2.0.8 [#2348](https://github.com/threefoldtech/zos/issues/2348)
- Slowdown speed of retries in healthcheckers [#2380](https://github.com/threefoldtech/zos/issues/2380)
- Improve HDD errors on the ZUI [#2376](https://github.com/threefoldtech/zos/issues/2376)
- Add features call on ZOS [#2421](https://github.com/threefoldtech/zos/issues/2421)
- Add validation for workload's name length [#2368](https://github.com/threefoldtech/zos/issues/2368)
- Add `xattr` to virtiofsd [#2420](https://github.com/threefoldtech/zos/issues/2420)
- Fix network speed tests [#2325](https://github.com/threefoldtech/zos/issues/2325)
- Supporting multiple stacks in ZOS [#2372](https://github.com/threefoldtech/zos/issues/2372)
- ZOS can now run on cloud providers e.g Hetzner [#2378](https://github.com/threefoldtech/zos/issues/2378)
- Periodically update the node location [#2401](https://github.com/threefoldtech/zos/issues/2401)
- Fix reporting Read only disks [#2409](https://github.com/threefoldtech/zos/issues/2409)
- Controlled rollout process is established in ZOS [#2413](https://github.com/threefoldtech/zos/issues/2413)
- Introduce more stability by replacing the usage of MacVlans [#2403](https://github.com/threefoldtech/zos/issues/2403)
- Restriction of outgoing traffic (NOT DONE) [#2399](https://github.com/threefoldtech/zos/issues/2399)

## TFChain/GraphQL

This release introduce lots of stability and bugsquashing in TFChain/GraphQL.

- During the grace period, the NU consumption may be incorrectly accumulated [#994](https://github.com/threefoldtech/ledger_chain/issues/994)
- Certified capacity paid as DIY capacity [#991](https://github.com/threefoldtech/ledger_chain/issues/991)
- Refactor/remove lock balance logic in billing flow [#990](https://github.com/threefoldtech/ledger_chain/issues/990)
- Contract is not getting billed [#982](https://github.com/threefoldtech/ledger_chain/issues/982)
- What will happen to a rent contract on a grace period for an offline node [#979](https://github.com/threefoldtech/ledger_chain/issues/979)
- Misuse of balance lock [#969](https://github.com/threefoldtech/ledger_chain/issues/969)
- Error distributing cultivation rewards [#834](https://github.com/threefoldtech/ledger_chain/issues/834)
- Improve off-chain worker logic [#932](https://github.com/threefoldtech/ledger_chain/issues/932)
- Instrument billing logic to improve audibility and log all major steps [#989](https://github.com/threefoldtech/ledger_chain/issues/989)
- Replacing the locking mechanism with a more reliable system [#990](https://github.com/threefoldtech/ledger_chain/issues/990)

## Mycelium

- Desktop/Mobile applications [#1544](https://github.com/threefoldtech/grid_wiki/issues/1544)
- Stable 1.0.0 release [Milestone 0.9.0](https://github.com/threefoldtech/mycelium/issues?q=is%3Aissue+milestone%3A0.9.0+is%3Aclosed)

## grid-proxy

- Include GPU info in node response [#1144](https://github.com/threefoldtech/zos_sdk_go/issues/1144)
- Fix error when getting consumption for a newly created twin [#1186](https://github.com/threefoldtech/zos_sdk_go/issues/1186)
- Return `free_public_ips_count` in node reponse [#1160](https://github.com/threefoldtech/zos_sdk_go/issues/1160)
- Support farm public ips endpoint [#1067](https://github.com/threefoldtech/zos_sdk_go/issues/1067)
- Farms sorting by IPs [#1125](https://github.com/threefoldtech/zos_sdk_go/issues/1125)
- Added a filter for nodes that are rentable or rented by the user [#1078](https://github.com/threefoldtech/zos_sdk_go/issues/1078)
- Support features healthcheck that helps listing the features supported by the nodes [#1214](https://github.com/threefoldtech/zos_sdk_go/pull/1214)
- More strict healthcheck to filter up nodes [#891](https://github.com/threefoldtech/zos_sdk_go/issues/891)

## Farmerbot

- Farmerbot disclaimer [#1009](https://github.com/threefoldtech/zos_sdk_go/issues/1009)
- Improved validations for included, excluded and priority nodes [#1017](https://github.com/threefoldtech/zos_sdk_go/issues/1017)

## Terraform

- Rename mnemonics to mnemonic [#962](https://github.com/threefoldtech/terraform-provider-grid/issues/962)
- Use the same k8s master's flist for all of the workers [#964](https://github.com/threefoldtech/terraform-provider-grid/issues/964)
- Fix no sshkey path [#968](https://github.com/threefoldtech/terraform-provider-grid/issues/968)
- All of the examples has mycelium network now [#967](https://github.com/threefoldtech/terraform-provider-grid/issues/967)

## Pulumi

- Python support [#452](https://github.com/threefoldtech/grid_pulumi/issues/452)
- Javascript support [#453](https://github.com/threefoldtech/grid_pulumi/issues/453)
- Add mycelium to all of the examples [#483](https://github.com/threefoldtech/grid_pulumi/issues/483)
- Validations hardening [#14](https://github.com/threefoldtech/grid_pulumi/issues/14)
- Support ZOS4 [#517](https://github.com/threefoldtech/grid_pulumi/issues/517)

## sdk-go

- Support of multiple stacks per network [#1113](https://github.com/threefoldtech/zos_sdk_go/issues/1113)
- Support of ZOS4 deploymnets [#1213](https://github.com/threefoldtech/zos_sdk_go/issues/1213)
- Unify kubernetes flists [#1210](https://github.com/threefoldtech/zos_sdk_go/issues/1210)
- Harden the validation for deployment, disk, and network names [#1055](https://github.com/threefoldtech/zos_sdk_go/issues/1055)
- Harden the validation of workload fields [#1165](https://github.com/threefoldtech/zos_sdk_go/issues/1165)

## RFS

- Lightweight Flist server [#61](https://github.com/threefoldtech/rfs/issues/61)
- Flist Frontend [#67](https://github.com/threefoldtech/rfs/issues/67)
- Improve Dir store for performance [#52](https://github.com/threefoldtech/rfs/issues/52)
- Implement HTTP Store [#51](https://github.com/threefoldtech/rfs/issues/51)
- Support Syncing from on location to another e.g dir to S3
- Support tracking progress while packing flists [#69](https://github.com/threefoldtech/rfs/issues/69)

## Threefold Connect

- More native rewrite of the application
- Support of DAO
- Support of Light/dark modes
- KYC support

For a detailed view, please check the project [here](https://github.com/orgs/threefoldtech/projects/210/views/20).

## sdk-ts

- KYC support, the user needs to go through KYC to be able to deploy
- Monitring via Sentry integration [#3101](https://github.com/threefoldtech/zos_sdk_ts/issues/3101)
- Support of multiple stacks [#3078](https://github.com/threefoldtech/zos_sdk_ts/issues/3078)
- Enable SMTP settings in case of public IP of solutions [#2522](https://github.com/threefoldtech/zos_sdk_ts/issues/2522)
- Add last deployment date to the node card [#2718](https://github.com/threefoldtech/zos_sdk_ts/issues/2718)
- Sorting for Farms and Nodes tables [#1685](https://github.com/threefoldtech/zos_sdk_ts/issues/1685)
- Include bandwidth cost when doing price estimates [#3018](https://github.com/threefoldtech/zos_sdk_ts/issues/3018)
- Configure the timeout for poor internet/connectivity of the node [#3169](https://github.com/threefoldtech/zos_sdk_ts/issues/3169)
- Separately managed domains page [#3178](https://github.com/threefoldtech/zos_sdk_ts/issues/3178)
- Deleta All contracts button [#3056](https://github.com/threefoldtech/zos_sdk_ts/issues/3056)
- Use te same master flist in kubernetes for all of the newly added workers [#3320](https://github.com/threefoldtech/zos_sdk_ts/issues/3320)

> Note: Various bugfixes and UX rework can be checked in detail [here](https://github.com/orgs/threefoldtech/projects/210/views/4).