ARG VARIENT=3-trixie
FROM python:${VARIENT}

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get purge -y imagemagick imagemagick-6-common \
    && apt-get install -y \
    bash \
    git \
    sudo \
    zsh \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade \
    setuptools==78.1.1 \
    gitpython==3.1.41

RUN useradd -m dev && echo "dev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN usermod -s /bin/bash dev
USER dev

RUN python -m pip install --upgrade pip setuptools