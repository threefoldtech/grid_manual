---
title: "Docker Basics"
sidebar_position: 272
---





## Introduction

We present here a quick introduction to Docker. We cover basic commands, as well as command combinations. Understanding the following should give system administrators confidence when it comes to using Docker efficiently.

The following can serve as a quick reference guide when deploying workloads on the ThreeFold Grid and using Docker in general.

We invite the readers to consult the [official Docker documentation](https://docs.docker.com/) for more information.



## Basic Commands

### Install Docker Desktop and Docker Engine

You can install [Docker Desktop](https://docs.docker.com/get-docker/) and [Docker Engine](https://docs.docker.com/engine/install/) for Linux, MAC and Windows. Follow the official Docker documentation for the details.

Note that the quickest way to install Docker Engine is to use the convenience script:

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```



### Remove completely Docker

To completely remove docker from your machine, you can follow these steps:

* List the docker packages
  * ```
    dpkg -l | grep -i docker
    ```
* Purge and autoremove docker
  * ```
    apt-get purge -y docker-engine docker docker.io docker-ce docker-ce-cli docker-compose-plugin
    apt-get autoremove -y --purge docker-engine docker docker.io docker-ce docker-compose-plugin
    ```
* Remove the docker files and folders
  * ```
    rm -rf /var/lib/docker /etc/docker
    rm /etc/apparmor.d/docker
    groupdel docker
    rm -rf /var/run/docker.sock
    ```

You can also use the command **whereis docker** to see if any Docker folders and files remain. If so, remove them with 



### List containers

* List only running containers
  * ```
    docker ps
    ```
* List all containers (running + stopped)
  * ```
    docker ps -a
    ```



### Pull an image

To pull an image from [Docker Hub](https://hub.docker.com/):

* Pull an image
  * ```
    docker pull image_name
    ```
* Pull an image with the tag
  * ```
    docker pull image_name:tag
    ```
* Pull all tags of an image
  * ```
    docker pull image_name -a
    ```



### Push an image

To pull an image to [Docker Hub](https://hub.docker.com/):

* Push an image
  * ```
    docker push image_name
    ```
* Push an image with the tag
  * ```
    docker push image_name:tag
    ```
* Push all tags of an image
  * ```
    docker pull image_name -a
    ```



### Inspect and pull an image with GHCR

* Inspect the docker image
  * ```
    docker inspect ghcr.io/<repository>/<image>:<tag>
    ```
* Pull the docker image
  * ```
    docker pull ghcr.io/<repository>/<image>:<tag>
    ```



### See a docker image (no download)

If you want to see a docker image without downloading the image itself, you can use Quay's [Skopeo tool](https://github.com/containers/skopeo), a command line utility that performs various operations on container images and image repositories. 

```
docker run --rm quay.io/skopeo/stable list-tags docker://ghcr.io/<repository>/<image>
```

Make sure to write the proper information for the repository and the image.

To install Skopeo, read [this documentation](https://github.com/containers/skopeo/blob/main/install.md).




### Build a container

Use **docker build** to build a container based on a Dockerfile

* Build a container based on current directory Dockerfile
  * ```
    docker build .
    ```
* Build a container and store the image with a given name
  * Template
    * ```
      docker build -t "image_name:<tag>"
      ```
  * Example
    * ```
      docker build -t newimage:latest
      ```
* Build a docker container without using the cache
  * ```
    docker build --no-cache
    ```



### List all available docker images

```
docker images
```



### Run a container

To run a container based on an image, use the command **docker run**.

* Run an image
  * ```
    docker run image_name
    ```
* Run an image in the background (run and detach)
  * ```
    docker run -d image_name
    ```
* Run an image with CLI input
  * ```
    docker run -it image_name
    ```

You can combine arguments, e.g. **docker run -itd**.

You can also specify the shell, e.g. **docker run -it image_name /bin/bash**



### Run a new command in an existing container

To run a new command in an existing container, use **docker exec**.

* Execute interactive shell on the container
  * ```
    docker exec -it <container_name> sh
    ```



### Bash shell into container 

* Bash shell into a container
  * ```
    docker exec -i -t /bin/bash
    ```
* Bash shell into a container with root
  * ```
    docker exec -i -t -u root /bin/bash
    ```

Note: if bash is not available, you can use `/bin/sh`



### Pass arguments with a bash script and a Dockerfile

You can do the following to pass arguments with a bash script and a Dockerfile.

```sh
# script_example.sh
#!/bin/sh

echo This is the domain: $env_domain
echo This is the name: $env_name
echo This is the password: $env_password

```
* File `Dockerfile`

```Dockerfile
FROM ubuntu:latest

ARG domain

ARG name

ARG password

ENV env_domain $domain

ENV env_name $name

ENV env_password $password

COPY script_example.sh .

RUN chmod +x /script_example.sh

CMD ["/script_example.sh"]
```



### Copy files from a container to the local computer

```
docker cp <container_id>:<file_path> <file_path_destination>
```



### Delete all the containers, images and volumes

* To delete all containers:
  * ```
    docker compose rm -f -s -v
    ```

* To delete all images:
  * ```
    docker rmi -f $(docker images -aq)
    ```

* To delete all volumes:
  * ```
    docker volume rm $(docker volume ls -qf dangling=true)
    ```

* To delete all containers, images and volumes:
  * ```
    docker compose rm -f -s -v && docker rmi -f $(docker images -aq) && docker volume rm $(docker volume ls -qf dangling=true)
    ```



### Kill all the Docker processes

* To kill all processes:
  * ```
    killall Docker && open /Applications/Docker.app
    ```



### Output full logs for all containers

The following command output the full logs for all containers in the file **containers.log**:

```
docker compose logs > containers.log
```



## Resources Usage

### Examine containers with size

```
docker ps -s
```



### Examine disks usage

* Basic mode
  * ```
    docker system df
    ```
* Verbose mode
  * ```
    docker system df -v
    ```



## Wasted Resources

### Prune the Docker logs

```
docker system prune
```

### Prune the Docker containers

You can use the prune function to delete all stopped containers:

```
docker container prune
```

### Remove unused and untagged local container images

The following is useful if you want to clean up local filesystem:

```
docker image prune
```

### Clean up and delete all unused container images

```
docker image prune -a
```

### Clean up container images based on a given timeframe

To clean up container images created X hours ago, you can use the following template (replace X with a number):

```
docker image prune -a --force --filter "until=Xh"
```

To clean up container images created before a given date, you can use the following template (replace `<date>` with the complete date):

```
docker image prune -a --force --filter "until=<date>"
```

Note: An example of a complete date would be `2023-01-04T00:00:00`



## Command Combinations

### Kill all running containers

```
docker kill $(docker ps -q)
```



### Stop all running containers

```
docker stop $(docker ps -a -q)
```



### Delete all stopped containers

```
docker rm $(docker ps -a -q)
```


### Delete all images 

```
docker rmi $(docker images -q)
```



### Update and stop a container in a crash-loop 

```
docker update –restart=no && docker stop
```



## References

* Docker Manual - https://docs.docker.com/
* Code Notary - https://codenotary.com/blog/extremely-useful-docker-commands