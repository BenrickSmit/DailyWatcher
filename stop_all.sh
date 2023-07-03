#!/bin/bash

# Stop all containers
docker-compose down
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -aq)


