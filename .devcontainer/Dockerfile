FROM ubuntu:22.04

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bc \
    build-essential \
    ca-certificates \
    clang \
    clang-format \
    curl \
    git \
    libffi-dev \
    make \
    openssh-client \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    shellcheck \
    sudo \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up Python environment
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install pre-commit, pytest, and other development tools
RUN python3 -m pip install pre-commit pytest pytest-cov ruff

# Set up shell for the non-root user
USER $USERNAME
WORKDIR /home/$USERNAME/workspace

# Setup shell history
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/home/$USERNAME/.bashrc"

# Set default shell to bash
SHELL ["/bin/bash", "-c"]
