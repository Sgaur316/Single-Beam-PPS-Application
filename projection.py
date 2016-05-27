import config # Config file
import time
#serial is PySerial, the serial port software for Python
import serial
import math

# Define DMX Channels - specific to "InnoPocket Scan" projector
THETA_CHANNEL   = 1
PHI_CHANNEL     = 2
STROBE_CHANNEL  = 3
PATTERN_CHANNEL = 4
DIMMER_CHANNEL  = 5

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
    print "[Debug] Converting (%s, %s)" % (X,Y)
    TanTheta  = (config.RACK_ORIGIN - float(X)) / (config.P_HORIZONTAL) 
    TanPhi    = (config.P_HORIZONTAL) / (config.P_VERTICAL - float(Y))
    print "[Debug] TanTheta = %s TanPhi = %s" % (TanTheta, TanPhi)
    Theta     = math.degrees(math.atan(TanTheta)) 
    Phi       = math.degrees(math.atan(TanPhi))
    print "[Debug] Theta = %s Phi = %s" % (Theta, Phi)
    DMX_Theta = int ( (90 - Theta) / 180 * 255 )
    DMX_Phi   = int ( (Phi % 180) / 180 * 255 )
    return (DMX_Theta, DMX_Phi)

def setCoordinateToLight(X, Y):
    Theta, Phi = coordinateToDmx(X, Y)
    setDmxToLight(Theta, Phi)

####################### Test ####################### 

    