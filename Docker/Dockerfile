#using Base image ubuntu 16
FROM ubuntu:18.04

#installing Python and essential packages
RUN apt-get update && apt-get install -y python3-pip \
    python3.6

RUN python3.6 -m pip install --upgrade pip==20.3.1

#--- Install App specific python packages---
RUN python3.6 -m pip install \
    configparser \
    pyudev==0.22.0 \
    pyserial==3.5 \
    requests==2.18.4

# Copy projector service source code
ARG PROJECTOR_DIR="/projector_release/src/"

#------Setup the Working Directory----------
WORKDIR ${PROJECTOR_DIR}/

COPY . ${PROJECTOR_DIR}
COPY ./Deployment/Release/docker-compose.yml /docker-compose.yml
