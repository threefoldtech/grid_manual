---
title: "Deploy Kubernetes"
sidebar_position: 94
---



## Introduction

We show how to deploy a Kubernetes cluster with the Go client.

## Example

```go
import (
    "fmt"
    "net"

    "github.com/threefoldtech/zos_sdk_go/grid-client/deployer"
    "github.com/threefoldtech/zos_sdk_go/grid-client/workloads"
    "github.com/threefoldtech/zos_sdk_go/grid-proxy/pkg/types"
    "github.com/threefoldtech/zos/pkg/gridtypes"
)

func main() {

    // Create Threefold plugin client
    tfPluginClient, err := deployer.NewTFPluginClient(mnemonics, "sr25519", network, "", "", "", 0, true)

    // Get a free node to deploy
    freeMRU := uint64(1)
    freeSRU := uint64(1)
    status := "up"
    filter := types.NodeFilter{
        FreeMRU: &freeMRU,
        FreeSRU: &freeSRU,
        Status:  &status,
    }
    nodeIDs, err := deployer.FilterNodes(tfPluginClient.GridProxyClient, filter)
    masterNodeID := uint32(nodeIDs[0].NodeID)
    workerNodeID1 := uint32(nodeIDs[1].NodeID)
    workerNodeID2 := uint32(nodeIDs[2].NodeID)

    // Create a new network to deploy
    network := workloads.ZNet{
        Name:        "newNetwork",
        Description: "A network to deploy",
        Nodes:       []uint32{masterNodeID, workerNodeID1, workerNodeID2},
        IPRange: gridtypes.NewIPNet(net.IPNet{
            IP:   net.IPv4(10, 1, 0, 0),
            Mask: net.CIDRMask(16, 32),
        }),
        AddWGAccess: true,
    }

    // Create master and worker nodes to deploy
    master := workloads.K8sNode{
        Name:      "master",
        Node:      masterNodeID,
        DiskSize:  1,
        CPU:       2,
        Memory:    1024,
        Planetary: true,
        Flist:     "https://hub.grid.tf/tf-official-apps/threefoldtech-k3s-latest.flist",
    }

    worker1 := workloads.K8sNode{
        Name:     "worker1",
        Node:     workerNodeID1,
        DiskSize: 1,
        CPU:      2,
        Memory:   1024,
        Flist:    "https://hub.grid.tf/tf-official-apps/threefoldtech-k3s-latest.flist",
    }

    worker2 := workloads.K8sNode{
        Name:     "worker2",
        Node:     workerNodeID2,
        DiskSize: 1,
        Flist:    "https://hub.grid.tf/tf-official-apps/threefoldtech-k3s-latest.flist",
        CPU:      2,
        Memory:   1024,
    }
  
    k8sCluster := workloads.K8sCluster{
        Master:      &master,
        Workers:     []workloads.K8sNode{worker1, worker2},
        Token:       "tokens",
        SSHKey:      publicKey,
        NetworkName: network.Name,
    }

    // Deploy the network first
    err = tfPluginClient.NetworkDeployer.Deploy(ctx, &network)

    // Deploy the k8s cluster
    err = tfPluginClient.K8sDeployer.Deploy(ctx, &k8sCluster)

    // Load the k8s cluster
    k8sClusterObj, err := tfPluginClient.State.LoadK8sFromGrid([]uint32{masterNodeID, workerNodeID1, workerNodeID2}, master.Name)

    // Print master node Yggdrasil IP
    fmt.Println(k8sClusterObj.Master.YggIP)

    // Cancel the VM deployment
    err = tfPluginClient.K8sDeployer.Cancel(ctx, &k8sCluster)

    // Cancel the network deployment
    err = tfPluginClient.NetworkDeployer.Cancel(ctx, &network)
}

```

You should see an output like this:

```bash
300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f
```
