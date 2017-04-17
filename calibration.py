import curses
import configparser
import projection
from time import sleep


def setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine):
    print "Mock output DMX : ", DmxPan, DmxTilt, DmxPanFine, DmxTiltFine

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

stdscr.addstr(0, 0, "Calibrating the projector : Hit 'q' to quit")
stdscr.refresh()

# DMX Calibration params
DmxPan = 0
DmxPanFine = 0
DmxTilt = 0
DmxTiltFine = 0

key = ''
fineMode = False
pointsList = ['a', 'b', 'c', 'd']
currentPoint = 'a'

# Read from the config file
config = configparser.ConfigParser()
config.read('corner_points.cfg')


def isValidDmx(value):
    return value >= 0 and value <= 255


def increaseByOne(dmxValue):
    incremented = dmxValue + 1
    if isValidDmx(incremented):
        return incremented
    else:
        return dmxValue   # Return unchanged value


def decreaseByOne(dmxValue):
    decremented = dmxValue - 1
    if isValidDmx(decremented):
        return decremented
    else:
        return dmxValue   # Return unchanged value


def redrawCustomScreen():
    # Repaints the enire screen : a work around for the problems
    # caused by print statements in other modules
    global stdscr
    stdscr.clear()
    stdscr.addstr(0, 0, "Calibrating the projector : Hit 'q' to quit")
    stdscr.addstr(1, 0, "Current DMX Values are %s, %s, %s, %s" % (
        DmxPan, DmxTilt, DmxPanFine, DmxTiltFine))
    stdscr.addstr(2, 0, "Currently setting for point : " + currentPoint)
    stdscr.addstr(3, 0, "Last Key pressed : " + str(key))
    stdscr.addstr(4, 0, "Fine channels mode : " + str(fineMode))
    stdscr.refresh()


def showEndScreen():
    redrawCustomScreen()
    stdscr.addstr(5, 0, "Written to config file, press any key to exit!!!")

while pointsList != []:
    key = stdscr.getch()
    stdscr.refresh()

    if key == curses.KEY_UP:
        # stdscr.addstr(2, 0, "Last Key pressed : Up")
        if fineMode:
            DmxTiltFine = increaseByOne(DmxTiltFine)
        else:
            DmxTilt = increaseByOne(DmxTilt)

    elif key == curses.KEY_DOWN:
        # stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        if fineMode:
            DmxTiltFine = decreaseByOne(DmxTiltFine)
        else:
            DmxTilt = decreaseByOne(DmxTilt)

    elif key == curses.KEY_LEFT:
        # stdscr.addstr(2, 0, "Last Key pressed : Left\n")
        if fineMode:
            DmxPanFine = decreaseByOne(DmxPanFine)
        else:
            DmxPan = decreaseByOne(DmxPan)

    elif key == curses.KEY_RIGHT:
        # stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        if fineMode:
            DmxPanFine = increaseByOne(DmxPanFine)
        else:
            DmxPan = increaseByOne(DmxPan)

    elif key == ord('f') or key == ord('F'):
        # Flip the fine mode
        fineMode = not fineMode

    elif key == ord('w') or key == ord('W'):
        # write config to file
        config['DEFAULT'][currentPoint + '_pan'] = str(DmxPan)
        config['DEFAULT'][currentPoint + '_pan_fine'] = str(DmxPanFine)
        config['DEFAULT'][currentPoint + '_tilt'] = str(DmxTilt)
        config['DEFAULT'][currentPoint + '_tilt_fine'] = str(DmxTiltFine)
        pointsList.remove(currentPoint)
        if pointsList == []:
            with open('corner_points.cfg', 'w') as configfile:
                config.write(configfile)
            showEndScreen()
            stdscr.getch()
            break
        else:
            currentPoint = pointsList[0]

    elif key == ord('q'):
        break

    for dmxValue in [DmxPan, DmxTilt, DmxPanFine, DmxTiltFine]:
        if dmxValue < 0 or dmxValue > 255:
            stdscr.addstr(5, 0, "Invalid DMX values detected, setting everything to zero. Press any key to restore")
            stdscr.getch()
            stdscr.refresh()
            DmxPan = 0
            DmxPanFine = 0
            DmxTilt = 0
            DmxTiltFine = 0
            break

    projection.setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine, 255)
    redrawCustomScreen()

curses.endwin()
