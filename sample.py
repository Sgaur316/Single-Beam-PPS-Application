import array
from ola.ClientWrapper import ClientWrapper

wrapper = None
loop_count = 0
TICK_INTERVAL = 100  # in ms

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():
  # schdule a function call in 100ms
  # we do this first in case the frame computation takes a long time.
  wrapper.AddEvent(TICK_INTERVAL-1, SendDMXFrame)

  # compute frame here
  current_frame = [0] * 512 
  current_frame[0] = 110
  data = array.array('B', current_frame)

  # send
  print "Sending ", data
  wrapper.Client().SendDmx(1, data, DmxSent)
                                                                                                                        

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL-1, SendDMXFrame)
wrapper.Run()
