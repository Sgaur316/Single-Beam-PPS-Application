import curses, sys

def setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine):
    print "Mock output DMX : ", DmxPan, DmxTilt, DmxPanFine, DmxTiltFine

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# stdscr.addstr(0,0,"Calibrating the projector : Hit 'q' to quit")
stdscr.refresh()

# DMX Calibration params
DmxPan       = 0 
DmxPanFine   = 0
DmxTilt      = 0
DmxTiltFine  = 0

key = ''
while True:
    key = stdscr.getch()
    stdscr.refresh()
    if key == curses.KEY_UP: 
        print "test "
        # stdscr.addstr(2, 0, "Last Key pressed : Up")
        DmxTilt += 1
                
    elif key == curses.KEY_DOWN: 
        stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        DmxTilt -= 1
    
    elif key == curses.KEY_LEFT:
        stdscr.addstr(2, 0, "Last Key pressed : Left\n")
        DmxPan -= 1

    elif key == curses.KEY_RIGHT:
        stdscr.addstr(2, 0, "Last Key pressed : Down\n")
        DmxPan += 1
    
    elif  key == ord('q'):
        break 

    for dmxValue in [DmxPan, DmxTilt, DmxPanFine, DmxTiltFine] :
        if dmxValue < 0 or dmxValue > 255:
            stdscr.addstr(2, 0, "Invalid DMX values detected, setting everything to zero\n")
            DmxPan       = 0 
            DmxPanFine   = 0
            DmxTilt      = 0
            DmxTiltFine  = 0

    setDmxToLight(DmxPan, DmxTilt, DmxPanFine, DmxTiltFine)
    # stdscr.addstr(0,0,"Calibrating the projector : Hit 'q' to quit")
    # stdscr.refresh()
    sys.stdout.flush()

curses.endwin()

