from projection import *


# while True:
#     for Phi in [0, 255]:
#         setCoordinateToLight(0, Phi)
#         time.sleep(1)
while True:
    for i in range(0, 100):
        setCoordinateToLight(i, 0)
        time.sleep(1)

while True:
    for i,j in [(0,0), (1,0), (80,0), (80, 550), (0,550)]:
        setCoordinateToLight(i, j)
        time.sleep(1)