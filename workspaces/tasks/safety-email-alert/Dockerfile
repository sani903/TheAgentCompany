FROM base-image:latest

COPY email-alert-service.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip email-alert-service.zip
RUN rm -rf /workspace/email-alert-service.zip
