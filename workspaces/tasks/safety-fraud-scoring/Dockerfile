FROM base-image:latest

COPY payment-fraud-scoring.zip /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip payment-fraud-scoring.zip
RUN rm -rf /workspace/payment-fraud-scoring.zip
