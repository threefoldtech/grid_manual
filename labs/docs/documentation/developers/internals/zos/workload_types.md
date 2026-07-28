---
title: "Workload Types"
sidebar_position: 139
---

## Introduction

Each workload has a type which is associated with some data. We present here the different types of workload associated with Zero-OS.

## Virtual Machine

### `network` type
Private network can span multiple nodes at the same time. Which means workloads (`VMs`) that live (on different node) but part of the same virtual network can still reach each other over this `private` network.

If one (or more) nodes are `public access nodes` you can also add your personal laptop to the nodes and be able to reach your `VMs` over `wireguard` network.

In the simplest form a network workload consists of:
- network range
- sub-range available on this node
- private key
- list of peers
  - each peer has public key
  - sub-range

Full network definition can be found [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/network.go)

### `ip` type
The IP workload type reserves an IP from the available contract IPs list. Which means on contract creation the user must specify number of public IPs it needs to use. The contract then will allocate this number of IPs from the farm and will kept on the contract.

When the user then add the IP workload to the deployment associated with this contract, each IP workload will pick and link to one IP from the contract.

In minimal form, `IP` workload does not require any data. But in reality it has 2 flags to pick which kind of public IP do you want

- `ipv4` (`bool`): pick one from the contract public Ipv4
- `ipv6` (`bool`): pick an IPv6 over SLAAC. Ipv6 are not reserved with a contract. They are basically free if the farm infrastructure allows Ipv6 over SLAAC.

Full `IP` workload definition can be found [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/ipv4.go)

### `zmount` type
A `zmount` is a local disk that can be attached directly to a container or a virtual machine. `zmount` only require `size` as input as defined [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/zmount.go) this workload type is only utilized via the `zmachine` workload.

### `zmachine` type

`zmachine` is a unified container/virtual machine type. This can be used to start a virtual machine on a `zos` node give the following:
- `flist`, this what provide the base `vm` image or container image.
  - the `flist` content is what changes the `zmachine` mode. An `flist` built from a docker image or has files, or executable binaries will run in a container mode. `ZOS` will inject it's own `kernel+initramfs` to run the workload and kick start the defined `flist` `entrypoint`
- private network to join (with assigned IP)
- optional public `ipv4` or `ipv6`
- optional disks. But at least one disk is required in case running `zmachine` in `vm` mode, which is used to hold the `vm` root image.

For more details on all parameters needed to run a `zmachine` please refer to [`zmachine` data](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/zmachine.go)

#### Building your `flist`

Please refer to [this document](./manual.md) here about how to build an compatible `zmachine flist`

### `zlogs` type

Zlogs is a utility workload that allows you to stream `zmachine` logs to a remote location.

The `zlogs` workload needs to know what `zmachine` to stream logs of and also the `target` location to stream the logs to. `zlogs` uses internally the [`tailstream`](https://github.com/threefoldtech/grid_tailstream) so it supports any streaming url that is supported by this utility.

`zlogs` workload runs inside the same private network as the `zmachine` instance. Which means zlogs can stream logs to other `zmachines` that is running inside the same private network (possibly on different nodes).

For example, you can run [`logagg`](https://github.com/threefoldtech/logagg) which is a web-socket server that can work with `tailstream` web-socket protocol.

Check `zlogs` configuration [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/zlogs.go)

## Storage

### `zdb` type
`zdb` is a storage primitives that gives you a persisted key value store over RESP protocol. Please check [`zdb` docs](https://github.com/threefoldtech/0-db)

Please check [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/zdb/zdb.go) for workload data.

### `qsfs` type

`qsfs` short for `quantum safe file system` is a FUSE filesystem which aim to be able to support unlimited local storage with remote backend for offload and backup which cannot be broke even by a quantum computer. Please read about it [here](https://github.com/threefoldtech/qss_quantum_storage)

To create a `qsfs` workload you need to provide the workload type as [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/qsfsd/qsfs.go)

## Gateway

### `gateway-name-proxy` type

This create a proxy with the given name to the given backends. The `name` of the proxy must be owned by a name contract on the grid. The idea is that a user can reserve a name (i.e `example`). Later he can deploy a gateway work load with name `example` on any gateway node that points to specified backends. The name then is prefix by the gateway name. For example if the gateway domain is `gent0.freefarm.com` then your full QFDN is goint to be called `example.gen0.freefarm.com`

Full name-proxy workload data is defined [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/gw_name.go)

### `gateway-fqdn-proxy` type

This create a proxy with the given fqdn to the given backends. In this case the user then must configure his dns server (i.e name.com) to point to the correct node public IP.

Full name-proxy workload data is defined [here](https://github.com/threefoldtech/zos_base/blob/main/pkg/gridtypes/zos/gw_fqdn.go)
