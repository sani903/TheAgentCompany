IMAGE_NAME=code-network-management-ip-address-and-ports-image
CONTAINER_NAME=code-network-management-ip-address-and-ports

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)

