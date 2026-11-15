# Controller image for running AIOpsLab (https://github.com/microsoft/AIOpsLab) experiments.
# Built and run by roles/aiopslab; see that role's README for how the two supported cluster
# targets (k3s, kind) are wired up. This image is target-agnostic - everything here is
# common setup, the target only affects how the container is *run*
# (roles/aiopslab/tasks/install.yml), never how it's built.
FROM python:3.11-slim

ARG AIOPSLAB_VERSION=main
ARG AIOPSLAB_REPO_URL=https://github.com/microsoft/AIOpsLab.git

# git/curl: clone AIOpsLab and run install scripts. ca-certificates: TLS for both.
# libssl-dev: build dependency of AIOpsLab's bundled wrk2 workload generator.
RUN apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/local/bin/kubectl \
      "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" \
    && chmod +x /usr/local/bin/kubectl

# docker CLI only (no daemon) - AIOpsLab's own Shell.docker_exec() shells out to `docker exec
# kind-control-plane ...` to run commands inside the kind cluster, over the socket mounted
# into this container at run time (kind target only). The static binary is used instead of
# the docker.io apt package: on Debian 13 (this image's base) that package ships dockerd but
# not the docker CLI client at all.
RUN curl -fsSL https://download.docker.com/linux/static/stable/aarch64/docker-27.3.1.tgz \
      | tar -xz -C /usr/local/bin --strip-components=1 docker/docker

RUN curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

RUN git clone --recurse-submodules --branch "${AIOPSLAB_VERSION}" --depth 1 \
      "${AIOPSLAB_REPO_URL}" /aiopslab
WORKDIR /aiopslab

# In-project venv keeps everything under /aiopslab/.venv, so image layers stay self-contained.
# The "clients" poetry group (vllm/transformers/autogen-agentchat/azure-ai-ml/groq/flwr)
# targets CUDA/cloud-ML hardware and isn't expected to build on ARM64; the bundled GPT,
# Qwen, DeepSeek, OpenRouter and generic-OpenAI-compatible clients this image runs only
# depend on AIOpsLab's core dependency group (openai, python-dotenv, tiktoken, ... are all
# core deps, not in the clients group).
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install --without clients

COPY run_experiment.py /aiopslab/run_experiment.py

CMD ["sleep", "infinity"]
