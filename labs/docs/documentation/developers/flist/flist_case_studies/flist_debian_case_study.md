---
title: "Case Study: Debian 12"
sidebar_position: 134
---



## Introduction

For this tutorial, we will present a case study demonstrating how easy it is to create a new flist on the ThreeFold ecosystem. We will be creating a Debian Flist and we will deploy a micro VM on the ThreeFold Playground and access our Debian deployment. 

To do all this, we will need to create a Docker Hub account, create a Dockerfile, a docker image and a docker container, then convert the docker image to a Zero-OS flist. After all this, we will be deploying our Debian workload on the ThreeFold Playground. You'll see, it's pretty straightforward and fun to do.



### You Said Flist?

First, let's recall what an flist actually is and does. In short, an flist is a very effective way to deal with software data and the end result is fast deployment and high reliability.

In a flist, we separate the metadata from the data. The metadata is a description of what files are in that particular image. It's the data providing information about the app/software. Thanks to flist, the 3Node doesn't need to install a complete software program in order to run properly. Only the necessary files are installed. Zero-OS can read the metadata of a container and only download and execute the necessary binaries and applications to run the workload, when it is necessary.

Sounds great? It really is great, and very effective!

One amazing thing about the flist technology is that it is possible to convert any Docker image into an flist, thanks to the [ThreeFold Docker Hub Converter tool](https://hub.grid.tf/docker-convert). If this sounds complicated, fear not. It is very easy and we will show you how to proceed in this case study.



### Case Study Objective

The goal of this case study is to give you enough information and tools so that you can yourself build your own flist projects and deploy on the ThreeFold Grid.

This case study is not meant to show you all the detailed steps on creating an flist from scratch. We will instead start with some files templates available on the ThreeFold repository [tf-images](https://github.com/threefoldtech/zos_images). This is one of the many advantages of working with open-source projects: we can easily get inspiration from the already available codes of the many ThreeFold repositories and work our way up from there.



### The Overall Process

To give you a bird's view of the whole project, here are the main steps:

* Create the Docker image
* Push the Docker image to the Docker Hub
* Convert the Docker image to a Zero-OS flist
* Deploy a micro VM with the flist on the ThreeFold Playground



## Docker Image Creation

As we've said previously, we will not explore all the details of creating an flist from scratch. This would be done in a subsequent guide. For now, we want to take existing codes and work our way from there. This is not only quicker, but it is a good way to get to know the ThreeFold's ecosystem and repositories.

We will be using the code available on the [ThreeFold Github page](https://github.com/threefoldtech). In our case, we want to explore the repository [tf-images](https://github.com/threefoldtech/zos_images).

If you go on the subsection [tfgrid3](https://github.com/threefoldtech/zos_images/tree/development/tfgrid3), you can see many different flists available. In our case, we want to deploy the Debian Linux distribution. It is thus logic to try and find similar Linux distributions to take inspiration from.

For this case study, we draw inspiration from the [Ubuntu 22.04](https://github.com/threefoldtech/zos_images/tree/development/tfgrid3/ubuntu22.04) directory.

If we look at the Ubuntu 22.04 directory tree, this is what we get:

```
.
├── Dockerfile
├── README.md
├── start.sh
└── zinit
    ├── ssh-init.yaml
    └── sshd.yaml
```

We will now explore each of those files to get a good look at the whole repository and try to understand how it all works together.

### Dockerfile

We recall that to make a Docker image, you need to create a Dockerfile. As per [Docker's documentation](https://docs.docker.com/engine/reference/builder/), a Dockerfile is "a Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image". 

The Ubuntu 22.04 Dockerfile is as follows:

File: `Dockerfile`

```Dockerfile
FROM ubuntu:22.04

RUN apt update && \
  apt -y install wget openssh-server

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit

COPY zinit /etc/zinit
COPY start.sh /start.sh

RUN chmod +x /sbin/zinit && chmod +x /start.sh
ENTRYPOINT  ["zinit", "init"]
```

We can see from the first line that the Dockerfile will look for the docker image `ubuntu:22.04`. In our case, we want to get the Debian 12 docker image. This information is available on the Docker Hub (see [Debian Docker Hub](https://hub.docker.com/_/debian)).

We will thus need to change the line `FROM ubuntu:22.04` to the line `FROM debian:12`. It isn't more complicated than that!

We now have the following Dockerfile fore the Debian docker image:

File: `Dockerfile`

```Dockerfile
FROM debian:12

RUN apt update && \
  apt -y install wget openssh-server

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit

COPY zinit /etc/zinit
COPY start.sh /start.sh

RUN chmod +x /sbin/zinit && chmod +x /start.sh
ENTRYPOINT  ["zinit", "init"]
```

There is nothing more needed here. Pretty fun to start from some existing open-source code, right?

### Docker Image Script

The other important file we will be looking at is the `start.sh` file. This is the basic script that will be used to properly set the docker image. Thankfully, there is nothing more to change in this file, we can leave it as is. As we will see later, this file will be executed by zinit when the container starts.

File: `start.sh`

```.sh
#!/bin/bash

mkdir -p /var/run/sshd
mkdir -p /root/.ssh
touch /root/.ssh/authorized_keys

chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys

echo "$SSH_KEY" >> /root/.ssh/authorized_keys
```

### zinit Folder

Next, we want to take a look at the zinit folder. 

But first, what is zinit? In a nutshell, zinit is a process manager (pid 1) that knows how to launch, monitor and sort dependencies. It thus executes targets in the proper order. For more information on zinit, check the [zinit repository](https://github.com/threefoldtech/zinit). 

When we start the Docker container, the files in the folder zinit will be executed. 

If we take a look at the file `ssh-init.yaml`, we find the following:

```.yaml
exec: bash /start.sh
log: stdout
oneshot: true
````

We can see that the first line calls the [bash](https://www.gnu.org/software/bash/) Unix shell and that it will run the file `start.sh` we've seen earlier. 

In this zinit service file, we define a service named `ssh-init.yaml`, where we tell zinit which commands to execute (here `bash /start.sh`), where to log (here in `stdout`) and where `oneshot` is set to `true` (meaning that it should only be executed once).

If we take a look at the file `sshd.yaml`, we find the following:

```.yaml
exec: bash -c "/usr/sbin/sshd -D"
after:
  - ssh-init
```

Here another service `sshd.yaml` runs after the `ssh-init.yaml` process.

### README.md File

As every good programmer knows, a good code is nothing without some good documentation to help others understand what's going on! This is where the `README.md` file comes into play.

In this file, we can explain what our code is doing and offer steps to properly configure the whole deployment. For the users that will want to deploy the flist on the ThreeFold Playground, they would need the FLIst URL and the basic steps to deploy a Micro VM on the TFGrid. We will thus add this information in the README.md file. This information can be seen in the [section below](#deploy-the-flist-on-the-tf-playground). To read the complete README.md file, go to [this link](https://github.com/threefoldtech/zos_images/tree/development/tfgrid3/debian).

### Putting it All Together

We've now went through all the files available in the Ubuntu 22.04 directory on the tf-images repository. To build your own image, you would simply need to put all those files in a local folder on your computer and follow the steps presented at the next section, [Docker Publishing Steps](#docker-publishing-steps).

To have a look at the final result of the changes we bring to the Ubuntu 22.04 version, have a look at this [Debian directory](https://github.com/threefoldtech/zos_images/tree/development/tfgrid3/debian) on the ThreeFold's tf-images repository.



## Docker Publishing Steps

### Create Account and Access Token

To be able to push Docker images to the Docker Hub, you obviously need to create a Docker Hub account! This is very easy and please note that there are so many amazing documentation on Docker online. If you're lost, make the most of your favorite search engine and find a way out of the blue.

Here are the steps to create an account and an access token.

* Go to the [Docker Hub](https://hub.docker.com/)
* Click `Register` and follow the steps given by Docker
* On the top right corner, click on your account name and select `Account Settings`
* On the left menu, click on `Security`
* Click on `New Access Token`
* Choose an Access Token description that you will easily identify then click `Generate`
  * Make sure to set the permissions `Read, Write, Delete`
* Follow the steps given to properly connect your local computer to the Docker Hub
  * Run `docker login -u <account_name>`
  * Set the password

You now have access to the Docker Hub from your local computer. We will then proceed to push the Docker image we've created.

### Build and Push the Docker Image

* Make sure the Docker Daemon is running
* Build the docker container
  * Template:
    * ```
      docker build -t <docker_username>/<docker_repo_name> . 
      ```
  * Example:
    * ```
      docker build -t username/debian12 . 
      ```
* Push the docker container to the [Docker Hub](https://hub.docker.com/)
  * Template:
    * ```
      docker push <your_username>/<docker_repo_name>
      ```
  * Example:
    * ```
      docker push username/debian12
      ```
* You should now see your docker image on the [Docker Hub](https://hub.docker.com/) when you go into the menu option `My Profile`.
  * Note that you can access this link quickly with the following template:
    * ```
      https://hub.docker.com/u/<account_name>
      ```



## Convert the Docker Image to an Flist

We will now convert the Docker image into a Zero-OS flist. This part is so easy you will almost be wondering why you never heard about flist before!

* Go to the [ThreeFold Hub](https://hub.grid.tf/).
* Sign in with the ThreeFold Connect app.
* Go to the [Docker Hub Converter](https://hub.grid.tf/docker-convert) section.
* Next to `Docker Image Name`, add the docker image repository and name, see the example below:
  * Template:
    * `<docker_username>/docker_image_name:tagname`
  * Example:
    * `username/debian12:latest`
* Click `Convert the docker image`.
* Once the conversion is done, the flist is available as a public link on the ThreeFold Hub.
* To get the flist URL, go to the [TF Hub main page](https://hub.grid.tf/), scroll down to your 3Bot ID and click on it.
* Under `Name`, you will see all your available flists.
* Right-click on the flist you want and select `Copy Clean Link`. This URL will be used when deploying on the ThreeFold Playground. We show below the template and an example of what the flist URL looks like.
  * Template:
    * ```
      https://hub.grid.tf/<3BOT_name.3bot>/<docker_username>-<docker_image_name>-<tagname>.flist
      ```
  * Example:
    * ```
      https://hub.grid.tf/idrnd.3bot/username-debian12-latest.flist
      ```



## Deploy the Flist on the TF Playground

* Go to the [ThreeFold Playground](https://play.grid.tf).
* Set your profile manager.
* Go to the [Micro VM](https://play.grid.tf/#/vm) page.
* Choose your parameters (name, VM specs, etc.).
* Under `flist`, paste the Debian flist from the TF Hub you copied previously.
* Make sure the entrypoint is as follows:
  * ```
    /sbin/zinit init
    ```
* Choose a 3Node to deploy on
* Click `Deploy`

That's it! You can now SSH into your Debian deployment and change the world one line of code at a time!

*

## Conclusion

In this case study, we've seen the overall process of creating a new flist to deploy a Debian workload on a Micro VM on the ThreeFold Playground.

If you have any questions or feedback, please let us know by either writing a post on the [ThreeFold Forum](https://forum.threefold.io/), or by chatting with us on the [TF Grid Tester Community](https://t.me/threefoldtesting) Telegram channel.
