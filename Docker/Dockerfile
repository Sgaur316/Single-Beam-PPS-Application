#using Base image ubuntu 16
FROM ubuntu:16.04

#installing Python and essential packages
RUN apt-get update && apt-get install -y python-pip \
    python2.7

RUN pip install --upgrade pip==20.3.1

#--- Install App specific python packages---
RUN pip install \
    pyserial \
    pyudev==0.17

# Copy projector service source code
ARG PROJECTOR_DIR="/projector_release/src/"

#------Setup the Working Directory----------
WORKDIR ${PROJECTOR_DIR}/

COPY . ${PROJECTOR_DIR}
COPY ./Deployment/Release/docker-compose.yml /docker-compose.yml


