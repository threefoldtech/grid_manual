---
title: "Deploy Gateways"
sidebar_position: 93
---



## Introduction

After [deploying a VM](./grid3_go_vm) you can deploy Gateways to further expose your VM.

## Gateway Name

This generates a FQDN for your VM.

## Example

```go
import (
    "fmt"

    "github.com/threefoldtech/zos_sdk_go/grid-client/deployer"
    "github.com/threefoldtech/zos_sdk_go/grid-client/workloads"
    "github.com/threefoldtech/zos_sdk_go/grid-proxy/pkg/types"
    "github.com/threefoldtech/zos/pkg/gridtypes/zos"
)

func main() {

    // Create Threefold plugin client
    tfPluginClient, err := deployer.NewTFPluginClient(mnemonics, "sr25519", network, "", "", true, false)

    // Get a free node to deploy
    domain := true
    status := "up"
    filter := types.NodeFilter{
        Domain: &domain,
        Status: &status,
    }
    nodeIDs, err := deployer.FilterNodes(tfPluginClient.GridProxyClient, filter)
    nodeID := uint32(nodeIDs[0].NodeID)

    // Create gateway to deploy
    gateway := workloads.GatewayNameProxy{
        NodeID:         nodeID,
        Name:           "mydomain",
        Backends:       []zos.Backend{"http://[300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f]:8080"},
        TLSPassthrough: true,
    }
    err = tfPluginClient.GatewayNameDeployer.Deploy(ctx, &gateway)

    gatewayObj, err := tfPluginClient.State.LoadGatewayNameFromGrid(nodeID, gateway.Name, gateway.Name)
    fmt.Println(gatewayObj.FQDN)
}

```

This deploys a Gateway Name Proxy that forwards requests to your VM. You should see an output like this:

```bash
mydomain.gent01.dev.grid.tf
```

## Gateway FQDN

In case you have a FQDN already pointing to the node, you can expose your VM using Gateway FQDN.

## Example

```go
import (
    "fmt"

    "github.com/threefoldtech/zos_sdk_go/grid-client/deployer"
    "github.com/threefoldtech/zos_sdk_go/grid-client/workloads"
    "github.com/threefoldtech/zos/pkg/gridtypes/zos"
)

func main() {

    // Create Threefold plugin client
    tfPluginClient, err := deployer.NewTFPluginClient(mnemonics, "sr25519", network, "", "", "", 0, true)

    // Create gateway to deploy
    gateway := workloads.GatewayFQDNProxy{
        NodeID:         14,
        Name:           "mydomain",
        Backends:       []zos.Backend{"http://[300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f]:8080"},
        FQDN:           "my.domain.com",
        TLSPassthrough: true,
    }
    err = tfPluginClient.GatewayFQDNDeployer.Deploy(ctx, &gateway)

    gatewayObj, err := tfPluginClient.State.LoadGatewayFQDNFromGrid(nodeID, gateway.Name, gateway.Name)
}

```

This deploys a Gateway FQDN Proxy that forwards requests to from node 14 public IP to your VM.
