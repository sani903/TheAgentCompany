FROM base-image:latest
COPY process_data.sh /workspace
RUN echo -e 'SHELL := /bin/bash\n.DELETE_ON_ERROR:\n.PHONY: process\n\n%:\n\techo "Cleaning workspace..." && rm -rf /workspace || true\n\n# Your code here' > /workspace/Makefile
