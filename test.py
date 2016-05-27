from projection import *

setDmxToLight(128, 0)
time.sleep(1)
setDmxToLight(128, 255)


for i in range(0, 100):
    setCoordinateToLight(0, i)
    time.sleep(0.1)