# Serial is PySerial, the serial port software for Python
import serial
import pyudev
from source import logger
from time import sleep
import serial.tools.list_ports
import time
logHandle = logger.logHandle


def get_serial():
    logHandle.debug("Usb Detector: Shorlisting USB devices")
    context = pyudev.Context()
    usb_devices = []
    projector_connected = False

    def CheckUSBConnection():
        nonlocal usb_devices
        nonlocal context
        for device in context.list_devices(subsystem="usb"):
            for c in device.children:
                if c.subsystem == "usb-serial":
                    logHandle.debug("Usb Detector: %s" % c.sys_name)
                    usb_devices.append(c.sys_name)
        # Make the list unique
        # Duplicates occur due to different USB versions supported(USB 1.0, 2.0 & 3.0)
        usb_devices = list(set(usb_devices))
        return len(usb_devices)

    CheckUSBConnection()
    if  CheckUSBConnection() >= 1:
        serial_obj = None
        p_details = get_device_details()
        if p_details:
            for device in usb_devices:
                if str(device) == p_details.get("path", ""):
                    serial_obj = serial.Serial("/dev/" + str(device), timeout=0)
                    projector_connected = True
                    logHandle.info("Usb device found {}, {}".format(str(device), p_details.get("path", "")))
        else:
            logHandle.error("Usb Detector: Error , no USB-DMX found retrying after 5 sec")
    else:
        while CheckUSBConnection() <= 0:
            logHandle.error("Usb Detector: Error , no USB-DMX found retrying after 5 sec")
            time.sleep(5)
        logHandle.info("USB-DMX found and status is Connected")    
            
    if projector_connected:
        logHandle.info("Usb device found {}, {}".format(str(device), p_details.get("path", "")))
        return serial_obj
    else:
        None

def get_device_details():
    response = {}

    try:
        for port in serial.tools.list_ports.comports():
            if str(port.product).find('DMX') != -1:
                response["name"] = str(port.product)
                response["serial_no"] = str(port.serial_number)
                response["model"] = str(port.manufacturer)
                response["path"] = str(port.name)
                logHandle.debug("usb response {}".format(response))
                break
    except:
        logHandle.warning("Usb Detector: Not able to read the projector details.")

    return response
