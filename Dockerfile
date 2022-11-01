# Base Image
FROM ubuntu:22.04

# Base Environment Variables
ENV PROJECT FakeNTP
ENV LC_CTYPE C.UTF-8

# tzdata Docker work around
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN truncate -s0 /tmp/preseed.cfg; \
    echo "tzdata tzdata/Areas select Europe" >> /tmp/preseed.cfg; \
    echo "tzdata tzdata/Zones/Europe select Berlin" >> /tmp/preseed.cfg; \
    debconf-set-selections /tmp/preseed.cfg && \
    rm -f /etc/timezone /etc/localtime && \
    apt-get update && \
    apt-get install -y tzdata
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Update and Install Development Packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y git \
    cmake \
    ninja-build \
    build-essential \
    python3-minimal python3-pip\
    wget \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Set Directory
WORKDIR /${PROJECT}

CMD [ "/bin/bash" ]