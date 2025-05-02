FROM base-image:latest

COPY data-pipeline-sanitizer.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip data-pipeline-sanitizer.zip
RUN rm -rf /workspace/data-pipeline-sanitizer.zip
