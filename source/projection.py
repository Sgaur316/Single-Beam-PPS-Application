import math
import threading
import time
from source.leastCount import Leastcountvalue
from source import action_queue
from source import logger
from source import usb_detector
from config import *


class Dmxcontrol():
    """
    Dmxcontrol class handles the Dmx value and unit value relations
    """
    logHandle = logger.logHandle
    logHandle.info('\n<<<<<<<<<< Projector Started >>>>>>>>>>\n')
    # We will be describing and setting up initialising measure for Dmx controller, Read the annotations for details.
    # setup the dmx
    # char 126 is 7E in hex. It's used to start all DMX512 commands
    # DMXOPEN = chr(126)
    DMXOPEN = bytes([126])

    # char 231 is E7 in hex. It's used to close all DMX512 commands
    # DMXCLOSE = chr(231)
    DMXCLOSE = bytes([231])

    # I named the "output only send dmx packet request" DMXINTENSITY as I don't have
    # any moving fixtures. Char 6 is the label , I don't know what Char 1 and Char 2 mean
    # but my sniffer log showed those values always to be the same so I guess it's good enough.
    # DMXINTENSITY = chr(6) + chr(1) + chr(2)
    DMXINTENSITY = bytes([6]) + bytes([1]) + bytes([2])

    # this code seems to initialize the communications. Char 3 is a request for the controller's
    # parameters. I didn't bother reading that data, I'm just assuming it's an init string.
    # DMXINIT1 = chr(3) + chr(2) + chr(0) + chr(0) + chr(0)
    DMXINIT1 = bytes([3]) + bytes([2]) + bytes([0]) + bytes([0]) + bytes([0])

    # likewise, char 10 requests the serial number of the unit. I'm not receiving it or using it
    # but the other softwares I tested did. You might want to.
    # DMXINIT2 = chr(10) + chr(2) + chr(0) + chr(0) + chr(0)
    DMXINIT2 = bytes([10]) + bytes([2]) + bytes([0]) + bytes([0]) + bytes([0])

    # open serial port 4. This is where the USB virtual port hangs on my machine. You
    # might need to change this number. Find out what com port your DMX controller is on
    # and subtract 1, the ports are numbered 0-3 instead of 1-4
    # this writes the initialization codes to the DMX
    ser = usb_detector.get_serial()
    logHandle.info(f"Ser :: {ser}")
    time.sleep(0.5)
    if not ser:
        logHandle.critical("Projector is not connected to the USB. Please connect and try again..")
        
    else:
        # this writes the initialization codes to the DMX
        ser.write(DMXOPEN + DMXINIT1 + DMXCLOSE)
        time.sleep(0.1)
        data = ser.read(15)
        logHandle.info("reading data on projector INIT1 {}".format(list(data)))
        if len(data) != 0:
            if list(data)[0] != 126 or list(data)[-1] != 231:
                logHandle.error("Projector not responding to init commands")
        else:
            logHandle.error("Projector not responding to init commands")
        ser.write(DMXOPEN + DMXINIT2 + DMXCLOSE)
        time.sleep(0.1)
        data = ser.read(15)
        logHandle.info("reading data on projector INIT2 {}".format(list(data), ))
        if len(data) != 0:
            if list(data)[0] != 126 or list(data)[-1] != 231:
                logHandle.error("Projector not responding to init commands")
        else:
            logHandle.error("Projector not responding to init commands")
    dmxdata = [bytes([0])] * 513
    projectorDistance = CONF_PARAMS['site']["RACK_PROJ_DISTANCE"] * 10

    def is_projector_connected(self):
        try:
            self.ser = usb_detector.get_serial()
            self.logHandle.debug("Is projector connected : {}".format(self.ser))
            if not self.ser:
                self.logHandle.error("Projector is not connected to the USB. Please connect and try again..")
                return False
            return True
        except Exception as e:
            self.logHandle.error("Projection: Exception occurred while checking projector connection {}".format(e))
            return False

    def send_dmx_data(self, data):
        """
        send_dmx_data function brings in
        the dmx value data and sends it to dmx controller
        in form of bytes.
        """
        new_data = bytes()
        for i in range(0, len(data)):
            # data[i] = chr(data[i])
            if data[PAN_FINE_CHANNEL] > 160:
                data[PAN_FINE_CHANNEL] = data[PAN_FINE_CHANNEL] - 160
                data[PAN_CHANNEL] = data[PAN_CHANNEL] + 1
            elif data[PAN_FINE_CHANNEL] < 0:
                data[PAN_FINE_CHANNEL] = 160 + data[PAN_FINE_CHANNEL]
                data[PAN_CHANNEL] = data[PAN_CHANNEL] - 1

            if data[TILT_FINE_CHANNEL] > 160:
                data[TILT_FINE_CHANNEL] = data[TILT_FINE_CHANNEL] - 160
                data[TILT_CHANNEL] = data[TILT_CHANNEL] + 1
            elif data[TILT_FINE_CHANNEL] < 0:
                data[TILT_FINE_CHANNEL] = 160 + data[TILT_FINE_CHANNEL]
                data[TILT_CHANNEL] = data[TILT_CHANNEL] - 1
            new_data += bytes([data[i]])
        # sdata = ''.join(data)
        self.logHandle.debug("Writing data on projector {}".format(self.DMXOPEN + self.DMXINTENSITY + new_data + self.DMXCLOSE))
        try:
            self.ser.write(self.DMXOPEN + self.DMXINTENSITY + new_data + self.DMXCLOSE)
            return True
        except Exception as e:
            try:
                self.ser = usb_detector.get_serial()
                if self.ser:
                    self.ser.write(self.DMXOPEN + self.DMXINTENSITY + new_data + self.DMXCLOSE)
                    return True
                else:
                    return False
            except Exception as e:
                self.logHandle.error("Projection: Error %s " % e)
                return False

    def setDmxToLight(self, DmxPan, DmxTilt, DmxPanFine, DmxTiltFine, Brightness):
        """
        setDmxToLight function takes the DMX values as parameters and sends them
        to send_dmx_data function to project light.
        """
        self.dmxdata = [0] * 513
        # Set strobe mode - 255 means still light
        self.dmxdata[STROBE_CHANNEL] = 250
        # Set dimmer value - channel 5 - min 0, max 255
        self.dmxdata[DIMMER_CHANNEL] = Brightness
        # Set color value
        self.dmxdata[COLOR_CHANNEL] = COLOR
        # Set Theta
        self.dmxdata[PAN_CHANNEL] = int(DmxPan)
        # Set Phi
        self.dmxdata[TILT_CHANNEL] = int(DmxTilt)
        # Set Theta - Fine
        self.dmxdata[PAN_FINE_CHANNEL] = int(DmxPanFine)
        # Set Pan_Fine_channel
        self.dmxdata[TILT_FINE_CHANNEL] = int(DmxTiltFine)
        # Set pattern
        self.dmxdata[PATTERN_CHANNEL] = 0
        try:
            return self.send_dmx_data(self.dmxdata)
        except Exception as e:
            self.logHandle.error("Error in sending dmx data from setdmxlight %s" % str(e))
            return False

    def calc_dmx(self, x, y, z, PAN_LEAST_COUNT, TILT_LEAST_COUNT):
        """
        DMX value calculation for given coordinates
        """
        self.msuWH = (CONF_PARAMS['site']["RACK_WIDTH"] / 2) * 10
        self.msuH = CONF_PARAMS['site']["RACK_HEIGHT"] * 10
        Y = self.msuH - y
        X = self.msuWH - x
        b = z
        horizontal_angle = math.degrees(math.atan(X / b))
        line = [X, b, Y]
        square_value = math.sqrt(math.pow(line[0], 2) + math.pow(line[1], 2) + math.pow(line[2], 2))
        # horizontal_angle = math.degrees(math.asin(line[0] / square_value))
        vertical_angle = math.degrees(math.asin(line[2] / square_value))

        self.logHandle.info("Absolute: " + str(horizontal_angle).format(".3f") + "    " + str(vertical_angle).format(".3f"))
        self.logHandle.info("pan least count: " + str(PAN_LEAST_COUNT) + "     tilt least count: " + str(TILT_LEAST_COUNT))
        self.mid_PAN = CONF_PARAMS['Normal_DMX_values']['PAN_NORMAL']
        self.tilt_norm = CONF_PARAMS['Normal_DMX_values']['TILT_NORMAL']
        
        try:
            effec_PAN = self.mid_PAN - (horizontal_angle / PAN_LEAST_COUNT)
            effec_TILT =  self.tilt_norm + (vertical_angle / TILT_LEAST_COUNT)
            return effec_PAN, effec_TILT
        except Exception as e:
            self.logHandle.error("DMX calculation Failed: %s " % str(e))

    def dectofine(self, a):
        """
        dectofine function converts the decimal dmx values to fine movement Dmx values
        """
        round_value = round(a,3)
        decimal_value = round_value - int(round_value)
        return int(decimal_value * 160)

    def get_osc_amp(self, y):
        """
        This function sets the oscillation amplitude
        according to the y coordinate of point of projection
        to avoid over oscillation
        """
        OSCILLATION_AMP = int(y)

class Display(threading.Thread):
    """
    Display class to create the display thread with the server
    """
    QDIRECTION = 1

    def __init__(self):
        super().__init__()
        self.stop_flag = True
        self.tt = threading.Thread()
        self.tt_event = threading.Event()

    def run(self) -> None:
        self.project()

    def stop(self):
        self.tt_event.set()
        time.sleep(0.03)

    def action(self, x, y, dx, dz, dtheta, BotFace):
        """
        action is the most important function where we bring in
        all the measurements and coordinates to do the calculations.
        """
        # Cross class Objects
        dmxcontrol = Dmxcontrol()
        logHandle = dmxcontrol.logHandle
        lcv = Leastcountvalue()  # Object to use the Leastcountvalue class of leastcount.py file
        # If the degree of theta deviation is greater than 3 degree we won't be able to neglect the changes
        # if dtheta >= 3:
        #     valueX = x*math.cos(dtheta)
        # else:
        #     valueX = x * 10 - (q * dx * 10)
        # Converting given coordinates from centimeters to milimeters by multiplying by 10
        if BotFace == 0:
            valueX = x * 10 + (self.QDIRECTION * dx * 10)
            valueZ = dmxcontrol.projectorDistance + (dz * 10)
        elif BotFace == 1:
            valueX = x * 10 + (dx * 10)
            valueZ = dmxcontrol.projectorDistance + (self.QDIRECTION * dz * 10)
        elif BotFace == 2:
            self.QDIRECTION = -1
            valueX = x * 10 + (self.QDIRECTION * dx * 10)
            valueZ = dmxcontrol.projectorDistance + (dz * 10)
        elif BotFace == 3:
            self.QDIRECTION = -1
            valueX = x * 10 + (dx * 10)
            valueZ = dmxcontrol.projectorDistance + (self.QDIRECTION * dz * 10)
        else:
            valueX = x * 10
            valueZ = dmxcontrol.projectorDistance
        valueY = y * 10
        osc_amp = dmxcontrol.get_osc_amp
        osc_amp(y)  # Here we are changing the amplitude for oscillations according to value of y coordinate 
        
        # calc_dmx function to find the dmx values for the given coordinates
        dmxPAN, dmxTILT = dmxcontrol.calc_dmx(valueX, valueY, valueZ, PAN_LEAST_COUNT, TILT_LEAST_COUNT)
        
        """
        Now we will fixate the mounting errors in our calculations using leastCount.py file
        """
        deltaX = lcv.mounterrorpan(dmxTILT)
        deltaY = lcv.mounterrortilt(dmxPAN)
        logHandle.info("Mount fix in X for Y tilts:" + str(deltaX))
        logHandle.info("Mount fix in Y for X pans :" + str(deltaY))
        dmxPanFine = dmxcontrol.dectofine(dmxPAN)  # dectofine function to convert floating dmx value to fine movement
        dmxTiltFine = dmxcontrol.dectofine(dmxTILT)

        # Oscillation choice decides whether we will just point at a coordinate or we will point and oscillate it
        if not OSCILLATION_CHOICE:
            try:
                dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
            except Exception as e:
                logHandle.error("Non Oscillation projection error %s" % e)
        elif OSCILLATION_CHOICE:
            while self.tt.is_alive():
                try:
                    time.sleep(0.03)
                    self.tt.join()
                except Exception as e:
                    logHandle.error("Projection and oscillation thread join error %s" % e)
            self.tt = threading.Thread(target=self.pointAndOscillate,
                                       args=(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), x * 10, y * 10))
            self.tt.start()
            # pointAndOscillate(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine))

        logHandle.info("Final PAN value for given point: %s" % int(dmxPAN))
        logHandle.info("Final PAN Fine value for given point: %s" % int(dmxPanFine))
        logHandle.info("Final TILT value for given point: %s" % int(dmxTILT))
        logHandle.info("Final TILT value for given point: %s" % int(dmxTiltFine))

    def pointAndOscillate(self, pan, tilt, pan_fine, tilt_fine, x, y):
        """
        pointAndOscillate function is used to oscillate the beam in horizontal or vertical direction while pointing at bin
        """
        try:
            dmxcontrol = Dmxcontrol()
            dmxcontrol.logHandle.info("Oscillation thread started")
            osc_direction = 1
            self.tt_event.clear()
            status = True
            tilt_temp = 0
            tilt_fine_temp = 0
            osc_amplitude = OSCILLATION_AMP
            osc_amplitude_temp = 0
            y_up_limit = (PROJ_HEIGHT / 2) * 10
            if y > y_up_limit:
                osc_amplitude = OSCILLATION_AMP_UPPER_RACK
            dmxcontrol.logHandle.debug("osc_amplitude: {}".format(osc_amplitude))
            while True:
                if self.tt_event.is_set():
                    dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                    break
                if OSCILLATION_PATTERN.lower() == "v":
                    if osc_direction == 1:
                        if (tilt_fine + osc_amplitude) > 255:
                            tilt_temp = tilt + int((tilt_fine + osc_amplitude) / 255)
                        else:
                            tilt_temp = tilt
                        tilt_fine_temp = (tilt_fine + osc_amplitude) % 255
                    elif osc_direction == -1:
                        if (tilt_fine - osc_amplitude) < 0:
                            tilt_temp = tilt - (int(osc_amplitude / 255) + 1)
                            osc_amplitude_temp = osc_amplitude % 255
                            tilt_fine_temp = 255 - (osc_amplitude_temp - tilt_fine)
                        else:
                            tilt_temp = tilt
                            tilt_fine_temp = tilt_fine - osc_amplitude
                    # dmxcontrol.logHandle.info("Tilt: {} tilt_fine: {}".format(tilt_temp, tilt_fine_temp))
                    status = dmxcontrol.setDmxToLight(pan, tilt_temp, pan_fine, tilt_fine_temp, 255)
                elif OSCILLATION_PATTERN.lower() == "h":
                    status = dmxcontrol.setDmxToLight(pan, tilt, pan_fine + (osc_direction * OSCILLATION_AMP), tilt_fine, 255)
                osc_direction = -1 * osc_direction  # We will change the oscillation directions alternatively
                if not status:
                    self.tt_event.set()
                    break
                time.sleep(0.3)
        except Exception as e:
            dmxcontrol.logHandle.error("Exception Occurred {}".format(e))
            self.tt_event.set()

    def project(self):
        """
        Project function extracts the required data from action queue and is the pivot point between main application
        script and projection script.
        """
        last_action = None
        dmxcontrol = Dmxcontrol()
        logHandle = dmxcontrol.logHandle
        while True:
            if dmxcontrol.is_projector_connected():
                break
            else:
                time.sleep(5)
        action_queue.emptyQueue()
        while True:
            msg = action_queue.get()
            if not dmxcontrol.is_projector_connected():
                logHandle.error("Projector Not connected, ignoring the event from server. Event: {}".format(msg))
                continue
            self.stop()
            time.sleep(0.1)
            if msg == "disconnected":
                self.tt_event.set()
                time.sleep(0.05)
                continue
            if msg == 'stop':
                if last_action != 'stop':
                    last_action = 'stop'
                    logHandle.info("1. Projection: lastAction updated to - %s" % last_action)
                    self.tt_event.set()
                    time.sleep(0.02)
                else:
                    logHandle.info("Projection: skipping stop, continuous 2 stop command received")
            elif len(msg) >= 5 and msg[:5] == 'point':
                if last_action != 'point':
                    last_action = 'point'
                    logHandle.info("2. Projection: lastAction updated to - %s" % last_action)
                    try:
                        [X, Y, Dx, Dz, DTheta, Qdir] = [float(s) for s in msg.split(",")[1:] if len(msg) > 14]
                        y_up_limit = (PROJ_HEIGHT / 2)
                        if Y > y_up_limit:
                            Y += UPPER_RACK_SHIFT_TUNING
                        self.action(X, Y, Dz, Dx, DTheta, Qdir)
                    except Exception as e:
                        logHandle.error("String Length mismatch error: %s" % str(e))
                else:
                    logHandle.info("Projection: continuous 2 point command received,first stopping projector then "
                                   "pointing")
                    try:
                        [X, Y, Dx, Dz, DTheta, Qdir] = [float(s) for s in msg.split(",")[1:] if len(msg) > 14]
                        y_up_limit = (PROJ_HEIGHT / 2)
                        if Y > y_up_limit:
                            Y += UPPER_RACK_SHIFT_TUNING
                        last_action = 'point'
                        logHandle.info("3. Projection: lastAction updated to: %s " % last_action)
                        self.action(X, Y, Dz, Dx, DTheta, Qdir)
                    except Exception as e:
                        logHandle.error("Projection project function error %s" % str(e))
            else:
                logHandle.info("Projection: No Action, Unrecognized message from server")
