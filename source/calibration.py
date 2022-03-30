""" Calibration file is where we set the parameters and sets up our projection file according to the onsite situation"""
# importing libraries
import sys
import time
sys.path.append('./')
import curses
import json
from source.projection import Dmxcontrol
from source.projection import Display
from source.leastCount import Leastcountvalue
from config import CONF_PARAMS, RACK_PROJ_DISTANCE, TILT_LEAST_COUNT, PAN_LEAST_COUNT
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

    def convert_distance_to_dmx(self, x, y, panLeastCount, tiltLeastCount):
        dmxcontrol = Dmxcontrol()
        valueZ = RACK_PROJ_DISTANCE * 10
        dmxPAN, dmxTILT = dmxcontrol.calc_dmx(0, 0, valueZ, panLeastCount, tiltLeastCount)
        lcv = Leastcountvalue()
        deltaX = lcv.mounterrorpan(dmxTILT)
        deltaY = lcv.mounterrortilt(dmxPAN)
        logHandle.info("Mount fix in X for Y tilts:" + str(deltaX))
        logHandle.info("Mount fix in Y for X pans :" + str(deltaY))
        dmxPAN = dmxPAN + deltaX
        dmxPanFine = dmxcontrol.dectofine(dmxPAN)  # dectofine function to convert floating dmx value to fine movement
        dmxTILT = dmxTILT - deltaY
        dmxTiltFine = dmxcontrol.dectofine(dmxTILT)
        return dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine


    def lcv_adjustment(self):
        try:
            """
                    LCV stands for "Least Count Value"
            lcv_adjustment function is used for tuning the least count values to increase flexibility and gain scenario
            independency, Projectors may show different pan tilt angles covered for a single Dmx value change which makes it a
            mechanically dependent variable and is exactly what the least count is.
                So in order to manage the span of movement of projection beam for any angle totally depends on the least count value, it can be regulated from this function.
            """
            dmxcontrol = Dmxcontrol()
            dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine = self.convert_distance_to_dmx(0, 0, self.pan_lcv, self.tilt_lcv)
            dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
            while True:
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, "If the projector is not pointing towards the intended D(0,0) coordinate "
                                         "point adjust the projection to intended spot by altering span factors "
                                         "using arrow keys.")
                self.stdscr.addstr(1, 0, " PAN Span Factor : %s" % CONF_PARAMS["Least_Counts"]["panLeastCount"])
                self.stdscr.addstr(2, 0, " TILT Span Factor : %s" % CONF_PARAMS["Least_Counts"]["tiltLeastCount"])
                self.stdscr.addstr(3, 0,
                            "Adjust the span factor in order to accumulate the projection span inaccuracy(e.g. "
                            "reducing TILT span factor will push and increase the tilt motion range downwards"
                            ".i.e.Increases the Tilt DMX value).")
                self.stdscr.addstr(5, 0, "Press 'E' to exit this prompt: ")

                try:
                    key = self.stdscr.getch()
                    self.stdscr.refresh()
                    # here set dmx light to zero
                    if key == curses.KEY_UP:
                        self.tilt_lcv = self.tilt_lcv + 0.005
                        formatted_string = "{:.3f}".format(self.tilt_lcv)
                        self.tilt_lcv = float(formatted_string)
                        CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = self.tilt_lcv
                        dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine = self.convert_distance_to_dmx(0, 0, self.pan_lcv, self.tilt_lcv)
                        dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
                    elif key == curses.KEY_DOWN:
                        self.tilt_lcv = self.tilt_lcv - 0.005
                        formatted_string = "{:.3f}".format(self.tilt_lcv)
                        self.tilt_lcv = float(formatted_string)
                        CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = self.tilt_lcv
                        # TILT_LEAST_COUNT = CONF_PARAMS["Least_Counts"]["tiltLeastCount"]
                        dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine = self.convert_distance_to_dmx(0, 0, self.pan_lcv, self.tilt_lcv)
                        dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
                    elif key == curses.KEY_LEFT:
                        self.pan_lcv = self.pan_lcv - 0.001
                        formatted_string = "{:.3f}".format(self.pan_lcv)
                        self.pan_lcv = float(formatted_string)
                        CONF_PARAMS["Least_Counts"]["panLeastCount"] = self.pan_lcv
                        # PAN_LEAST_COUNT = CONF_PARAMS["Least_Counts"]["panLeastCount"]
                        dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine = self.convert_distance_to_dmx(0, 0, self.pan_lcv, self.tilt_lcv)
                        dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
                    elif key == curses.KEY_RIGHT:
                        self.pan_lcv = self.pan_lcv + 0.001
                        formatted_string = "{:.3f}".format(self.pan_lcv)
                        self.pan_lcv = float(formatted_string)
                        CONF_PARAMS["Least_Counts"]["panLeastCount"] = self.pan_lcv
                        # PAN_LEAST_COUNT = CONF_PARAMS["Least_Counts"]["panLeastCount"]
                        dmxPAN, dmxTILT, dmxPanFine, dmxTiltFine = self.convert_distance_to_dmx(0, 0, self.pan_lcv, self.tilt_lcv)
                        dmxcontrol.setDmxToLight(int(dmxPAN), int(dmxTILT), int(dmxPanFine), int(dmxTiltFine), 255)
                    elif key == ord('e') or key == ord('E'):
                        with open(r'./config/config.json', 'w') as conf:
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
        except Exception as e:
            logHandle.error("Exception occurred while advance caliberating the projector {}".format(e))
            self.stdscr.clear()
            self.stdscr.refresh()
            curses.endwin()


    # A simple function to increment the dmx value by one
    def increaseByOne(self, dmxValue):
        try:
            incremented = dmxValue + 1
            if self.isValidDmx(incremented):
                return incremented
            else:
                return dmxValue  # Return unchanged value
        except Exception as e:
            logHandle.error("Exception occurred inside increaseByOne {}".format(e))

    def decreaseByOne(self, dmxValue):
        """
            Logically opposite of the above function, decreases the dmx value by one.
        """
        try:
            decremented = dmxValue - 1
            if self.isValidDmx(decremented):
                return decremented
            else:
                return dmxValue  # Return unchanged value
        except Exception as e:
            logHandle.error("Exception occurred inside decreaseByOne {}".format(e))

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
        try:
            self.redrawCustomScreen()
            self.stdscr.addstr(5, 0, "Written to config file, press any key to exit!!!")
        except Exception as e:
            logHandle.error("Exception occurred {}".format(e))

    def showStartScreen(self):
        """
            Support function for redrawCustomScreen function
        """
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.echo()
        self.stdscr.addstr(0, 0, 
                        "Select the calibration mode:\n"
                        "1. MSU measurements from ground\n"
                        "2. Base Station Calibration\n"
                        "3. Quit Calibration Process\n"
                        "Select Option: ")
        while True:
            try:
                choice = self.stdscr.getch()
                self.stdscr.refresh()
                if choice == 49:
                    self.cal_mode = "1"
                    logHandle.info("Entered MSU Measurement option")
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(5, len("Select Option: "), self.cal_mode)
                elif choice == 50:
                    self.cal_mode = "2"
                    logHandle.info("Entered Base Station calibration")
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(5, len("Select Option: "), self.cal_mode)
                    break
                elif choice == 51:
                    self.cal_mode = "3"
                    logHandle.info("Entered Advance calibration")
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(5, len("Select Option: "), self.cal_mode)
                elif choice == ord('\n'):
                    break
                elif choice == 52:
                    self.cal_mode = "4"
                elif choice == curses.KEY_BACKSPACE:
                    self.cal_mode = "0"
                    self.stdscr.clrtoeol()
                else:
                    self.stdscr.addstr(5, len("Select Option: "), "Invalid Input")
                    self.cal_mode = "0"
            except Exception as e:
                logHandle.error("Start Screen error: %s" % e)
                self.stdscr.clear()
                self.stdscr.refresh()
                curses.endwin()

    def measrementcalibrations(self):
        """
        This function runs the application in measurement input mode.
        """
        try:
            oscillation_choice = CONF_PARAMS["dev"]["OSCILLATION_CHOICE"]
            self.stdscr.clear()
            curses.echo()
            self.stdscr.addstr(0, 0, "MSU Rack Width: ")
            CONF_PARAMS["site"]["RACK_WIDTH"] = float(self.stdscr.getstr(0, len("MSU Rack Width: "), 2))
            self.stdscr.addstr(2, 0, "MSU Rack Base Height from ground: ")
            CONF_PARAMS["site"]["RACK_BASE_HEIGHT"] = float(self.stdscr.getstr(2, len("MSU Rack Base Height from ground: "), 2))
            self.stdscr.addstr(4, 0, "Projector Height from ground: ")
            CONF_PARAMS["site"]["PROJ_HEIGHT"] = float(self.stdscr.getstr(4, len("Projector Height from ground: "), 3))
            curses.noecho()
            self.stdscr.addstr(6, 0, "Set Oscillation True or False by pressing 'F': " + str(oscillation_choice))
            while True:
                choice = self.stdscr.getch()
                if choice == ord('f') or choice == ord('F'):
                    oscillation_choice = not oscillation_choice
                    self.stdscr.deleteln()
                    self.stdscr.refresh()
                    self.stdscr.addstr(6, 0, "Set Oscillation True or False by pressing 'F': " + str(oscillation_choice))
                elif choice == ord('\n'):
                    CONF_PARAMS["dev"]["OSCILLATION_CHOICE"] = oscillation_choice
                    break
            curses.echo()
            CONF_PARAMS["site"]["RACK_HEIGHT"] = CONF_PARAMS["site"]["PROJ_HEIGHT"] - CONF_PARAMS["site"]["RACK_BASE_HEIGHT"]
            with open(r'./config/config.json', 'w') as con:
                json.dump(CONF_PARAMS, con, indent=4)
            self.stdscr.clear()
            self.stdscr.refresh()
            curses.endwin()
        except Exception as e:
            logHandle.error("measurement calibration mode error: %s" % e)
            self.stdscr.clear()
            self.stdscr.refresh()
            curses.endwin()

    def finetodec(self, a) -> float:
        try:
            return a / 255
        except Exception as e:
            logHandle.error("Exception occurred {}".format(e))

    # dectofine function is used for converting decimal value to fine mode dmx values
    def dectofine(self, a):
        try:
            return int((a % 1) * 255)
        except Exception as e:
            logHandle.error("Exception occurred {}".format(e))

    # Main function of the script to run the calibration application
    def calibrate(self):
        try:
            dmxcontrol = Dmxcontrol()
            while True:
                if dmxcontrol.is_projector_connected():
                    break
                else:
                    time.sleep(5)
            while True:
                lcv = Leastcountvalue()
                self.showStartScreen()

                if self.cal_mode == '1':
                    self.measrementcalibrations()

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
                                    formatted_string = "{:.3f}".format(min(a_pan, b_pan) + (diff / 2))
                                    CONF_PARAMS['Normal_DMX_values']['PAN_NORMAL'] = float(formatted_string)
                                    CONF_PARAMS["Least_Counts"]["panLeastCount"] = lcv.panLeastCount()
                                    CONF_PARAMS["Least_Counts"]["tiltLeastCount"] = lcv.tiltLeastCount()
                                    self.pan_lcv = CONF_PARAMS["Least_Counts"]["panLeastCount"]
                                    self.tilt_lcv = CONF_PARAMS["Least_Counts"]["tiltLeastCount"]
                                    with open(r'./config/config.json', 'w') as f:
                                        json.dump(CONF_PARAMS, f, indent=4)
                                    f.close()
                                    self.showEndScreen()
                                    self.stdscr.getch()
                                    # curses.endwin()
                                    self.lcv_adjustment()
                                else:
                                    self.currentPoint = self.pointsList[0]

                            elif key == ord('q') or key == ord('Q'):
                                dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)

                                break

                            dmxcontrol.setDmxToLight(int(self.DmxPan), int(self.DmxTilt), int(self.DmxPanFine), int(self.DmxTiltFine), 255)
                            self.redrawCustomScreen()
                        except KeyboardInterrupt:
                            dmxcontrol.setDmxToLight(0, 0, 0, 0, 0)
                            self.stdscr.clear()
                            self.stdscr.refresh()
                            curses.endwin()
                            return


                elif self.cal_mode == '3':
                    logHandle.info("Exiting Calibration mode option selected")
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    curses.endwin()
                    break

                else:
                    logHandle.error("Unknown input selected cal_mode = {}".format(self.cal_mode))
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    curses.endwin()
                    break

        except Exception as e:
            logHandle.error("Exception occurred while advance caliberating the projector {}".format(e))
            self.stdscr.clear()
            self.stdscr.refresh()
            curses.endwin()

    curses.endwin()
