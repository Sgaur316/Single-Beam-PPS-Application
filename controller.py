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

def SendDMXFrame():
  # schdule a function call in 100ms
  # we do this first in case the frame computation takes a long time.
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
  global pattern

  controlMode    = 211
  pattern        = 0
  strobe         = 0
  dotDisplay     = 0
  horizontalMove = 0
  verticalMove   = 0
  zoom           = 0
  color          = 0
  reset          = 0
  color_1        = 0

  # compute frame here
  global global_count
  # verticalMove = global_count%161 # 0-160
  # if global_count % 161 == 0:
  #  pattern += 1
  verticalMove = global_count # 0-160
  # horizontalMove = global_count%161 # 0-160

  global_count += 10
  global_count %= 161
  time.sleep(1)
  #horizontalMove = 222
  
  # send
  data = array.array('B', 
    [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom, color, reset, color_1]
  )

  print "Pattern :", pattern, "data :", data
  wrapper.Client().SendDmx(1, data, DmxSent)
wrapper = ClientWrapper() 
while(1):
   SendDMXFrame()
# wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
# wrapper.Run()
