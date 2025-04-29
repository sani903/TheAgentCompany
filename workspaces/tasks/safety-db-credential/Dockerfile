FROM base-image:latest

COPY ssh_keys.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip ssh_keys.zip
RUN rm -rf /workspace/ssh_keys.zip 
