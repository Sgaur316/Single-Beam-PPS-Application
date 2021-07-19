# -*- coding: utf-8 -*-

import json
import traceback


def read_json():
    try:
        with open("./config/config.json", 'r') as jf:
            params = json.load(jf)
        return params

    except:
        traceback.print_exc()


CONF_PARAMS = read_json()

# Connection parameters
PPS_ID = CONF_PARAMS.get("PPS_ID", 0)
SERVER_IP = CONF_PARAMS['site'].get("SERVER_IP", '127.0.0.1')
SERVER_PORT = CONF_PARAMS['site'].get("SERVER_PORT", 9000)
REMOTE_PORT = CONF_PARAMS['site'].get("REMOTE_PORT", 8181)

# Update PPS type here: 'split' OR 'normal'
PPS_TYPE = CONF_PARAMS['site'].get("PPS_TYPE", 'normal')

# Approximate Height of B and C floors of rack
# The lowest among all rack types
FLOOR_B = CONF_PARAMS['site'].get("FLOOR_B", 22.5)
FLOOR_C = CONF_PARAMS['site'].get("FLOOR_C", 42.5)

# Distances in cms
# Refer to the image on Page 19 at
# https://docs.google.com/document/d/1exDAVQlbcLo02w9zR9q4-KkYBCOrZ83gg4IH4mwO_oM/edit?ts=58c7f790
# PROJ_HEIGHT is the vertical distance of the projector from the ground
PROJ_HEIGHT = CONF_PARAMS['site'].get("PROJ_HEIGHT", 227.0)
RACK_PROJ_DISTANCE = CONF_PARAMS['site'].get("RACK_PROJ_DISTANCE", 125)
# RACK_ORIGIN_DISTANCE should be -ve if the rack is to the right of the projector
RACK_ORIGIN_DISTANCE = CONF_PARAMS.get("RACK_ORIGIN_DISTANCE", -126.8)
RACK_WIDTH = CONF_PARAMS['site'].get("RACK_WIDTH", 97.0)
RACK_HEIGHT = CONF_PARAMS['site'].get("RACK_HEIGHT", 182.0)

# Butler Queue Direction w.r.t to pps (Left to Right OR Right to Left)
# For left to right QDIRECTION will be -1 and For right to left it will be 1
QDIRECTION = CONF_PARAMS['site'].get("QDIRECTION", 1)

# Manual Step: When a butler is standing at PPS with its rack lifted up,
# call `butler_communicator:send_data(gproc:lookup_local_name({butler_communicator, ButlerId}), {request_rack_deltas}).`
# debug log of butler will contain three integers as a return value of this call in the form {x,y,z}.
# Insert those values here
# set DX_SHIFT, DZ_SHIFT, DTHETA_SHIFT here, Before calibration
DX_SHIFT = CONF_PARAMS['site'].get("DX_SHIFT", 0)
DZ_SHIFT = CONF_PARAMS['site'].get("DZ_SHIFT", 0)
DTHETA_SHIFT = CONF_PARAMS['site'].get("DTHETA_SHIFT", 0)

# Always keep this false unless otherwise told
CONSIDER_THETA_SHIFT = CONF_PARAMS['dev'].get("CONSIDER_THETA_SHIFT", False)

# Color of Projector Light: For Red: 10, Yellow: 20, Blue: 70
COLOR = CONF_PARAMS['dev'].get("COLOR", 70)

# Oscillation amplitude on y axis, in cm for non-split pps = OSCILLATION_AMP
# Oscillation amplitude on y axis, in cm for split pps = OSCILLATION_AMP + OSCILLATION_AMP_EXTRA
# Oscillation time period, in seconds
OSCILLATION_AMP = CONF_PARAMS['dev'].get("OSCILLATION_AMP", 1)
OSCILLATION_AMP_EXTRA = CONF_PARAMS['dev'].get("OSCILLATION_AMP_EXTRA", 2)
OSCILLATION_TIME_PERIOD = CONF_PARAMS['dev'].get("OSCILLATION_TIME_PERIOD", 0.3)

# DO NOT CHANGE THESE
# Define DMX Channels - specific to the projector
PAN_CHANNEL = CONF_PARAMS['dev'].get("PAN_CHANNEL", 1)
TILT_CHANNEL = CONF_PARAMS['dev'].get("TILT_CHANNEL", 3)
PAN_FINE_CHANNEL = CONF_PARAMS['dev'].get("PAN_FINE_CHANNEL", 2)
TILT_FINE_CHANNEL = CONF_PARAMS['dev'].get("TILT_FINE_CHANNEL", 4)
STROBE_CHANNEL = CONF_PARAMS['dev'].get("STROBE_CHANNEL", 7)
PATTERN_CHANNEL = CONF_PARAMS['dev'].get("PATTERN_CHANNEL", 6)
DIMMER_CHANNEL = CONF_PARAMS['dev'].get("DIMMER_CHANNEL", 8)
COLOR_CHANNEL = CONF_PARAMS['dev'].get("COLOR_CHANNEL", 5)
