import array
import time
from ola.ClientWrapper import ClientWrapper

wrapper = None
loop_count = 0
TICK_INTERVAL = 40  # in ms

global_count = 1

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():
  # schdule a function call in 100ms
  # we do this first in case the frame computation takes a long time.
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
  
  controlMode    = 211
  pattern        = 35
  strobe         = 0
  dotDisplay     = 100
  horizontalMove = 0
  verticalMove   = 225
  zoom           = 0
  # compute frame here
  global loop_count
  global global_count
  # if loop_count%255 < 128 : 
  verticalMove = global_count%160
  horizontalMove = global_count%160
  global_count = global_count + 4
  time.sleep(0.5)
 
  loop_count += 1

  # send
  data = array.array('B', [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom])
  print "data ", data
  wrapper.Client().SendDmx(1, data, DmxSent)
wrapper = ClientWrapper()                                                                                                       
while(1):
   SendDMXFrame()
# wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
# wrapper.Run()