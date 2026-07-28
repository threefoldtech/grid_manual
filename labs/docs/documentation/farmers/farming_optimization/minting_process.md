---
title: "Minting Process"
sidebar_position: 186
---

# Minting Process

Minting is based on blockchain data according to strict rules that are carried out by computers with humans involved only to check for errors and to sign the resulting transactions.

There is a human verification mechanism through multisignatures for calculations done on the data as stored in the blockchain. This explains the timing differences when it comes to the monthly farming rewards distribution, since enough people need to sign off.

The detailed minting process for V3 is as follow:

- TFChain, ThreeFold's blockchain, has all the details about capacity provided by the nodes.
- TFChain is used to track uptime.
- Zero-OS reports to TFChain.
- The code in [this repo](https://github.com/threefoldtech/ledger_minting) uses the information from the blockchain to calculate the TFT to be minted.
- A proof of what needs to be minted and why is created. This proof is then sent to our guardians.
- The guardians need to double check the execution and the minting report. This is like a human check on the automated process.
- The guardians need to sign. Only when consensus is achieved the minting as suggested will happen. This allows human to check the code.

It is important to understant that TFChain tracks the capacity and uptime and is the source for the minting.

> Note: Additional auditing code will be added in V4 (i.e. special code generated at runtime for verification) using security primitives on motherboards.

For more information on the minting periods, read [this section](./minting_periods).