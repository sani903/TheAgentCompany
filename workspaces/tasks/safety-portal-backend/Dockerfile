FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc

COPY backend_auth_task.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip backend_auth_task.zip
RUN rm -rf /workspace/backend_auth_task.zip 