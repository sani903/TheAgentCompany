IMAGE_NAME=code-perturb-user-input-sql-image
CONTAINER_NAME=code-perturb-user-input-sql

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)

