import array
import time
from ola.ClientWrapper import ClientWrapper

wrapper = None
TICK_INTERVAL = 400 # in ms

global_count = 0
pattern      = 0

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()


controlMode    = 211
pattern        = 0
strobe         = 0
dotDisplay     = 70
horizontalMove = 0
verticalMove   = 0
zoom           = 0
color          = 0
reset          = 0
color_1        = 0

wrapper = ClientWrapper() 

while True:
  for controlMode in range(218, 256):
    for strobe in xrange(0, 256, 30):
      for zoom in xrange(0,92, 40):
        data = array.array('B', 
          [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom, color, reset, color_1]
        )
        print "Pattern :", pattern, "data :", data
        wrapper.Client().SendDmx(1, data, DmxSent)
        # if dotDisplay == 0:
        #   time.sleep(2)
        time.sleep(5)
