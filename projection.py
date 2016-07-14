from config import *
from time import sleep
#  serial is PySerial, the serial port software for Python
import serial
import math
import numpy
import threading
import configparser
import pyudev

# setup the dmx
# char 126 is 7E in hex. It's used to start all DMX512 commands
DMXOPEN = chr(126)

# char 231 is E7 in hex. It's used to close all DMX512 commands
DMXCLOSE = chr(231)

# I named the "output only send dmx packet request" DMXINTENSITY as I don't have
# any moving fixtures. Char 6 is the label , I don't know what Char 1 and Char 2 mean
# but my sniffer log showed those values always to be the same so I guess it's good enough.
DMXINTENSITY = chr(6) + chr(1) + chr(2)

# this code seems to initialize the communications. Char 3 is a request for the controller's
# parameters. I didn't bother reading that data, I'm just assuming it's an init string.
DMXINIT1 = chr(03) + chr(02) + chr(0) + chr(0) + chr(0)

# likewise, char 10 requests the serial number of the unit. I'm not receiving it or using it
# but the other softwares I tested did. You might want to.
DMXINIT2 = chr(10) + chr(02) + chr(0) + chr(0) + chr(0)

# open serial port 4. This is where the USB virtual port hangs on my machine. You
# might need to change this number. Find out what com port your DMX controller is on
# and subtract 1, the ports are numbered 0-3 instead of 1-4
print "Shorlisting USB devices"
context = pyudev.Context()
usb_devices = []
for device in context.list_devices(subsystem="usb"):
    for c in device.children:
        if (c.subsystem == "usb-serial"):
            print c.sys_name
            usb_devices.append(c.sys_name)
#  Make the list unique
#  Duplicates occur due to different USB versions supported(USB 1.0, 2.0 & 3.0)
usb_devices = list(set(usb_devices))
if len(usb_devices) == 1:
    print "Successful : Single unambiguious device found"
    ser = serial.Serial("/dev/" + str(usb_devices[0]))
else:
    print "Error : more than one or no USB-DMX found"

# this writes the initialization codes to the DMX
ser.write(DMXOPEN + DMXINIT1 + DMXCLOSE)
ser.write(DMXOPEN + DMXINIT2 + DMXCLOSE)

#  this sets up an array of 513 bytes, the first item in the array ( dmxdata[0] ) is the previously
# mentioned spacer byte following the header. This makes the array math more obvious
dmxdata = [chr(0)] * 513

# senddmx accepts the 513 byte long data string to keep the state of all the channels
#  the channel number and the value for that channel
# senddmx writes to the serial port then returns the modified 513 byte array


def send_dmx_data(data):
    #  print "[DMX] Writing data :", data[1:11]
    #  print ""
    for i in range(0, len(data)):
        data[i] = chr(data[i])
    sdata = ''.join(data)
    ser.write(DMXOPEN + DMXINTENSITY + sdata + DMXCLOSE)


def senddmx(data, chan, intensity):
    #  because the spacer bit is [0], the channel number is the array item number
    #  set the channel number to the proper value
    data[chan] = chr(intensity)
    #  join turns the array data into a string we can send down the DMX
    sdata = ''.join(data)
    #  write the data to the serial port, this sends the data to your fixture
    ser.write(DMXOPEN + DMXINTENSITY + sdata + DMXCLOSE)
    #  return the data with the new value in place
    return(data)


def setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine, Brightness):
    dmxdata = [0] * 513
    #  Set strobe mode - 255 means still light
    dmxdata[STROBE_CHANNEL] = 255
    #  Set dimmer value - channel 5 - min 0, max 255
    dmxdata[DIMMER_CHANNEL] = Brightness
    #  Set Theta
    dmxdata[PAN_CHANNEL] = DmxPan
    #  Set Phi
    dmxdata[TILT_CHANNEL] = DmxTilt
    #  Set Theta - Fine
    dmxdata[PAN_FINE_CHANNEL] = DmxPanFine
    #  Set Phi - Fine
    dmxdata[TILT_FINE_CHANNEL] = DmxTiltFine
    #  Set pattern
    dmxdata[PATTERN_CHANNEL] = 0
    send_dmx_data(dmxdata)


def turnOffLight():
    dmxdata = [0] * 513
    send_dmx_data(dmxdata)


def coordinateToDmx(X, Y):
    X = float(X)
    Y = float(Y)
    #  print "[Debug] Converting (%s, %s)" % (X, Y)
    E_Pan = weighted_average(A_PAN, RACK_HEIGHT - Y, D_PAN, Y)
    E_Tilt = weighted_average(A_TILT, RACK_HEIGHT - Y, D_TILT, Y)
    #  print "[Debug] E : (%s, %s) " % (E_Theta, E_Phi)
    F_Pan = weighted_average(B_PAN, RACK_HEIGHT - Y, C_PAN, Y)
    F_Tilt = weighted_average(B_TILT, RACK_HEIGHT - Y, C_TILT, Y)
    #  print "[Debug] F : (%s, %s) " % (F_Theta, F_Phi)
    P_Pan = weighted_average(F_Pan, X, E_Pan, RACK_WIDTH - X)
    P_Tilt = weighted_average(F_Tilt, X, E_Tilt, RACK_WIDTH - X)
    #  print "Final DMX in floating point : (%s, %s)" % (X_Theta, X_Phi)
    P_Pan_Fine = (P_Pan - int(P_Pan)) * 255
    P_Tilt_Fine = (P_Tilt - int(P_Tilt)) * 255
    return (int(P_Pan), int(P_Tilt), int(P_Pan_Fine), int(P_Tilt_Fine))


def coordinateToDmx1(X, Y):
    X = float(X)
    Y = float(Y)
    print "[Debug] Converting (%s, %s)" % (X, Y)
    E_Pan = weighted_average(A_PAN, RACK_HEIGHT - Y, D_PAN, Y)
    # E_Tilt = weighted_average(A_TILT, RACK_HEIGHT - Y, D_TILT, Y)
    # print "[Debug] E : (%s, %s) " % (E_Pan, E_Tilt)
    F_Pan = weighted_average(B_PAN, RACK_HEIGHT - Y, C_PAN, Y)
    # F_Tilt = weighted_average(B_TILT, RACK_HEIGHT - Y, C_TILT, Y)

    AD_Theta = math.degrees(math.atan2(RACK_ORIGIN_DISTANCE, RACK_PROJ_DISTANCE))
    BC_Theta = math.degrees(math.atan2(RACK_ORIGIN_DISTANCE - RACK_WIDTH, RACK_PROJ_DISTANCE))
    P_Theta = math.degrees(math.atan2(RACK_ORIGIN_DISTANCE - X, RACK_PROJ_DISTANCE))
    print "AD_Theta = %s, BC_Theta = %s, P_Theta = %s" % (AD_Theta, BC_Theta, P_Theta)
    P_Pan = E_Pan + (F_Pan - E_Pan) * (P_Theta - AD_Theta) / (BC_Theta - AD_Theta)
    P_Pan_Fine = (P_Pan - int(P_Pan)) * 255

    RackProjDistanceCorrected = math.sqrt(RACK_PROJ_DISTANCE ** 2 + (RACK_ORIGIN_DISTANCE - X) ** 2)
    print "Correction is:", (RackProjDistanceCorrected - RACK_PROJ_DISTANCE)
    Phi = math.degrees(math.atan((PROJ_HEIGHT - Y) / RackProjDistanceCorrected))
    D_Phi = math.degrees(math.atan((PROJ_HEIGHT - RACK_HEIGHT) / RackProjDistanceCorrected))
    A_Phi = math.degrees(math.atan(PROJ_HEIGHT / RackProjDistanceCorrected))
    G_Tilt = weighted_average(A_TILT, RACK_WIDTH - X, B_TILT, X)
    H_Tilt = weighted_average(D_TILT, RACK_WIDTH - X, C_TILT, X)

    P_Tilt = ((G_Tilt - H_Tilt) * (Phi - D_Phi)) / (A_Phi - D_Phi) + H_Tilt
    P_Tilt_Fine = (P_Tilt - int(P_Tilt)) * 255
    return (int(P_Pan), int(P_Tilt), int(P_Pan_Fine), int(P_Tilt_Fine))


def coordinateToDmxGeometry(X, Y):
    X = float(X)
    Y = float(Y)
    TanPhiA = math.tan(math.radians(dmxToPhiDegrees(A_TILT)))
    TanPhiD = math.tan(math.radians(dmxToPhiDegrees(D_TILT)))
    TanPhiX = (-TanPhiA / (TanPhiA - TanPhiD)) + (Y / RACK_HEIGHT)
    PhiX = math.degrees(math.atan(TanPhiX)) + PHI_OFFSET_DEGREES
    #  print "[Debug] TanPhiA =", TanPhiA, " TanPhiD =", TanPhiD, "PhiX =", PhiX
    P_Tilt, P_Tilt_Fine = phiToDmx(PhiX)
    P_Pan, _, P_Pan_Fine, _ = coordinateToDmx1(X, Y)
    return (P_Pan, P_Tilt, P_Pan_Fine, P_Tilt_Fine)


def weighted_average(a1, w1, a2, w2):
    return (a1 * w1 + a2 * w2) / (w1 + w2)


def dmxToThetaDegrees(DmxValue):
    return numpy.interp(DmxValue, [0, 255], [THETA_MIN_DEG, THETA_MAX_DEG])


def dmxToPhiDegrees(DmxValue):
    return numpy.interp(DmxValue, [0, 255], [PHI_MIN_DEG, PHI_MAX_DEG])


def phiToDmx(Phi):
    DmxValue = numpy.interp(Phi, [PHI_MIN_DEG, PHI_MAX_DEG], [0, 255])
    return (int(DmxValue), int((DmxValue % 1) * 255))  # Two channel values : Coarse & fine


def thetaToDmx(Theta):
    DmxValue = numpy.interp(Phi, [THETA_MIN_DEG, THETA_MAX_DEG], [0, 255])
    return (int(DmxValue), int((DmxValue % 1) * 255))  # Two channel values : Coarse & fine


def distanceFromNearestInt(x):
    delta = x - int(x)
    if delta > 0.5:
        return 1 - delta
    else:
        return delta


def setCoordinateToLight(X, Y, Brightness=255):
    X = float(X)
    Y = float(Y)
    #  offset = Y * SCALE_OFFSET * distanceFromNearestInt(1.0 - Y / RACK_HEIGHT)
    #  print "Applying offset of :", offset
    #  Y = Y + offset
    DmxPan, DmxTilt, DmxPanFine, DmxTiltFine = coordinateToDmx1(X, Y)
    print "[Debug] Final DMX values for (%s, %s) Pan: (%s, %s), Tilt: (%s, %s)" % (X, Y, DmxPan, DmxPanFine, DmxTilt, DmxTiltFine)
    setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine, Brightness)


def setPhiOffset(NewPhiOffset):
    global PHI_OFFSET_DEGREES
    PHI_OFFSET_DEGREES = NewPhiOffset


class Display(object):

    """docstring for ClassName"""

    def __init__(self):
        self.stop_flag = True
        self.t = threading.Thread()

    def stop(self):
        self.stop_flag = True

    def pointAndOscillate(self, X, Y):
        if self.t.isAlive():
            return "Cannot start thread, another thread started"
        else:
            self.stop_flag = False
            setCoordinateToLight(X, Y, 0)
            sleep(0.5)
            self.t = threading.Thread(target=self.pointAndOscillateInternal, args=(X, Y))
            self.t.start()
            return "Point & Oscillate thread started successfully"

    def pointAndOscillateInternal(self, X, Y):
        while(self.stop_flag is False):
            setCoordinateToLight(X, Y + OSCILLATION_AMP)
            sleep(OSCILLATION_TIME_PERIOD)
            setCoordinateToLight(X, Y - OSCILLATION_AMP)
            sleep(OSCILLATION_TIME_PERIOD)
        if self.stop_flag:
            turnOffLight()


def loadCalibrationData(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    global A_PAN, A_TILT, B_PAN, B_TILT, C_PAN, C_TILT, D_PAN, D_TILT

    A_PAN = float(config['DEFAULT']['a_pan']) + float(config['DEFAULT']['a_pan_fine']) / 255
    A_TILT = float(config['DEFAULT']['a_tilt']) + float(config['DEFAULT']['a_tilt_fine']) / 255

    B_PAN = float(config['DEFAULT']['b_pan']) + float(config['DEFAULT']['b_pan_fine']) / 255
    B_TILT = float(config['DEFAULT']['b_tilt']) + float(config['DEFAULT']['b_tilt_fine']) / 255

    C_PAN = float(config['DEFAULT']['c_pan']) + float(config['DEFAULT']['c_pan_fine']) / 255
    C_TILT = float(config['DEFAULT']['c_tilt']) + float(config['DEFAULT']['c_tilt_fine']) / 255

    D_PAN = float(config['DEFAULT']['d_pan']) + float(config['DEFAULT']['d_pan_fine']) / 255
    D_TILT = float(config['DEFAULT']['d_tilt']) + float(config['DEFAULT']['d_tilt_fine']) / 255
    print "Loaded calibration data from :", str(filename)

'''
This function is for testing the projector,
points to locations marked on the chart paper
'''


def testLoop():
    for x in range(0, int(RACK_WIDTH) + 1, 15):
        for y in range(0, int(RACK_HEIGHT) + 1, 40):
            setCoordinateToLight(x, y)
            sleep(1.5)

loadCalibrationData('corner_points.cfg')
display = Display()

#  display.pointAndOscillate(0, 0)
#  print "Oscillation thread started"
#  sleep(100)
#  print "stopping pointing"
#  display.stop()
#  sleep(1)
#  print "Started another thread"
#  display.pointAndOscillate(25, 90)
#  sleep(2)
#  print "stopping the 2nd thread"
#  display.stop()
