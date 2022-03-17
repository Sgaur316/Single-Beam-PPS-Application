#using Base image ubuntu 16
FROM ubuntu:18.04

#installing Python and essential packages
RUN apt-get update && apt-get install -y python3.6 python3-pip

# Copy projector service source code
ARG PROJECTOR_DIR="/projector_release/src/"

#------Setup the Working Directory----------
WORKDIR ${PROJECTOR_DIR}/

COPY . ${PROJECTOR_DIR}
COPY ./Deployment/Release/docker-compose.yml /docker-compose.yml

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install --upgrade distlib

RUN python3 -m pip install -r ./requirements.txt
