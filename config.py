# Connection paramaters
PPS_ID = 0
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

# Update PPS type here: 'split' OR 'normal'
PPS_TYPE = 'normal'

# Approximate Height of B and C floors of rack
# The lowest among all racktypes
FLOOR_B = 22.5
FLOOR_C = 42.5

# Distances in cms
# Refer to the image on Page 19 at 
# https://docs.google.com/document/d/1exDAVQlbcLo02w9zR9q4-KkYBCOrZ83gg4IH4mwO_oM/edit?ts=58c7f790
# PROJ_HEIGHT is the vertical distance of the projector from the ground
PROJ_HEIGHT = 227.0
RACK_PROJ_DISTANCE = 125
# RACK_ORIGIN_DISTANCE should be -ve if the rack is to the right of the projector
RACK_ORIGIN_DISTANCE = -126.8
RACK_WIDTH = 97.0
RACK_HEIGHT = 182.0

# Butler Queue Direction w.r.t to pps (Left to Right OR Right to Left)
# For left to right QDIRECTION will be -1 and For right to left it will be 1
QDIRECTION = 1

# Manual Step: When a butler is standing at PPS with its rack lifted up,
# call `butler_communicator:send_data(gproc:lookup_local_name({butler_communicator, ButlerId}), {request_rack_deltas}).`
# debug log of butler will contain three integers as a return value of this call in the form {x,y,z}.
# Insert those values here
# set DX_SHIFT, DZ_SHIFT, DTHETA_SHIFT here, Before calibration
DX_SHIFT = 0
DZ_SHIFT = 0
DTHETA_SHIFT = 0
# Always keep this false unless otherwise told
CONSIDER_THETA_SHIFT = False

# Color of Projector Light: For Red: 10, Yellow: 20, Blue: 70
COLOR = 70

# Oscillation amplitude on y axis, in cm for non-split pps = OSCILLATION_AMP
# Oscillation amplitude on y axis, in cm for split pps = OSCILLATION_AMP + OSCILLATION_AMP_EXTRA
# Oscillation time period, in seconds
OSCILLATION_AMP = 1
OSCILLATION_AMP_EXTRA = 2
OSCILLATION_TIME_PERIOD = 0.3

# DO NOT CHANGE THESE
# Define DMX Channels - specific to the projector
PAN_CHANNEL = 1
TILT_CHANNEL = 3
PAN_FINE_CHANNEL = 2
TILT_FINE_CHANNEL = 4
STROBE_CHANNEL = 7
PATTERN_CHANNEL = 6
DIMMER_CHANNEL = 8
COLOR_CHANNEL = 5

