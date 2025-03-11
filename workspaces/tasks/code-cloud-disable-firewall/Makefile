IMAGE_NAME=code-cloud-disable-firewall-image
CONTAINER_NAME=code-cloud-disable-firewall

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)

