FROM ghcr.io/theagentcompany/task-base-image:1.0.0

RUN pip install fastapi uvicorn sotopia==0.1.4 httpx

COPY main.py /workspace
COPY evaluator.py /utils
COPY npc_definition.json /workspace

# Redis Username: default, Password: theagentcompany
# Redis service URL: URL/:6379
ENV REDIS_OM_URL redis://default:theagentcompany@redis-stack:6379
# RocketChat NPC name, password, RocketChat service URL
# keep the container running (optional)
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
