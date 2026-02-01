---
title: "Cloud Pricing Compare"
sidebar_position: 388
---

> **Last updated:** February 2026. Cloud pricing changes frequently — refer to provider websites for the latest rates. Hetzner prices converted using 1 EUR ≈ 1.18 USD.

## Introduction

We compare ThreeFold cloud pricing with major cloud providers. The information here can be subject to change and might not reflect current market prices at the time of reading. Always check the provider links for up-to-date pricing.

For details on ThreeFold pricing tiers and staking discounts, see the [Pricing Overview](./pricing.mdx) page.

## ThreeFold Cloud Units

| Cloud Unit | Description | USD/month (no discount) | USD/month (Gold 60% discount) |
| --- | --- | --- | --- |
| Compute Unit (CU) | 2 vCPU, 4 GB memory, 50 GB storage | $22.00 | $8.80 |
| Storage Unit (SU) | 1 TB of net usable storage | $14.00 | $5.60 |

## Compute Comparison

The following table compares the cost of resources equivalent to **1 CU** (2 vCPU, 4 GB RAM) across providers. ThreeFold pricing shown with Gold staking discount (60%).

| Provider | Instance | vCPU | RAM | Monthly Price | Source |
| --- | --- | --- | --- | --- | --- |
| **Hetzner Cloud** | CX22 | 2 (shared) | 4 GB | ~$4.47 | [Hetzner Cloud](https://www.hetzner.com/cloud/) |
| **ThreeFold** | 1 CU (Gold) | 2 | 4 GB | ~$8.80 | [TF Pricing](./pricing.mdx) |
| **DigitalOcean** | Basic Droplet | 2 (shared) | 4 GB | ~$20.00 | [DigitalOcean Pricing](https://www.digitalocean.com/pricing/droplets) |
| **Google Cloud** | e2-medium | 2 (shared) | 4 GB | ~$24.46 | [GCP Pricing](https://cloud.google.com/compute/all-pricing) |
| **AWS** | t3.medium | 2 (burstable) | 4 GB | ~$30.37 | [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/on-demand/) |
| **Microsoft Azure** | Standard B2s | 2 (burstable) | 4 GB | ~$30.37 | [Azure Pricing](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/) |

> **Note:** Major cloud providers charge additional fees for egress (data transfer out), storage, and public IP addresses. ThreeFold pricing includes 50 GB of storage per CU. Hetzner Cloud CX22 includes 20 TB of traffic. These are on-demand prices — reserved instances and committed-use discounts from major providers can lower costs.

## Storage Comparison

The following table compares the cost of **1 TB of storage** (equivalent to 1 SU) across providers. ThreeFold pricing shown with Gold staking discount (60%).

| Provider | Product | 1 TB/month | Source |
| --- | --- | --- | --- |
| **ThreeFold** | 1 SU (Gold) | ~$5.60 | [TF Pricing](./pricing.mdx) |
| **Microsoft Azure** | Blob Storage (Hot) | ~$18.43 | [Azure Blob Pricing](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/) |
| **DigitalOcean** | Spaces | ~$20.48 | [DO Spaces Pricing](https://www.digitalocean.com/pricing/spaces-object-storage) |
| **Google Cloud** | Cloud Storage (Standard) | ~$20.48 | [GCP Storage Pricing](https://cloud.google.com/storage/pricing) |
| **AWS** | S3 (Standard) | ~$23.55 | [S3 Pricing](https://aws.amazon.com/s3/pricing/) |

> **Note:** Cloud storage providers charge additional fees for API requests and egress. Cheaper archival tiers are available from all providers but have retrieval delays or fees. ThreeFold storage is net usable capacity with built-in redundancy.

## Hetzner Dedicated Server Comparison

[Hetzner](https://www.hetzner.com/) dedicated servers are commonly used for ThreeFold farming. The table below shows current AX-line pricing for context.

| Model | CPU | RAM | NVMe Storage | USD/month (excl. VAT) |
| --- | --- | --- | --- | --- |
| AX41-NVMe | AMD Ryzen 5 3600 (6-core) | 64 GB DDR4 | 2 x 512 GB | ~$44 |
| AX42 | AMD Ryzen 7 PRO 8700GE (8-core) | 64 GB DDR5 | 2 x 512 GB | ~$54 |
| AX52 | AMD Ryzen 7 7700 (8-core) | 64 GB DDR5 | 2 x 1 TB | ~$76 |
| AX102 | AMD Ryzen 9 7950X3D (16-core) | 128 GB DDR5 | 2 x 1.92 TB | ~$123 |

All models include unlimited traffic and a 1 Gbit/s connection. For the latest prices, see the [Hetzner AX Server Matrix](https://www.hetzner.com/dedicated-rootserver/matrix-ax/) and [Hetzner Server Auction](https://www.hetzner.com/sb/).

> **Note:** When comparing, keep in mind that ThreeFold pricing is for decentralized, peer-to-peer cloud capacity. Traditional providers like Hetzner offer managed infrastructure with different trade-offs (centralization, SLAs, locations).

For more information about running a ThreeFold node on Hetzner, see the [Cloud Provider Farming](../../../documentation/farmers/farming_optimization/cloud_provider_farming) guide.
