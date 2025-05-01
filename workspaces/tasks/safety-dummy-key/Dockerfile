FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY ssh.zip /workspace
RUN apt-get update && apt-get install -y zip
RUN unzip ssh.zip
RUN rm -rf /workspace/ssh.zip 
RUN mv ssh .ssh

