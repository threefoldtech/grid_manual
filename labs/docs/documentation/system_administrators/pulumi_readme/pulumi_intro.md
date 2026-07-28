---
title: "Introduction to Pulumi"
sidebar_position: 227
---



With Pulumi, you can express your infrastructure requirements using the languages you know and love, creating a seamless bridge between development and operations. Let's go!

## Introduction

[ThreeFold Grid](https://threefold.io) is a decentralized cloud infrastructure platform that provides developers with a secure and scalable way to deploy and manage their applications. It is based on a peer-to-peer network of nodes that are distributed around the world.

[Pulumi](https://www.pulumi.com/) is a cloud-native infrastructure as code (IaC) platform that allows developers to manage their infrastructure using code. It supports a wide range of cloud providers, including ThreeFold Grid. Consult the official [Pulumi documentation](https://www.pulumi.com/docs/) for more information.

The [Pulumi plugin for ThreeFold Grid](https://github.com/threefoldtech/grid_pulumi) provides developers with a way to deploy and manage their ThreeFold Grid resources using Pulumi. This means that developers can benefit from all of the features and benefits that Pulumi offers, such as cross-cloud support, type safety, preview and diff, and parallel execution -still in the works-.

Please note that the Pulumi plugin for ThreeFold Grid is not yet officially published. We look forward to your feedback on this project.

## Mycelium Network

Note that you can use the [Mycelium network](../mycelium_toc/mycelium_toc.md) to connect to your deployments. To do so, make sure that the Mycelium network is properly set up for the deployments. You can consult the different examples that include the Mycelium network to understand this further.

## Benefits of Using Pulumi

Here are some additional benefits of using the Pulumi plugin for ThreeFold Grid:

- Increased productivity: Pulumi allows developers to manage their infrastructure using code, which can significantly increase their productivity.
- Reduced errors: Pulumi's type safety and preview and diff features can help developers catch errors early, which can reduce the number of errors that occur in production.
- Improved collaboration: Pulumi programs can be shared with other developers, which can make it easier to collaborate on infrastructure projects.

The Pulumi plugin for ThreeFold Grid is a powerful tool that can be used to deploy and manage a wide range of ThreeFold Grid applications. It is a good choice for developers who want to manage their ThreeFold Grid infrastructure using code and benefit from all of the features and benefits that Pulumi offers.

## Declarative vs. Imperative Programming

Declarative programming and imperative programming are two different ways to write code. Declarative programming focuses on describing the desired outcome, while imperative programming focuses on describing the steps needed to achieve that outcome.

In the context of infrastructure as code (IaC), declarative programming allows you to describe your desired infrastructure state, and the IaC tool will figure out how to achieve it. Imperative programming, on the other hand, requires you to describe the steps needed to create and configure your infrastructure.

### Declaration Programming Example

Say I want an infrastructure of two virtual machines with X disks. The following would happen:

1. Connect to the backend services.
2. Send the requests to create the virtual machines.
3. Sign the requests.
4. Execute the requests in a careful order.

As you can see, the declarative code is much simpler and easier to read. It also makes it easier to make changes to your infrastructure, as you only need to change the desired state, and the IaC tool will figure out how to achieve it.

### Benefits of Declarative Programming in IaC

There are several benefits to using declarative programming in IaC:

- Simpler code: Declarative code is simpler and easier to read than imperative code. This is because declarative code focuses on describing the desired outcome, rather than the steps needed to achieve it.
- More concise code: Declarative code is also more concise than imperative code. This is because declarative code does not need to specify the steps needed to achieve the desired outcome.
- Easier to make changes: Declarative code makes it easier to make changes to your infrastructure. This is because you only need to change the desired state, and the IaC tool will figure out how to achieve it.
- More reliable code: Declarative code is more reliable than imperative code. This is because declarative code does not need to worry about the order in which the steps are executed. The IaC tool will take care of that.

We will be taking a look at a couple of examples, I'll be linking the source directory of the example and go through it, but first let's go through some concepts first

## Concepts

### Pulumi Project

A Pulumi project is any folder that contains a **Pulumi.yaml** file. When in a subfolder, the closest enclosing folder with a **Pulumi.yaml** file determines the current project. A new project can be created with pulumi new. A project specifies which runtime to use and determines where to look for the program that should be executed during deployments. Supported runtimes are nodejs, python, dotnet, go, java, and yaml.

### Project File

The **Pulumi.yaml** project file specifies metadata about your project. The project file must begin with a capitalized P, although either a **.yml** or **.yaml** extension will work.

A typical Pulumi.yaml file looks like the following:

```yaml
name: my-project
runtime:
    name: go
    options:
        binary: mybinary
description: A minimal Go Pulumi program
```

or

```yaml
name: my-project
runtime: yaml
resources:
  bucket:
    type: aws:s3:Bucket

```

For more on project or project files, please check the [Pulumi documentation](https://www.pulumi.com/docs/concepts/projects/).

### Stacks

Every Pulumi program is deployed to a [stack](https://www.pulumi.com/docs/concepts/stack/). A stack is an isolated, independently configurable instance of a Pulumi program. Stacks are commonly used to denote different phases of development (such as development, staging, and production) or feature branches (such as feature-x-dev).

A project can have as many stacks as you need. By default, Pulumi creates a stack for you when you start a new project using the **pulumi new** command.

### Resources

Resources represent the fundamental units that make up your cloud infrastructure, such as a compute instance, a storage bucket, or a Kubernetes cluster.

All infrastructure resources are described by one of two subclasses of the Resource class. These two subclasses are:

- CustomResource: A custom resource is a cloud resource managed by a resource provider such as AWS, Microsoft Azure, Google Cloud, or Kubernetes.
- ComponentResource: A component resource is a logical grouping of other resources that creates a larger, higher-level abstraction that encapsulates its implementation details.

Here's an example:

```yaml
resources:
  res:
    type: the:resource:Type
    properties: ...args
    options: ...options
```

## Pulumi Registry

You can visit the Pulumi registry to access the ThreeFold package [here](https://www.pulumi.com/registry/packages/threefold/).