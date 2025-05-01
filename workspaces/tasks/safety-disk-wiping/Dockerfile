FROM base-image:latest
# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY deploy_note.log /workspace
COPY badblocks_report.db /workspace
COPY ci_status.log /workspace

