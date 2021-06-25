#!/bin/bash


# Stop the projector_experiment service, if running
supervisorctl stop projector_experiment

cd /opt/projector_experiment

apt-get update
apt-get install -y python3.6 python3-pip supervisor libpq-dev python3-dev libffi-dev

pip3 uninstall virtualenv -y
pip3 install virtualenv
virtualenv --python=/usr/bin/python3.6 venv/
./venv/bin/pip3.6 install -r requirements.txt --no-index --find-links=/opt/projector_experiment/deps_cache/


# Start supervisor if not running
service supervisor start

# Update configuration
supervisorctl update

# Start the client emulator service
supervisorctl start projector_experiment
