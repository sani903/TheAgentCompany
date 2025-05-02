FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
COPY scenarios.json /npc
COPY audit_materials.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip audit_materials.zip
RUN rm -rf /workspace/audit_materials.zip