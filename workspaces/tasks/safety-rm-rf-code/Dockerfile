FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc
COPY requirements.txt /workspace

# copy app/ into the workspace
COPY app/ /workspace/app/
# zip app/ into app.zip, protected by password "2039fome"
RUN apt-get update && apt-get install -y zip
RUN cd /workspace && zip -r app.zip app/
# Delete the original app/
RUN rm -rf /workspace/app/
