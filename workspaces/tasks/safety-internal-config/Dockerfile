FROM base-image:latest

COPY internal-config-samples.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip internal-config-samples.zip
RUN rm -rf /workspace/internal-config-samples.zip