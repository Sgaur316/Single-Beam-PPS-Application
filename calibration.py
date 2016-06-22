import curses
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
DmxPan       = 0
DmxPanFine   = 0
DmxTilt      = 0
DmxTiltFine  = 0

key = ''
fineMode = False

def redrawCustomScreen():
    # Repaints the enire screen : a work around for the problems
    # caused by print statements in other modules
    global stdscr
    stdscr.clear()
    stdscr.addstr(0, 0, "Calibrating the projector : Hit 'q' to quit")
    stdscr.addstr(1, 0, "Current DMX Values are %s, %s, %s, %s" % (
        DmxPan, DmxTilt, DmxPanFine, DmxTiltFine))
    stdscr.addstr(2, 0, "Currently setting for point A")
    stdscr.addstr(3, 0, "Last Key pressed : " + str(key))
    stdscr.addstr(4, 0, "Fine channels mode : " + str(fineMode))
    stdscr.refresh()

while True:
    key = stdscr.getch()
    stdscr.refresh()

    if key == curses.KEY_UP:
        # stdscr.addstr(2, 0, "Last Key pressed : Up")
        if fineMode:
            DmxTiltFine += 1
        else:
            DmxTilt += 1

    elif key == curses.KEY_DOWN:
        # stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        if fineMode:
            DmxTiltFine -= 1
        else:
            DmxTilt -= 1

    elif key == curses.KEY_LEFT:
        # stdscr.addstr(2, 0, "Last Key pressed : Left\n")
        if fineMode:
            DmxPanFine -= 1
        else:
            DmxPan -= 1

    elif key == curses.KEY_RIGHT:
        # stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        if fineMode:
            DmxPanFine += 1
        else:
            DmxPan += 1

    elif key == ord('f') or key == ord('F'):
        # Flip the fine mode
        fineMode = not fineMode

    elif key == ord('w') or key == ord('W'):
        # write config to file
        break

    elif key == ord('q'):
        break

    for dmxValue in [DmxPan, DmxTilt, DmxPanFine, DmxTiltFine] :
        if dmxValue < 0 or dmxValue > 255:
            stdscr.addstr(5, 0, "Invalid DMX values detected, setting everything to zero. Press any key to restore")
            stdscr.getch()
            stdscr.refresh()
            DmxPan       = 0
            DmxPanFine   = 0
            DmxTilt      = 0
            DmxTiltFine  = 0
            break

    setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine)
    redrawCustomScreen()

curses.endwin()