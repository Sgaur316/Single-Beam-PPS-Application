#using Base image ubuntu 16
FROM ubuntu:16.04

#installing Python and essential packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean

RUN pip install --upgrade pip

#--- Install App specific python packages---
RUN pip install \
    configparser \
    pyudev==0.21.0 \
    pyserial==3.2.1 \ 
    requests==2.5.0 

# Copy gpms scannersource code 
ARG PROJECTOR_DIR="/projector_release/src/"

COPY . ${PROJECTOR_DIR}

#------Setup the Working Directory----------
WORKDIR ${PROJECTOR_DIR}/