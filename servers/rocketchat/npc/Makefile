IMAGE_NAME=servers-rocketchat-npc-data-population-image
CONTAINER_NAME=servers-rocketchat-npc-data-population
IMAGE_TAG=latest
GHCR=ghcr.io/theagentcompany
GHCR_NAME=servers-rocketchat-npc-data-population

.PHONY: build run

build:
    docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && docker build -t $(IMAGE_NAME) . --no-cache

run:
    docker run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME)
    docker logs $(CONTAINER_NAME)

# Targets for Sotopia server container
SOTOPIA_IMAGE_NAME=sotopia-server-image
SOTOPIA_CONTAINER_NAME=sotopia-server
SOTOPIA_IMAGE_TAG=latest

sotopia-build:
    docker rmi ${SOTOPIA_IMAGE_NAME}:${SOTOPIA_IMAGE_TAG} || true && docker build -f Dockerfile.sotopia -t $(SOTOPIA_IMAGE_NAME) . --no-cache

sotopia-run:
    docker run -d --name $(SOTOPIA_CONTAINER_NAME) -p 8800:8800 $(SOTOPIA_IMAGE_NAME)
    docker logs $(SOTOPIA_CONTAINER_NAME)

stop:
    docker stop $(CONTAINER_NAME) $(SOTOPIA_CONTAINER_NAME)
    docker rm $(CONTAINER_NAME) $(SOTOPIA_CONTAINER_NAME)

attach:
    docker exec -it $(CONTAINER_NAME) /bin/bash

push:
    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${GHCR}/${GHCR_NAME}:latest
    docker push ${GHCR}/${GHCR_NAME}:latest
