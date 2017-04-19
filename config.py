# Connection paramaters
PPS_ID = 0
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

# Update PPS type here: 'split' OR 'normal'
PPS_TYPE = 'normal'

# Approximate Height of floors of rack
FLOOR_B = 22.5
FLOOR_C = 42.5

# Distances in cms
PROJ_HEIGHT = 227.0
RACK_PROJ_DISTANCE = 125
RACK_ORIGIN_DISTANCE = -126.8
RACK_WIDTH = 97.0
RACK_HEIGHT = 182.0

# Butler Queue Direction w.r.t to pps (Left to Right OR Right to Left)
# For left to right QDIRECTION will be -1 and For right to left it will be 1
QDIRECTION = 1
# set DX_SHIFT, DZ_SHIFT, DTHETA_SHIFT here, Before calibration
DX_SHIFT = 0
DZ_SHIFT = 0
DTHETA_SHIFT = 0
CONSIDER_THETA_SHIFT = False


# Define DMX Channels - specific to the projector
PAN_CHANNEL = 1
TILT_CHANNEL = 3
PAN_FINE_CHANNEL = 2
TILT_FINE_CHANNEL = 4
STROBE_CHANNEL = 7
PATTERN_CHANNEL = 6
DIMMER_CHANNEL = 8
COLOR_CHANNEL = 5

# Color of Projector Light: For Red: 10, Yellow: 20, Blue: 70
COLOR = 70

# Oscillation amplitude on y axis, in cm
# Oscillation time period, in seconds
OSCILLATION_AMP = 1
OSCILLATION_TIME_PERIOD = 0.3

# For split pps to fix deviation in Y direction increase oscillation amplitude
# by this value
OSCILLATION_AMP_EXTRA = 2
