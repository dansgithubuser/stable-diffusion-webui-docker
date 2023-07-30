FROM --platform=$TARGETPLATFORM nvidia/cuda:11.4.3-devel-ubuntu20.04

RUN apt update && apt install -y --no-install-recommends \
        bash ca-certificates wget git gcc sudo libgl1 libglib2.0-dev python3-dev google-perftools vim ripgrep \
        && rm -rf /var/lib/apt/lists/*

RUN echo "LD_PRELOAD=/usr/lib/libtcmalloc.so.4" | tee -a /etc/environment

RUN useradd --home /app -M app -K UID_MIN=10000 -K GID_MIN=10000 -s /bin/bash
RUN mkdir /app
RUN chown app:app -R /app
RUN usermod -aG sudo app
RUN echo 'app ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER app
WORKDIR /app/

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
RUN bash ./Miniconda3-py310_23.5.2-0-Linux-x86_64.sh -b \
    && rm -rf ./Miniconda3-py310_23.5.2-0-Linux-x86_64.sh

RUN git clone --depth 1 --branch v1.5.1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /app/stable-diffusion-webui

ENV PATH /app/miniconda3/bin/:$PATH

RUN conda install python="3.10" -y

WORKDIR /app/stable-diffusion-webui

RUN ./webui.sh --exit
