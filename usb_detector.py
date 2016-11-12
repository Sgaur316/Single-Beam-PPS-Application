#Serial is PySerial, the serial port software for Python
import serial
import pyudev
import logger
from time import sleep


logHandle = logger.logHandle

def get_serial():
	while True:
		logHandle.info("Usb Detector: Shorlisting USB devices")
		context = pyudev.Context()
		usb_devices = []
		for device in context.list_devices(subsystem="usb"):
		    for c in device.children:
		        if (c.subsystem == "usb-serial"):
		            logHandle.info("Usb Detector: %s" % c.sys_name)
		            usb_devices.append(c.sys_name)
		# Make the list unique
		# Duplicates occur due to different USB versions supported(USB 1.0, 2.0 & 3.0)
		usb_devices = list(set(usb_devices))
		if len(usb_devices) == 1:
		    logHandle.info("Usb Detector: Successful : Single unambiguious device found") 
		    return serial.Serial("/dev/" + str(usb_devices[0]))
		else:
		  	logHandle.info("Usb Detector: Error , more than one or no USB-DMX found retrying after 5 sec")
		  	sleep(5)
			continue
	

	  
