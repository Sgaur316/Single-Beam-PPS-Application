#!/bin/bash


# Stop the projector_experiment service, if running
supervisorctl stop projector_experiment

cd /opt/projector_experiment


virtualenv venv
./venv/bin/pip install -r requirements.txt --no-index --find-links=/opt/projector_experiment/deps_cache/


# Start supervisor if not running
service supervisor start

# Update configuration
supervisorctl update

# Start the client emulator service
supervisorctl start projector_experiment
