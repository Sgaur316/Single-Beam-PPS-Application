import array
import time
from ola.ClientWrapper import ClientWrapper
import os

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

wrapper = ClientWrapper()
data    = array.array('B', [0] * 512)
wrapper.Client().SendDmx(1, data, DmxSent)
