FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY .bashrc /workspace
COPY .gitconfig /workspace
COPY main.py /workspace

