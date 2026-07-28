---
title: "Performance Monitor Package"
sidebar_position: 146
---

## Overview

The `perf` package is a performance monitor in `zos` nodes. it schedules tasks, cache their results and allows retrieval of these results through `RMB` calls.

## Flow

1. The `perf` monitor is started by the `noded` service in zos.
2. Tasks are registered with a schedule in the new monitor.
3. A bus handler is opened to allow result retrieval.

## Node Initialization Check

To ensure that the node always has a test result available, a check is performed on node startup for all the registered tasks, if a task doesn't have any stored result, it will run immediately without waiting for the next scheduled time.

## Scheduling

- Tasks are scheduled using a 6 fields cron format. this format provides flexibility to define time, allowing running tasks periodically or at specific time.

- Each task has a jitter which is the maximum number of seconds the task could sleep before it runs, this happens to prevent all tests ending up running at exactly the same time. So, for example, if a task is scheduled to run at `06:00` and its jitter is `10`, it is expected to run anywhere between `06:00` and `06:10`.

## RMB Commands

- `zos.perf.get`:

  - Payload: a payload type that contains the name of the test

    ```go
    type Payload struct {
      Name string
    }
    ```

    Possible values:

    - `"public-ip-validation"`
    - `"cpu-benchmark"`
    - `"iperf"`

  - Return: a single task result.

  - Possible Error: `ErrResultNotFound` if no result is stored for the given task.

- `zos.perf.get_all`:

  - Return: all stored results

The rmb direct client can be used to call these commands. check the [example](https://github.com/threefoldtech/zos_sdk_go/blob/development/rmb-sdk-go/examples/rpc_client/main.go)

## Caching

Results are stored in a Redis server running on the node.

The key in redis is the name of the task prefixed with the word `perf`.
The value is an instance of `TaskResult` struct contains:

- Name of the task
- Timestamp when the task was run
- A brief description about what the task do
- The actual returned result from the task

Notes:

- Storing results by a key ensures each new result overrides the old one, so there is always a single result for each task.
- Storing results prefixed with `perf` eases retrieving all the results stored by this module.

## Registered Tests

- [Public IP Validation](./publicips.md)
- [CPUBenchmark](./cpubench.md)
- [IPerf](./iperf.md)
- [Health Check](./healthcheck.md)

## Test Suite

Go to [this link](https://app.testlodge.com/a/26076/projects/40893/suites/234919) for a test suite covering the test cases for the performance testing.