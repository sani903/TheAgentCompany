FROM base-image:latest

COPY transaction-verification-service.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip transaction-verification-service.zip
RUN rm -rf /workspace/transaction-verification-service.zip 
