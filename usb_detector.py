# Serial is PySerial, the serial port software for Python
import serial
import pyudev
import logger
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
            for device in usb_devices:
                serial_obj = serial.Serial("/dev/" + str(device))
                if str(device) == p_details.get("path", ""):
                    break
            yield serial_obj
            break

        else:
            logHandle.info("Usb Detector: Error , no USB-DMX found retrying after 5 sec")
            yield None
            sleep(2)
            # continue


def get_device_details():
    response = {"name": "",
                "model": "",
                "serial_no": "",
                "path": ""}

    try:
        for port in serial.tools.list_ports.comports():
            if str(port.product).find('DMX') != -1:
                response["name"] = str(port.product)
                response["serial_no"] = str(port.serial_number)
                response["model"] = str(port.manufacturer)
                response["path"] = str(port.name)
                break
                # print(port.hwid)
                # print(port.location)
                # print(port.manufacturer)
                # print(port.product)
                # print(port.serial_number)
                # print(port.usb_description)
                # print(port.usb_info)
                # print(port.device)
                # print(port.description)

    except:
        logHandle.warning("Usb Detector: Not able to read the projector details.")

    return response
