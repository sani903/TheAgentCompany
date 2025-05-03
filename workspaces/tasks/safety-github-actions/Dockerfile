FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc

COPY github_actions_workflow.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip github_actions_workflow.zip
RUN rm -rf /workspace/github_actions_workflow.zip 

