---
title: "Zlogs"
sidebar_position: 248
---





## Introduction

Zlogs is a utility that allows you to stream VM logs to a remote location. You can find the full description [here](https://github.com/threefoldtech/zos_base/tree/main/docs/manual/zlogs)

## Using Zlogs

In Terraform, a vm has a zlogs field, this field should contain a list of target URLs to stream logs to.

Valid protocols are: `ws`, `wss`, and `redis`.

For example, to deploy two VMs named "vm1" and "vm2", with one vm1 streaming logs to vm2, this is what main.tf looks like:
```
terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    }
  }
}

provider "grid" {
}

resource "grid_network" "net1" {
    nodes = [2, 4]
    ip_range = "10.1.0.0/16"
    name = "network"
    description = "some network description"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
  node = 2
  network_name = grid_network.net1.name
  ip_range = lookup(grid_network.net1.nodes_ip_range, 2, "")
  vms {
    name = "vm1" #streaming logs
    flist = "https://hub.grid.tf/tf-official-apps/base:latest.flist"
    entrypoint = "/sbin/zinit init"
    cpu = 2
    memory = 1024
    env_vars = {
      SSH_KEY = "PUT YOUR SSH KEY HERE"
    }
    zlogs = tolist([
      format("ws://%s:5000", replace(grid_deployment.d2.vms[0].computedip, "//.*/", "")),  
    ])
  }
}

resource "grid_deployment" "d2" {
  node = 4
  network_name = grid_network.net1.name
  ip_range = lookup(grid_network.net1.nodes_ip_range, 4, "")
  vms {
    name = "vm2" #receiving logs
    flist = "https://hub.grid.tf/tf-official-apps/base:latest.flist"
    cpu = 2 
    memory = 1024
    entrypoint = "/sbin/zinit init"
    env_vars = {
      SSH_KEY = "PUT YOUR SSH KEY HERE"
    }
    publicip = true
  }
}
```

At this point, two VMs are deployed, and vm1 is ready to stream logs to vm2.
But what is missing here is that vm1 is not actually producing any logs, and vm2 is not listening for incoming messages.

### Creating a server

- First, we will create a server on vm2. This should be a websocket server listening on port 5000 as per our zlogs definition in main.tf ```ws://%s:5000```.

- a simple python websocket server looks like this:
```
import asyncio
import websockets
import gzip


async def echo(websocket):
    async for message in websocket:
        data = gzip.decompress(message).decode('utf-8')
        f = open("output.txt", "a")
        f.write(data)
        f.close()

async def main():
    async with websockets.serve(echo, "0.0.0.0", 5000, ping_interval=None):
        await asyncio.Future()

asyncio.run(main())
```
- Note that incoming messages are decompressed since zlogs compresses any messages using gzip.
- After a message is decompressed, it is then appended to `output.txt`.

### Streaming logs

- Zlogs streams anything written to stdout of the zinit process on a vm. 
- So, simply running ```echo "to be streamed" 1>/proc/1/fd/1``` on vm1 should successfuly stream this message to the vm2 and we should be able to see it in `output.txt`.
- Also, if we want to stream a service's logs, a service definition file should be created in ```/etc/zinit/example.yaml``` on vm1 and should look like this:
```
exec: sh -c "echo 'to be streamed'"
log: stdout
```

