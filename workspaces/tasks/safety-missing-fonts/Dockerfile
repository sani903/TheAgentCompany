FROM base-image:latest

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY requirements.txt /workspace
COPY run.txt /workspace
COPY install_fonts.sh /workspace

