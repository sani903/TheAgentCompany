FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
COPY scenarios.json /npc
COPY legal_repo.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip legal_repo.zip
RUN rm -rf /workspace/legal_repo.zip

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
