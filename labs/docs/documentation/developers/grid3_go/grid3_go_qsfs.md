---
title: "Deploy a QSFS"
sidebar_position: 95
---



## Introduction

We show how to deploy QSFS workloads with the Go client.

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
    filter := types.NodeFilter{
        FreeMRU: &freeMRU,
        FreeSRU: &freeSRU,
        Status:  &status,
    }
    nodeIDs, err := deployer.FilterNodes(tfPluginClient.GridProxyClient, filter)
    nodeID := uint32(nodeIDs[0].NodeID)

    // Create data and meta ZDBs
    dataZDBs := []workloads.ZDB{}
    metaZDBs := []workloads.ZDB{}
    for i := 1; i <= DataZDBNum; i++ {
        zdb := workloads.ZDB{
            Name:        "qsfsDataZdb" + strconv.Itoa(i),
            Password:    "password",
            Public:      true,
            Size:        1,
            Description: "zdb for testing",
            Mode:        zos.ZDBModeSeq,
        }
        dataZDBs = append(dataZDBs, zdb)
    }

    for i := 1; i <= MetaZDBNum; i++ {
        zdb := workloads.ZDB{
            Name:        "qsfsMetaZdb" + strconv.Itoa(i),
            Password:    "password",
            Public:      true,
            Size:        1,
            Description: "zdb for testing",
            Mode:        zos.ZDBModeUser,
        }
        metaZDBs = append(metaZDBs, zdb)
    }

    // Deploy ZDBs
    dl1 := workloads.NewDeployment("qsfs", nodeID, "", nil, "", nil, append(dataZDBs, metaZDBs...), nil, nil)
    err = tfPluginClient.DeploymentDeployer.Deploy(ctx, &dl1)

    // result ZDBs
    resDataZDBs := []workloads.ZDB{}
    resMetaZDBs := []workloads.ZDB{}
    for i := 1; i <= DataZDBNum; i++ {
        res, err := tfPluginClient.State.LoadZdbFromGrid(nodeID, "qsfsDataZdb"+strconv.Itoa(i), dl1.Name)
        resDataZDBs = append(resDataZDBs, res)
    }
    for i := 1; i <= MetaZDBNum; i++ {
        res, err := tfPluginClient.State.LoadZdbFromGrid(nodeID, "qsfsMetaZdb"+strconv.Itoa(i), dl1.Name)
        resMetaZDBs = append(resMetaZDBs, res)
    }

    // backends
    dataBackends := []workloads.Backend{}
    metaBackends := []workloads.Backend{}
    for i := 0; i < DataZDBNum; i++ {
        dataBackends = append(dataBackends, workloads.Backend{
            Address:   "[" + resDataZDBs[i].IPs[1] + "]" + ":" + fmt.Sprint(resDataZDBs[i].Port),
            Namespace: resDataZDBs[i].Namespace,
            Password:  resDataZDBs[i].Password,
        })
    }
    for i := 0; i < MetaZDBNum; i++ {
        metaBackends = append(metaBackends, workloads.Backend{
            Address:   "[" + resMetaZDBs[i].IPs[1] + "]" + ":" + fmt.Sprint(resMetaZDBs[i].Port),
            Namespace: resMetaZDBs[i].Namespace,
            Password:  resMetaZDBs[i].Password,
        })
    }

    // Create a new qsfs to deploy
    qsfs := workloads.QSFS{
        Name:                 "qsfs",
        Description:          "qsfs for testing",
        Cache:                1024,
        MinimalShards:        2,
        ExpectedShards:       4,
        RedundantGroups:      0,
        RedundantNodes:       0,
        MaxZDBDataDirSize:    512,
        EncryptionAlgorithm:  "AES",
        EncryptionKey:        "4d778ba3216e4da4231540c92a55f06157cabba802f9b68fb0f78375d2e825af",
        CompressionAlgorithm: "snappy",
        Groups:               workloads.Groups{{Backends: dataBackends}},
        Metadata: workloads.Metadata{
            Type:                "zdb",
            Prefix:              "test",
            EncryptionAlgorithm: "AES",
            EncryptionKey:       "4d778ba3216e4da4231540c92a55f06157cabba802f9b68fb0f78375d2e825af",
            Backends:            metaBackends,
        },
    }

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

    vm := workloads.VM{
        Name:       "vm",
        Flist:      "https://hub.grid.tf/tf-official-apps/base:latest.flist",
        CPU:        2,
        Planetary:  true,
        Memory:     1024,
        Entrypoint: "/sbin/zinit init",
        EnvVars: map[string]string{
            "SSH_KEY": publicKey,
        },
        Mounts: []workloads.Mount{
            {DiskName: qsfs.Name, MountPoint: "/qsfs"},
        },
        NetworkName: network.Name,
    }    

    // Deploy the network first
    err = tfPluginClient.NetworkDeployer.Deploy(ctx, &network)

    // Deploy the VM/QSFS deployment
    dl2 := workloads.NewDeployment("qsfs", nodeID, "", nil, network.Name, nil, append(dataZDBs, metaZDBs...), []workloads.VM{vm}, []workloads.QSFS{qsfs})
    err = tfPluginClient.DeploymentDeployer.Deploy(ctx, &dl2)

    // Load the QSFS using the state loader
    qsfsObj, err := tfPluginClient.State.LoadQSFSFromGrid(nodeID, qsfs.Name, dl2.Name)

    // Load the VM using the state loader
    vmObj, err := tfPluginClient.State.LoadVMFromGrid(nodeID, vm.Name, dl2.Name)

    // Print the VM Yggdrasil IP
    fmt.Println(vmObj.YggIP)

    // Cancel the VM,QSFS deployment
    err = tfPluginClient.DeploymentDeployer.Cancel(ctx, &dl1)
    err = tfPluginClient.DeploymentDeployer.Cancel(ctx, &dl2)

    // Cancel the network deployment
    err = tfPluginClient.NetworkDeployer.Cancel(ctx, &network)
}
```

Running this code should result in a VM with QSFS deployed on an available node and get an output like this:

```bash
Yggdrasil IP: 300:e9c4:9048:57cf:6d98:42c6:a7bf:2e3f
```
