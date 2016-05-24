import time
import config
import array
import time
from ola.ClientWrapper import ClientWrapper
wrapper = ClientWrapper()


def DmxSent(state):
    wrapper.Stop()

def send_dmx_internal(raw_data):
    data = array.array('B', raw_data)
    print "[DMX] Data sent to ola:", data
    wrapper.Client().SendDmx(1, data, DmxSent)
    wrapper.Run()

def coordinateToDMX(X, Y):
    Theta = config.MinTheta + (X - config.MinX) / (config.MaxX - config.MinX) * (config.MaxTheta-config.MinTheta)
    Phi   = config.MinPhi + (X - config.MinX) / (config.MaxX - config.MinX) * (config.MaxPhi-config.MinPhi)
    return (Theta, Phi)

def setDmxToLight(X, Y):
    Theta, Phi = X, Y
    raw_data = [
        int(Theta), 
        int(Phi), 
        255,   # Strobe 
        0,     # Color Wheel
        30,   # Dimmer
        0,     # Dimmer Mode
        ]
    send_dmx_internal(raw_data)

def turnOffLight():
    raw_data = [0, 0, 0, 0, 0, 0]
    send_dmx_internal(raw_data)    

for i in range(128, 255, 10):
    for j in range(1, 100, 10):
        setDmxToLight(i, j)
        time.sleep(1)

turnOffLight()


