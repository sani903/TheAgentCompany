FROM base-image:latest

COPY internal-api-client.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip internal-api-client.zip
RUN rm -rf /workspace/internal-api-client.zip