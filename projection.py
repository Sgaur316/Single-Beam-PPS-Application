import config # Config file
from config import *
import time
#serial is PySerial, the serial port software for Python
import serial
import math
import numpy

#setup the dmx
#char 126 is 7E in hex. It's used to start all DMX512 commands
DMXOPEN=chr(126)

#char 231 is E7 in hex. It's used to close all DMX512 commands
DMXCLOSE=chr(231)

#I named the "output only send dmx packet request" DMXINTENSITY as I don't have
#any moving fixtures. Char 6 is the label , I don't know what Char 1 and Char 2 mean
#but my sniffer log showed those values always to be the same so I guess it's good enough.
DMXINTENSITY=chr(6)+chr(1)+chr(2)

#this code seems to initialize the communications. Char 3 is a request for the controller's
#parameters. I didn't bother reading that data, I'm just assuming it's an init string.
DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)

#likewise, char 10 requests the serial number of the unit. I'm not receiving it or using it
#but the other softwares I tested did. You might want to.
DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)

#open serial port 4. This is where the USB virtual port hangs on my machine. You
#might need to change this number. Find out what com port your DMX controller is on
#and subtract 1, the ports are numbered 0-3 instead of 1-4
ser=serial.Serial("/dev/ttyUSB0")

#this writes the initialization codes to the DMX
ser.write( DMXOPEN+DMXINIT1+DMXCLOSE)
ser.write( DMXOPEN+DMXINIT2+DMXCLOSE)

# this sets up an array of 513 bytes, the first item in the array ( dmxdata[0] ) is the previously
#mentioned spacer byte following the header. This makes the array math more obvious
dmxdata = [chr(0)]*513

#senddmx accepts the 513 byte long data string to keep the state of all the channels
# the channel number and the value for that channel
#senddmx writes to the serial port then returns the modified 513 byte array

def send_dmx_data(data):
    print "[DMX] Writing data :", data[1:6]
    print ""
    for i in range(0, len(data)):
        data[i] = chr(data[i])
    sdata=''.join(data)
    ser.write(DMXOPEN+DMXINTENSITY+sdata+DMXCLOSE)
 
def senddmx(data, chan, intensity):
    # because the spacer bit is [0], the channel number is the array item number
    # set the channel number to the proper value
    data[chan]=chr(intensity)
    # join turns the array data into a string we can send down the DMX
    sdata=''.join(data)
    # write the data to the serial port, this sends the data to your fixture
    ser.write(DMXOPEN+DMXINTENSITY+sdata+DMXCLOSE)
    # return the data with the new value in place
    return(data)

def setDmxToLight(Theta, Phi):
    dmxdata = [0]*513
    # Set strobe mode - 255 means still light
    dmxdata[STROBE_CHANNEL] = 255
    # Set dimmer value - channel 5 - min 0, max 255
    dmxdata[DIMMER_CHANNEL] = 255
    # Set Theta
    dmxdata[THETA_CHANNEL] = Theta
    # Set Phi
    dmxdata[PHI_CHANNEL] = Phi
    # Set pattern
    dmxdata[PATTERN_CHANNEL] = 0 
    send_dmx_data(dmxdata)

def turnOffLight():
    dmxdata=[0]*513
    send_dmx_data(dmxdata)

def coordinateToDmxSimple(X, Y):
    Theta = config.MinTheta + (X - config.MinX) / (config.MaxX - config.MinX) * (config.MaxTheta-config.MinTheta)
    Phi   = config.MinPhi + (X - config.MinX) / (config.MaxX - config.MinX) * (config.MaxPhi-config.MinPhi)
    return (Theta, Phi)

def coordinateToDmx(X, Y):
    X = float(X)
    Y = float(Y)
    print "[Debug] Converting (%s, %s)" % (X, Y)
    E_Theta = divide(A_THETA, RACK_HEIGHT - Y, D_THETA, Y)
    E_Phi   = divide(A_PHI, RACK_HEIGHT - Y, D_PHI, Y)
    print "[Debug] E : (%s, %s) " % (E_Theta, E_Phi)
    F_Theta = divide(B_THETA, RACK_HEIGHT - Y, C_THETA, Y)
    F_Phi   = divide(B_PHI, RACK_HEIGHT - Y, C_PHI, Y)
    print "[Debug] F : (%s, %s) " % (F_Theta, F_Phi)
    X_Theta = divide(F_Theta, X, E_Theta, RACK_WIDTH - X)
    X_Phi   = divide(F_Phi, Y, E_Phi, RACK_HEIGHT - Y)
    return (int(X_Theta), int(X_Phi))

def divide(a1, w1, a2, w2):
    return (a1*w1 + a2*w2) / (w1+w2)

def dmxToThetaDegrees(DmxValue):
    return numpy.interp(Dmxvalue, [0, 255], [THETA_MIN_DEG, THETA_MAX_DEG])

def dmxToPhiDegrees(Dmxvalue):
    return numpy.interp(Dmxvalue, [0, 255], [PHI_MIN_DEG, PHI_MAX_DEG])

def phiToDmx(Phi):
    return int( numpy.interp(Phi, [PHI_MIN_DEG, PHI_MAX_DEG], [0, 255]) )

def thetaToDmx(Theta):
    return int( numpy.interp(Phi, [THETA_MIN_DEG, THETA_MAX_DEG], [0, 255]) )

def setCoordinateToLight(X, Y):
    DmxPan, DmxTilt = coordinateToDmx(X, Y)
    print "[Debug] Final DMX values (%s, %s)" % (DmxPan, DmxTilt)
    print "[Debug] Final Theta: %s, Phi: %s" % (dmxToThetaDegrees(DmxPan), dmxToPhiDegrees(DmxTilt))
    setDmxToLight(DmxPan, DmxTilt)

####################### Test ####################### 
