---
title: "Deploy a VM with GPU"
sidebar_position: 98
---



## Introduction

In this section, we explore how to deploy a virtual machine equipped with GPU. We deploy the VM using Go. The VM will be deployed on a 3Node with an available GPU.



## Example

```go
import (
    "context"
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
    freeMRU := uint64(2)
    freeSRU := uint64(20)
    status := "up"
    trueVal := true

    twinID := uint64(tfPluginClient.TwinID)
    filter := types.NodeFilter{
        FreeMRU: &freeMRU,
        FreeSRU: &freeSRU,
        Status:  &status,
        RentedBy: &twinID,
        HasGPU:   &trueVal,
    }
    nodeIDs, err := deployer.FilterNodes(tfPluginClient.GridProxyClient, filter)
    nodeID := uint32(nodeIDs[0].NodeID)

    // Get the available gpus on the node
    nodeClient, err := tfPluginClient.NcPool.GetNodeClient(tfPluginClient.SubstrateConn, nodeID)
    gpus, err := nodeClient.GPUs(ctx)

    // Create a new network to deploy
    network := workloads.ZNet{
        Name:        "newNetwork",
        Description: "A network to deploy",
        Nodes:       []uint32{nodeID},
        IPRange: gridtypes.NewIPNet(net.IPNet{
            IP:   net.IPv4(10, 1, 0, 0),
            Mask: net.CIDRMask(16, 32),
        }),
        AddWGAccess: true,
    }

    // Create a new disk to deploy
    disk := workloads.Disk{
        Name:   "gpuDisk",
        SizeGB: 20,
    }

    // Create a new VM to deploy
    vm := workloads.VM{
        Name:       "vm",
        Flist:      "https://hub.grid.tf/tf-official-apps/base:latest.flist",
        CPU:        2,
        PublicIP:   true,
        Planetary:  true,
        // Insert your GPUs' IDs here
        GPUs:       []zos.GPU{zos.GPU(gpus[0].ID)},
        Memory:     1024,
        RootfsSize: 20 * 1024,
        Entrypoint: "/sbin/zinit init",
        EnvVars: map[string]string{
            "SSH_KEY": publicKey,
        },
        Mounts: []workloads.Mount{
            {DiskName: disk.Name, MountPoint: "/data"},
        },
        IP:          "10.20.2.5",
        NetworkName: network.Name,
    }

    // Deploy the network first
    err = tfPluginClient.NetworkDeployer.Deploy(ctx, &network)

    // Deploy the VM deployment
    dl := workloads.NewDeployment("gpu", nodeID, "", nil, network.Name, []workloads.Disk{disk}, nil, []workloads.VM{vm}, nil)
    err = tfPluginClient.DeploymentDeployer.Deploy(ctx, &dl)

    // Load the VM using the state loader
    vmObj, err := tfPluginClient.State.LoadVMFromGrid(nodeID, vm.Name, dl.Name)

    // Print the VM Yggdrasil IP
    fmt.Println(vmObj.YggIP)

    // Cancel the VM deployment
    err = tfPluginClient.DeploymentDeployer.Cancel(ctx, &dl)

    // Cancel the network deployment
    err = tfPluginClient.NetworkDeployer.Cancel(ctx, &network)
}
```

Running this code should result in a VM with a GPU deployed on an available node. The output should look like this:

```bash
Yggdrasil IP: 300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f
```