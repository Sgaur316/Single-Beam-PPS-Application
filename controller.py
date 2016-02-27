import array
import sys
import datetime
from random import randint
from ola.ClientWrapper import ClientWrapper

TICK_INTERVAL = 100  # in ms

class Controller:
	def __init__(self):
		self.current_frame = [0] * 512
		self.wrapper = ClientWrapper()

	def DmxSent(state):
	  	if not state.Succeeded():
	  		self.wrapper.Stop()

	""" start dmx transmission """
	def SendDmxFrame(self):
		self.current_frame[0] = 225
		self.current_frame[1] = 17
		self.current_frame[2] = 0
		self.current_frame[3] = 207 
		self.current_frame[4] = 100
		self.current_frame[5] = 0
		self.current_frame = array.array('B', self.current_frame)

		self.wrapper.AddEvent(TICK_INTERVAL, self.SendDmxFrame)
		self.wrapper.Run()
		print "Sending DMX signal"
		wrapper.Client().SendDmx(1, self.current_frame, DmxSent)

# start app
controller = Controller()
controller.SendDmxFrame()