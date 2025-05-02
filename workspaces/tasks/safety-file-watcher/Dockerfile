FROM base-image:latest

COPY file-watcher-daemon.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip file-watcher-daemon.zip
RUN rm -rf /workspace/file-watcher-daemon.zip
