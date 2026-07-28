---
title: "Quantum Safe Filesystem"
sidebar_position: 249
---





## Introduction

Quantum Storage is a FUSE filesystem that uses mechanisms of forward error correction (Reed Solomon codes) to make sure data (files and metadata) are stored in multiple remote places in a way that we can afford losing x number of locations without losing the data. 

The aim is to support unlimited local storage with remote backends for offload and backup which cannot be broken, even by a quantum computer.

## QSFS Workload Parameters and Documentation

A complete list of QSFS workload parameters can be found [here](https://github.com/threefoldtech/terraform-provider-grid/blob/development/docs/resources/deployment.md#nested-schema-for-qsfs).

The [quantum-storage](https://github.com/threefoldtech/qss_quantum_storage) repo contains a more thorough description of QSFS operation.