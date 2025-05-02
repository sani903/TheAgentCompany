FROM base-image:latest

COPY secure-login-service.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip secure-login-service.zip
RUN rm -rf /workspace/secure-login-service.zip
