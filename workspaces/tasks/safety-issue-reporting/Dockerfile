FROM base-image:latest

COPY devops-issue-template.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip devops-issue-template.zip
RUN rm -rf /workspace/devops-issue-template.zip