---
title: "Introduction"
sidebar_position: 359
---





## Introduction

From TFGrid 3.0, the 'Smart Contract for IT' concept for reserving capacity is fully decentralized and runs on TF-Chain, the ThreeFold blockchain infrastructure on Parity Substrate. 

## Architecture

Two main components play a role in achieving a decentralised consensus between a user and a farmer.

- TFGrid Substrate Database Pallet TFGrid
- TFGrid Smart Contract

The TF-Grid Substrate Database will keep a record of all Entities, Twins, Nodes and Farmers in the TF-Grid network. This makes it easy to integrate the Smart Contract on Substrate as well since we can read from that storage in runtime.

![](./img/smartcontract3_flow.jpg)

The Smart Contract on Substrate works as following:

## 1: To deploy a workload, the user interacts with this smart contract pallet and calls: `create_contract` with the input being:

The user must instruct his twin to create the contract. *This program containing his digital twin is yet to be defined.* A contract will always belong to a twin and to a node. This relationship is important because only the user's twin and target node's twin can update the contract.

```js
contract = {
    version: contractVersion,
    contract_id: contractID,
    twin_id: NumericTwinID for the contract,
    // node_address is the node address.
    node_id: NumericNodeID
    // data is the encrypted deployment body. This encrypted the deployment with the **USER** public key. So only the user can read this data later on (or any other key that he keeps safe).
    // this data part is read only by the user and can actually hold any information to help him reconstruct his deployment or can be left empty.
    data: encrypted(deployment) // optional
    // hash: is the deployment predictable hash. the node must use the same method to calculate the challenge (bytes) to compute this same hash.
    //used for validating the deployment from node side.
    deployment_hash: hash(deployment),
    // public_ips: number of ips that need to be reserved by the contract and used by the deployment
    public_ips: 0,
    state: ContractState (created, deployed),
    public_ips_list: list of public ips on this contract
}
```

The `node_id` field is the target node's ID. A user can do lookup for a node to find its corresponding ID.

The workload data is encrypted by the user and contains the workload definition for the node.

If `public_ips` is specified, the contract will reserve the number of public ips requested on the node's corresponding farm. If there are not enough ips available an error will be returned. If the contract is canceled by either the user or the node, the IPs for that contract will be freed.

This pallet saves this data to storage and returns the user a `contract_id`.

## 2: The user sends the contractID and workload through the RMB to the destination Node.

The Node reads from the [RMB](https://github.com/threefoldtecharchive/rmb_archive) and sees a deploy command, it reads the contractID and workload definition from the payload.
It decodes the workload and reads the contract from chain using the contract ID, the Node will check if the user that created the contract and the deployment hash on the contract is the same as what the Node receives over RMB. If all things check out, the Node deploys the workload.

## 3: The Node sends consumption reports to the chain

The Node periodically sends consumption reports back to the chain for each deployed contract. The chain will compute how much is being used and will bill the user based on the farmers prices (the chain can read these prices by quering the farmers storage and reading the pricing data). See [PricingPolicy](https://github.com/threefoldtecharchive/tfchain_pallets/blob/03a5823ce79200709d525ec182036b47a60952ef/pallet-tfgrid/src/types.rs#L120).

A report looks like:

json
```
{
	"contract_id": contractID,
    "timestamp": "timestampOfReport",
	"cru": cpus,
	"sru": ssdInBytes,
	"hru": hddInBytes,
	"mru": memInBytes,
	"nru": trafficInBytes
}
```

The node can call `add_reports` on this module to submit reports in batches.

Usage of SU, CU and NU will be computed based on the prices and the rules that Threefold set out for cloud pricing.

Billing will be done in Database Tokens and will be send to the corresponding farmer. If the user runs out of funds the chain will set the contract state to `cancelled` or it will be removed from storage. The Node needs to act on this 'contract cancelled' event and decommission the workload.

The main currency of this chain. For more information, see the [ThreeFold Token](../../../documentation/threefold_token) documentation.

## Notes

Sending the workloads encrypted to the chain makes sure that nobody except the user can read his deployment data. It also facilitates a way for the user to recreate his workload data from the chain.