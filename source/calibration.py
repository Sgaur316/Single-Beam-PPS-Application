""" Calibration file is where we set the parameters and sets up our projection file according to the onsite situation"""
# importing libraries
import sys

sys.path.append('./')
import curses
import json
from source.projection import Dmxcontrol
from source.leastCount import Leastcountvalue
from config import CONF_PARAMS
from source import logger

logHandle = logger.logHandle

class Calibration():
    cal_mode = '0'
    # using curses library for keyboard interactions and canvas control
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.refresh()

    # DMX Calibration params
    DmxPan = 0
    DmxPanFine = 0
    DmxTilt = 0
    DmxTiltFine = 0

    key = ''
    fineMode = False
    # We only need to calibrate 3 points of the MSU adding the 4th point adds complexity to mounting error handling
    pointsList = ['a', 'b', 'c']
    currentPoint = 'a'

    # Global variables for pan and tilt least counts
    pan_lcv = CONF_PARAMS["Least_Counts"]["panLeastCount"]
    tilt_lcv = CONF_PARAMS["Least_Counts"]["tiltLeastCount"]

    # To keep our Dmx values in valid range
    def isValidDmx(self, value):
        return 0 <= value <= 255

    def upd_lcv(self, x, c, v):
        try:
            val = 0
            if v == 1:
                val = x + 0.005
            elif v == -1:
                val = x - 0.005
            if c == 0:
                CONF_PARAMS["Least_Counts"]["panLeastCount"] = val
            elif c == 1:
                CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = val
        except Exception as e:
            logHandle.error("Advanced calibration LCV inundation error %s"% str(e))

    def lcv_adjustment(self):
        """
                LCV stands for "Least Count Value"
        lcv_adjustment function is used for tuning the least count values to increase flexibility and gain scenario
        independency, Projectors may show different pan tilt angles covered for a single Dmx value change which makes it a
        mechanically dependent variable and is exactly what the least count is.
            So in order to manage the span of movement of projection beam for any angle totally depends on the least count value, it can be regulated from this function.
        """
        while True:
            dmxcontrol = Dmxcontrol()
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, " PAN_LCV : %s" % CONF_PARAMS["Least_Counts"]["panLeastCount"])
            self.stdscr.addstr(1, 0, " TILT_LCV : %s" % CONF_PARAMS["Least_Counts"]["tiltLeastCount"])
            self.stdscr.addstr(2, 0,
                          "Adjust the least count value in order to accumulate the projection span inaccuracy(e.g. "
                          "reducing TILT_LCV will push and increase the tilt motion range downwards.i.e. Increases "
                          "the Tilt DMX value).")
            self.stdscr.addstr(3, 0, "Press 'E' to exit this prompt: ")

            try:
                key = self.stdscr.getch()
                self.stdscr.refresh()
                # here set dmx light to zero
                if key == curses.KEY_UP:
                    tilt_lcv = self.tilt_lcv + 0.005
                    formatted_string = "{:.3f}".format(tilt_lcv)
                    tilt_lcv = float(formatted_string)
                    CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = tilt_lcv

                elif key == curses.KEY_DOWN:
                    tilt_lcv = self.tilt_lcv - 0.005
                    formatted_string = "{:.3f}".format(tilt_lcv)
                    tilt_lcv = float(formatted_string)
                    CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = tilt_lcv

                elif key == curses.KEY_LEFT:
                    pan_lcv = self.pan_lcv - 0.001
                    formatted_string = "{:.3f}".format(pan_lcv)
                    pan_lcv = float(formatted_string)
                    CONF_PARAMS["Least_Counts"]["panLeastCount"] = pan_lcv

                elif key == curses.KEY_RIGHT:
                    pan_lcv = self.pan_lcv + 0.001
                    formatted_string = "{:.3f}".format(pan_lcv)
                    pan_lcv = float(formatted_string)
                    CONF_PARAMS["Least_Counts"]["panLeastCount"] = pan_lcv

                elif key == ord('e') or key == ord('E'):
                    with open(r'./config/config.json', 'r+') as conf:
                        json.dump(CONF_PARAMS, conf, indent=4)

                    # set update dmx according to new lcv value
                    dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    curses.endwin()
                    break
            except KeyboardInterrupt:
                dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                self.stdscr.clear()
                self.stdscr.refresh()
                curses.endwin()
                break

    # A simple function to increment the dmx value by one
    def increaseByOne(self, dmxValue):
        incremented = dmxValue + 1
        if self.isValidDmx(incremented):
            return incremented
        else:
            return dmxValue  # Return unchanged value

    def decreaseByOne(self, dmxValue):
        """
            Logically opposite of the above function, decreases the dmx value by one.
        """
        decremented = dmxValue - 1
        if self.isValidDmx(decremented):
            return decremented
        else:
            return dmxValue  # Return unchanged value

    def redrawCustomScreen(self):
        """
        This function is used to draw custom curtain screen for direct user-device interaction

        """
        try:
            self.stdscr.clear()
        # Repaints the enire screen : a work around for the problems
        # caused by print statements in other modules
            self.stdscr.addstr(0, 0, "Calibrating the projector : Hit 'q' to quit")
            self.stdscr.addstr(1, 0, "Current DMX Values are %s, %s, %s, %s" % (
                self.DmxPan, self.DmxTilt, self.DmxPanFine, self.DmxTiltFine))
            self.stdscr.addstr(2, 0, "Currently setting for point : " + self.currentPoint)
            self.stdscr.addstr(3, 0, "Last Key pressed : " + str(self.key))
            self.stdscr.addstr(4, 0, "Fine channels mode : " + str(self.fineMode))
            self.stdscr.refresh()
        except Exception as e:
            logHandle.error("Screen Draw error %s"% str(e))

    def showEndScreen(self):
        """
         Support function for redrawCustomScreen function
        """
        self.redrawCustomScreen()
        self.stdscr.addstr(5, 0, "Written to config file, press any key to exit!!!")

    def showStartScreen(self):
        """
            Support function for redrawCustomScreen function
        """
        self.stdscr.addstr(0,0, "Select the calibration mode:\n1. MSU measurements from ground,\n2. Base Station "
                                "Calibration, \n3. Advanced Calibration: \n")
        while True:
            try:
                choice = self.stdscr.getch()
                self.stdscr.refresh()
                if choice == 49:
                    self.cal_mode = "1"
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(4, 0, self.cal_mode)
                elif choice == 50:
                    self.cal_mode = "2"
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(4, 0, self.cal_mode)
                elif choice == 51:
                    self.cal_mode = "3"
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(4, 0, self.cal_mode)
                elif choice == ord("\n"):
                    break
                elif choice == curses.KEY_BACKSPACE:
                    self.cal_mode = "0"
                    self.stdscr.clrtoeol()
                else:
                    self.stdscr.addstr(4, 0, "Invalid Input")
                    self.cal_mode = "0"
            except Exception as e:
                logHandle.error("Start Screen error: %s" % e)

    def measrementcalibrations(self):
        """
        This function runs the application in measurement input mode.
        """
        try:
            oscillation_choice = CONF_PARAMS["dev"]["OSCILLATION_CHOICE"]
            self.stdscr.clear()
            curses.echo()
            self.stdscr.addstr(0, 0, "MSU Rack Width: \n")
            CONF_PARAMS["site"]["RACK_WIDTH"] = float(self.stdscr.getstr(1,0,2))
            self.stdscr.addstr(2, 0, "MSU Rack Base Height from ground: \n")
            CONF_PARAMS["site"]["RACK_BASE_HEIGHT"] = float(self.stdscr.getstr(3,0,2))
            self.stdscr.addstr(4, 0, "Projector Height from ground: \n")
            CONF_PARAMS["site"]["PROJ_HEIGHT"] = float(self.stdscr.getstr(5,0,3))
            self.stdscr.addstr(6, 0, "Set Oscillation True or False by pressing 'F': \n")
            while True:
                choice = self.stdscr.getch()
                if choice == ord('f') or choice == ord('F'):
                    oscillation_choice = not oscillation_choice
                    self.stdscr.addstr(7, 0, str(oscillation_choice))
                elif choice == ord('\n'):
                    CONF_PARAMS["dev"]["OSCILLATION_CHOICE"] = oscillation_choice
                    break
            CONF_PARAMS["site"]["RACK_HEIGHT"] = CONF_PARAMS["site"]["PROJ_HEIGHT"] - CONF_PARAMS["site"]["RACK_BASE_HEIGHT"]
            with open(r'./config/config.json', 'w') as con:
                json.dump(CONF_PARAMS, con, indent=4)
            curses.endwin()
        except Exception as e:
            logHandle.error("measurement calibration mode error: %s" % e)


    def finetodec(self, a) -> float:
        return a / 255

    # dectofine function is used for converting decimal value to fine mode dmx values
    def dectofine(self, a):
        return int((a % 1) * 255)

    # Main function of the script to run the calibration application
    def calibrate(self):
        dmxcontrol = Dmxcontrol()
        lcv = Leastcountvalue()
        self.showStartScreen()
        if self.cal_mode == '1':
            self.measrementcalibrations()
            # CONF_PARAMS["site"]["RACK_WIDTH"] = float(input("MSU Rack Width: \n"))
            # CONF_PARAMS["site"]["RACK_BASE_HEIGHT"] = float(input("MSU Rack Base Height from ground: \n"))
            # CONF_PARAMS["site"]["PROJ_HEIGHT"] = float(input("Projector Height from ground: \n"))
            # CONF_PARAMS["dev"]["OSCILLATION_CHOICE"] = bool(input("Set Oscillation True or False "
            #                                                       "respectively: \n"))
            # CONF_PARAMS["site"]["RACK_HEIGHT"] = CONF_PARAMS["site"]["PROJ_HEIGHT"] - CONF_PARAMS["site"][
            #     "RACK_BASE_HEIGHT"]
            #
            # with open(r'./config/config.json', 'w') as con:
            #     json.dump(CONF_PARAMS, con, indent=4)

        elif self.cal_mode == '2':
            while self.pointsList:
                try:
                    key = self.stdscr.getch()
                    self.stdscr.refresh()

                    if key == curses.KEY_UP:

                        if self.fineMode:
                            self.DmxTiltFine = self.increaseByOne(self.DmxTiltFine)
                        else:
                            self.DmxTilt = self.increaseByOne(self.DmxTilt)

                    elif key == curses.KEY_DOWN:

                        if self.fineMode:
                            self.DmxTiltFine = self.decreaseByOne(self.DmxTiltFine)
                        else:
                            self.DmxTilt = self.decreaseByOne(self.DmxTilt)

                    elif key == curses.KEY_LEFT:
                        if self.fineMode:
                            self.DmxPanFine = self.decreaseByOne(self.DmxPanFine)
                        else:
                            self.DmxPan = self.decreaseByOne(self.DmxPan)
                            self.DmxTiltFine = self.DmxTiltFine
                    elif key == curses.KEY_RIGHT:
                        if self.fineMode:
                            self.DmxPanFine = self.increaseByOne(self.DmxPanFine)
                        else:
                            self.DmxPan = self.increaseByOne(self.DmxPan)

                    elif key == ord('f') or key == ord('F'):
                        # Flip the fine mode
                        self.fineMode = not self.fineMode

                    elif key == ord('w') or key == ord('W'):
                        # write config to file
                        CONF_PARAMS['corner_points'][self.currentPoint + '_pan'] = self.DmxPan
                        CONF_PARAMS['corner_points'][self.currentPoint + '_pan_fine'] = self.DmxPanFine
                        CONF_PARAMS['corner_points'][self.currentPoint + '_tilt'] = self.DmxTilt
                        CONF_PARAMS['corner_points'][self.currentPoint + '_tilt_fine'] = self.DmxTiltFine
                        self.pointsList.remove(self.currentPoint)
                        if not self.pointsList:
                            a_pan = float(CONF_PARAMS['corner_points']['a_pan']) \
                                    + self.finetodec(CONF_PARAMS['corner_points']['a_pan_fine'])
                            a_tilt = float(CONF_PARAMS['corner_points']['a_tilt']) \
                                     + self.finetodec(CONF_PARAMS['corner_points']['a_tilt_fine'])
                            b_pan = float(CONF_PARAMS['corner_points']['b_pan']) \
                                    + self.finetodec(CONF_PARAMS['corner_points']['b_pan_fine'])
                            b_tilt = float(CONF_PARAMS['corner_points']['b_tilt']) \
                                     + self.finetodec(CONF_PARAMS['corner_points']['b_tilt_fine'])
                            diff = abs(b_pan - a_pan)
                            c_pan = float(CONF_PARAMS['corner_points']['c_pan']) \
                                    + self.finetodec(CONF_PARAMS['corner_points']['c_pan_fine'])
                            c_tilt = float(CONF_PARAMS['corner_points']['c_tilt']) \
                                     + self.finetodec(CONF_PARAMS['corner_points']['c_tilt_fine'])
                            diff_y = abs(c_tilt - b_tilt)
                            point_D_pan = c_pan - diff
                            point_D_tilt = a_tilt + diff_y
                            CONF_PARAMS['corner_points']['d_pan'] = int(point_D_pan)
                            CONF_PARAMS['corner_points']['d_pan_fine'] = self.dectofine(point_D_pan)
                            CONF_PARAMS['corner_points']['d_tilt'] = int(point_D_tilt)
                            CONF_PARAMS['corner_points']['d_tilt_fine'] = self.dectofine(point_D_tilt)
                            CONF_PARAMS['Normal_DMX_values']['PAN_NORMAL'] = min(a_pan, b_pan) + (diff / 2)
                            CONF_PARAMS["Least_Counts"]["panLeastCount"] = lcv.panLeastCount()
                            CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = lcv.tiltLeastCount()
                            with open(r'./config/config.json', 'r+') as f:
                                json.dump(CONF_PARAMS, f, indent=4)
                            f.close()
                            self.showEndScreen()
                            self.stdscr.getch()
                            curses.endwin()
                            break
                        else:
                            self.currentPoint = self.pointsList[0]

                    elif key == ord('q'):
                        dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                        self.stdscr.clear()
                        self.stdscr.refresh()
                        curses.endwin()
                        return

                    dmxcontrol.setDmxToLight(int(self.DmxPan), int(self.DmxTilt), int(self.DmxPanFine), int(self.DmxTiltFine), 255)
                    self.redrawCustomScreen()

                except KeyboardInterrupt:
                    dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    curses.endwin()
                    return

        elif self.cal_mode == '3':
            self.lcv_adjustment()

    curses.endwin()
