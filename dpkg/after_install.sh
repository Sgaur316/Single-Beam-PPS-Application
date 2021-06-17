#!/bin/bash


# Stop the projector_experiment service, if running
supervisorctl stop projector_experiment

cd /opt/projector_experiment

pip uninstall virtualenv -y
pip install virtualenv
virtualenv venv/
./venv/bin/pip3.6 install -r requirements.txt --no-index --find-links=/opt/projector_experiment/deps_cache/


# Start supervisor if not running
service supervisor start

# Update configuration
supervisorctl update

# Start the client emulator service
supervisorctl start projector_experiment
