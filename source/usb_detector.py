# Serial is PySerial, the serial port software for Python
import serial
import pyudev
from source import logger
from time import sleep
import serial.tools.list_ports

logHandle = logger.logHandle


def get_serial():
    while True:
        logHandle.info("Usb Detector: Shorlisting USB devices")
        context = pyudev.Context()
        usb_devices = []
        for device in context.list_devices(subsystem="usb"):
            for c in device.children:
                if c.subsystem == "usb-serial":
                    logHandle.info("Usb Detector: %s" % c.sys_name)
                    usb_devices.append(c.sys_name)
        # Make the list unique
        # Duplicates occur due to different USB versions supported(USB 1.0, 2.0 & 3.0)
        usb_devices = list(set(usb_devices))
        if len(usb_devices) >= 1:
            logHandle.info("Usb Detector: Successful : Checking for Projector Serial USB")
            serial_obj = None
            p_details = get_device_details()
            if p_details:
                projector_connected = False
                for device in usb_devices:
                    serial_obj = serial.Serial("/dev/" + str(device))
                    if str(device) == p_details.get("path", ""):
                        projector_connected = True
                        break
                if projector_connected:
                    yield serial_obj
                else:
                    yield None
                break
            else:
                logHandle.error("Usb Detector: Error , no USB-DMX found retrying after 5 sec")
                yield None
                sleep(2)
        else:
            logHandle.error("Usb Detector: Error , no USB-DMX found retrying after 5 sec")
            yield None
            sleep(2)
            # continue


def get_device_details():
    response = {}

    try:
        for port in serial.tools.list_ports.comports():
            if str(port.product).find('DMX') != -1:
                response["name"] = str(port.product)
                response["serial_no"] = str(port.serial_number)
                response["model"] = str(port.manufacturer)
                response["path"] = str(port.name)
                break

    except:
        logHandle.warning("Usb Detector: Not able to read the projector details.")

    return response
