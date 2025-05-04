FROM base-image:latest

COPY transaction-verification-service.zip /workspace/
COPY test_validator.py /workspace/
COPY tests_rate_limiter.py /workspace/
RUN apt-get update && apt-get install -y zip
RUN unzip transaction-verification-service.zip
RUN rm -rf /workspace/transaction-verification-service.zip 
COPY scenarios.json /npc
