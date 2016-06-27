# Connection paramaters
PPS_ID 		= 10
SERVER_IP   = '127.0.0.1'
SERVER_PORT = 9000

# DMX values for the corner points

A_THETA = 89 + (97 / 255.0)
A_PHI   = 9  + (2 / 255.0)

B_THETA = 74 + (255 / 255.0)
B_PHI   = 9  + (58 / 255.0)

C_THETA = 74 + (0 / 255.0)
C_PHI   = 68 + (152 / 255.0)

D_THETA = 88 + (109 / 255.0)
D_PHI   = 71 + (101 / 255.0)

# Rack width and height in cms

RACK_WIDTH   = 90
RACK_HEIGHT  = 180

# Offset on the calculated tilt angle, in degrees
PHI_OFFSET_DEGREES = 0

# Define DMX Channels - specific to the projector
PAN_CHANNEL        = 1
TILT_CHANNEL       = 3
PAN_FINE_CHANNEL   = 2
TILT_FINE_CHANNEL  = 4
STROBE_CHANNEL     = 7
PATTERN_CHANNEL    = 6
DIMMER_CHANNEL     = 8

# Phi range - specific to the projector
PHI_MIN_DEG = -13
PHI_MAX_DEG = 197

# Theta range - specific to "InnoPocket Scan" projector
THETA_MIN_DEG = 0
THETA_MAX_DEG = 540

# Oscillation amplitude on y axis, in cm
# Oscillation time period, in seconds
OSCILLATION_AMP         = 2
OSCILLATION_TIME_PERIOD = 0.5

