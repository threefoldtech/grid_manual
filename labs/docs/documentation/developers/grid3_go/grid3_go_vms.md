---
title: "Deploy Multiple VMs"
sidebar_position: 92
---



## Introduction

We show how to deploy multiple VMs with the Go client.

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
    freeSRU := uint64(2)
    status := "up"
    filter := types.NodeFilter {
        FreeMRU: &freeMRU,
        FreeSRU: &freeSRU,
        Status: &status,
    }
    nodeIDs, err := deployer.FilterNodes(tfPluginClient.GridProxyClient, filter)
    nodeID1 := uint32(nodeIDs[0].NodeID)
    nodeID2 := uint32(nodeIDs[1].NodeID)

    // Create a new network to deploy
    network := workloads.ZNet{
        Name:        "newNetwork",
        Description: "A network to deploy",
        Nodes:       []uint32{nodeID1, nodeID2},
        IPRange: gridtypes.NewIPNet(net.IPNet{
            IP:   net.IPv4(10, 1, 0, 0),
            Mask: net.CIDRMask(16, 32),
        }),
        AddWGAccess: true,
    }

    // Create new VMs to deploy
    vm1 := workloads.VM{
        Name:       "vm1",
        Flist:      "https://hub.grid.tf/tf-official-apps/base:latest.flist",
        CPU:        2,
        PublicIP:   true,
        Planetary:  true,
        Memory:     1024,
        RootfsSize: 20 * 1024,
        Entrypoint: "/sbin/zinit init",
        EnvVars: map[string]string{
            "SSH_KEY": publicKey,
        },
        IP:          "10.20.2.5",
        NetworkName: network.Name,
    }
    vm2 := workloads.VM{
        Name:       "vm2",
        Flist:      "https://hub.grid.tf/tf-official-apps/base:latest.flist",
        CPU:        2,
        PublicIP:   true,
        Planetary:  true,
        Memory:     1024,
        RootfsSize: 20 * 1024,
        Entrypoint: "/sbin/zinit init",
        EnvVars: map[string]string{
            "SSH_KEY": publicKey,
        },
        IP:          "10.20.2.6",
        NetworkName: network.Name,
    }

    // Deploy the network first
    err = tfPluginClient.NetworkDeployer.Deploy(ctx, &network)

    // Load the network using the state loader
    // this loader should load the deployment as json then convert it to a deployment go object with workloads inside it
    networkObj, err := tfPluginClient.State.LoadNetworkFromGrid(network.Name)

    // Deploy the VM deployments
    dl1 := workloads.NewDeployment("vm1", nodeID1, "", nil, network.Name, nil, nil, []workloads.VM{vm1}, nil)
    dl2 := workloads.NewDeployment("vm2", nodeID2, "", nil, network.Name, nil, nil, []workloads.VM{vm2}, nil)
    err = tfPluginClient.DeploymentDeployer.BatchDeploy(ctx, []*workloads.Deployment{&dl1, &dl2})

    // Load the VMs using the state loader
    vmObj1, err := tfPluginClient.State.LoadVMFromGrid(nodeID1, vm1.Name, dl1.Name)
    vmObj2, err := tfPluginClient.State.LoadVMFromGrid(nodeID2, vm2.Name, dl2.Name)

    // Print the VMs Yggdrasil IP
    fmt.Println(vmObj1.YggIP)
    fmt.Println(vmObj2.YggIP)

    // Cancel the VM deployments
    err = tfPluginClient.DeploymentDeployer.Cancel(ctx, &dl1)
    err = tfPluginClient.DeploymentDeployer.Cancel(ctx, &dl2)

    // Cancel the network
    err = tfPluginClient.NetworkDeployer.Cancel(ctx, &network)
}

```

Running this code should result in two VMs deployed on two separate nodes while being on the same network and you should see an output like this:

```bash
300:e9c4:9048:57cf:f4e0:2343:f891:6037
300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f
```
