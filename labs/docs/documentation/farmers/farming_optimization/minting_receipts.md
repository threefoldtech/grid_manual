---
title: "Minting Receipts"
sidebar_position: 187
---



## Introduction

Once you have the receipt hash of your node minting, you can get the [minting report](../../dashboard/tfchain/tf_minting_reports) of your node.

## Access the Reports

- On the Dashboard, go to **TFChain** -> **TF Minting Reports**
- Enter your receipt hash
- Consult your minting report

## Available Information

The ThreeFold Alpha minting tool will present the following information for each minting receipt hash:

- Node Info: This contains the basic information in relation to your node.
  - Node ID
  - Farm Name and ID
  - Measured Uptime
- Node Resources: These resources are related to the [cloud units](../../../knowledge_base/cloud_toc/cloudunits) and the [resource units](../../../knowledge_base/cloud_toc/resource_units_calc_cloudunits).
  - CU
  - SU
  - NU
  - CRU
  - MRU
  - SRU
  - HRU
- TFT Farmed: This is the quantity of TFT farmed during the minting period.
- Payout Address: The payout address is the Stellar address you set to receive your farming rewards.

## TFT Farming Registration Price

Currently, minting is set at a TFT value of 0.08 USD. This TFT farming registration price (i.e. the TFT minting value) can be seen as a farming difficulty level. The higher this number is, the less TFT is minted for the same given node. This number is not related to the TFT market price and is currently fixed. 

The ThreeFold DAO can vote to change this number. For example, if the ThreeFold DAO decides to increase the TFT minting value to 0.10 USD, the farming difficulty would be increased by 25% (0.08 * 1.25 = 0.10). This updated TFT farming registration price would then affect all new nodes that are registered after the DAO vote is passed.

<!-- NOTE: This is removed from the new dashboard, but might be brought back.

## Introduction

You can easily consult minting receipts of all your 3Nodes on the ThreeFold Dashboard to get essential minting information of your 3Nodes and your ThreeFold farm. With your minting receipt hash, you can then query the ThreeFold Alpha minting tool for further minting information.

## Download Minting Receipts of Your Farm

You can download minting receipts of your whole farm directly on the ThreeFold Dashboard.

- On the [ThreeFold Dashboard](https://dashboard.grid.tf/), go to **TFChain** -> **TF Minting Reports**
- In the section **Your Farms**, on the left of your **Farm ID**, click on the down arrow button
- Click on **Download Minting Receipts**

## Download Minting Receipts of a 3Node

You can download minting receipts of a single 3Node directly on the ThreeFold Dashboard.

- On the [ThreeFold Dashboard](https://dashboard.grid.tf/), go to **Portal** -> **Farms**
- In the section **Your Farm Nodes**, on the left of your **Node ID**, click on the down arrow button
- Click on **Node Statistics**
- Click on **Download Node Receipt**

## Minting Receipts Information

The minting receipts contain the following information:

- Minting: <minting_receipt_hash>
- start: <start of minting period>
- end: <end of minting period>
- TFT: <TFT minted by the 3Node>
- Cloud Units: <3Node Resources>

## Alpha Minting Tool

You can query additional minting information by using the [TF Minting Reports tool on the Dashboard](https://dashboard.grid.tf/#/tf-chain/minting-reports/).

- Download the minting receipts of your farm or of a single 3Node
- Copy a minting receipt hash
- Open the ThreeFold Alpha Minting tool by clicking on **Minting** on the left-side [ThreeFold Dashboard](https://dashboard.grid.tf/) menu
- Paste the minting receipt hash

The ThreeFold Alpha minting tool will present the following information for each minting receipt hash:

- Node ID
- Farm Name
- Measured Uptime
- Node Resources
  - CU
  - SU
  - NU
  - CRU
  - MRU
  - SRU
  - HRU
- TFT Farmed
- Payout Address

-->