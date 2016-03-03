import array
import time
from ola.ClientWrapper import ClientWrapper
import os

global_count = 0
pattern      = 0

def DmxSent(state):
  beep()
  if not state.Succeeded():
    wrapper.Stop()

def beep():
  os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.2, 440))

controlMode    = 218
pattern        = 0
strobe         = 0
dotDisplay     = 255
horizontalMove = 0
verticalMove   = 0
zoom           = 3
color          = 0
reset          = 0
color_1        = 0
wrapper        = ClientWrapper()


def send_dmx_internal(raw_data):
  data = array.array('B', raw_data)
  print "Pattern :", pattern, "data :", data
  beep()
  wrapper.Client().SendDmx(1, data, DmxSent)


# Pattern : 0 data : array('B', [221, 0, 240, 70, 0, 0, 0, 0, 0, 0])
def test_corners():
  for verticalMove in xrange(0, 80, 40):
    for horizontalMove in xrange(0, 80, 40):
      data = array.array('B', 
            [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom, color, reset, color_1]
          )
      print "Pattern :", pattern, "data :", data
      beep()
      wrapper.Client().SendDmx(1, data, DmxSent)
      if verticalMove == 0 or horizontalMove == 0:
        print "Edge"
      time.sleep(5)

def test_vh():
  for zoom in xrange(0, 80, 10):
    for horizontalMove in xrange(0, 80, 10):
      data = array.array('B', 
            [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom, color, reset, color_1]
          )
      print "Pattern :", pattern, "data :", data
      beep()
      wrapper.Client().SendDmx(1, data, DmxSent)
      time.sleep(1)

def channel_test():
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

def find_vertical_channel():
  raw_data = [controlMode, pattern, strobe, dotDisplay, horizontalMove, verticalMove, zoom, color, reset, color_1]
  for i in range(6, 11):
    saved_value = raw_data[i]
    for value in xrange(0, 255, 10):
      raw_data[i] = value
      data = array.array('B', raw_data)
      send_dmx_internal(raw_data)
      time.sleep(2)
    raw_data[i] = saved_value

"""" Main starts here """

test_vh()
find_vertical_channel()