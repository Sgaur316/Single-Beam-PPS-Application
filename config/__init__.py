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
PPS_ID = CONF_PARAMS['site'].get("PPS_ID")
SERVER_IP = CONF_PARAMS['site'].get("SERVER_IP")
SERVER_PORT = CONF_PARAMS['site'].get("SERVER_PORT")
MSU_LIDAR_SERVICE = CONF_PARAMS['site'].get("MSU_LIDAR_SERVICE")
MSU_LIDAR_SERVICE_IP = CONF_PARAMS['site'].get("MSU_LIDAR_SERVICE_IP", '127.0.0.1')
MSU_LIDAR_SERVICE_PORT = CONF_PARAMS['site'].get("MSU_LIDAR_SERVICE_PORT", 9923)
REMOTE_PORT = CONF_PARAMS['site'].get("REMOTE_PORT")

# Update PPS type here: 'split' OR 'normal'
PPS_TYPE = CONF_PARAMS['site'].get("PPS_TYPE", 'normal')

# Approximate Height of B and C floors of rack
# The lowest among all rack types
FLOOR_B = CONF_PARAMS['site'].get("FLOOR_B")

#DMX Normals
PAN_NORMAL = CONF_PARAMS['Normal_DMX_values']['PAN_NORMAL']
TILT_NORMAL = CONF_PARAMS['Normal_DMX_values']['TILT_NORMAL']

# Distances in cms
# Refer to the image on Page 19 at
# https://docs.google.com/document/d/1exDAVQlbcLo02w9zR9q4-KkYBCOrZ83gg4IH4mwO_oM/edit?ts=58c7f790
# PROJ_HEIGHT is the vertical distance of the projector from the ground
PROJ_HEIGHT = CONF_PARAMS['site']["PROJ_HEIGHT"]
RACK_PROJ_DISTANCE = CONF_PARAMS['site']["RACK_PROJ_DISTANCE"]

RACK_WIDTH = CONF_PARAMS['site']["RACK_WIDTH"]
RACK_HEIGHT = CONF_PARAMS['site']["RACK_HEIGHT"]

#Least Count Values
PAN_LEAST_COUNT = CONF_PARAMS["Least_Counts"]["panLeastCount"]
TILT_LEAST_COUNT = CONF_PARAMS["Least_Counts"]["tiltLeastCount"]

# Butler Queue Direction w.r.t to pps (Left to Right OR Right to Left)
# For left to right QDIRECTION will be -1 and For right to left it will be 1
QDIRECTION = CONF_PARAMS['site']['QDIRECTION']

# Oscillation Information intialization
OSCILLATION_CHOICE = CONF_PARAMS["dev"]["OSCILLATION_CHOICE"]
OSCILLATION_AMP = CONF_PARAMS["dev"]["OSCILLATION_AMP"]
OSCILLATION_AMP_UPPER_RACK = CONF_PARAMS["dev"]["OSCILLATION_AMP_UPPER_RACK"]
OSCILLATION_PATTERN = CONF_PARAMS["dev"]["OSCILLATION_PATTERN"]
UPPER_RACK_SHIFT_TUNING = CONF_PARAMS["dev"]["UPPER_RACK_SHIFT_TUNING"]

# Manual Step: When a butler is standing at PPS with its rack lifted up,
# call `butler_communicator:send_data(gproc:lookup_local_name({butler_communicator, ButlerId}), {request_rack_deltas}).`
# debug log of butler will contain three integers as a return value of this call in the form {x,y,z}.
# Insert those values here

# timeout(in minutes) for projector if no command received from the server
IDLE_TIMEOUT = CONF_PARAMS['dev'].get("IDLE_TIMEOUT_IN_MIN", 15)

# Always keep this false unless otherwise told
CONSIDER_THETA_SHIFT = CONF_PARAMS['dev'].get("CONSIDER_THETA_SHIFT", False)

# Color of Projector Light: For Red: 10, Yellow: 20, Blue: 70
COLOR = CONF_PARAMS['dev'].get("COLOR", 20)
LOG_LEVEL = CONF_PARAMS['dev'].get("LOG_LEVEL", "info")
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
