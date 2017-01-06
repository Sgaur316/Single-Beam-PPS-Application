#!/bin/bash

# Stop the gpms_bridge , if running, and remove from process group
supervisorctl update

# Pass even if the above cmds failed
true
