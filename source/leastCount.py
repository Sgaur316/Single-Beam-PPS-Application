"""This script calculates the mounting error and least count value using calibration points"""
# importing libraries
import json
import math
from config import CONF_PARAMS
from source import logger

logHandle = logger.logHandle


class Leastcountvalue():

    # following are the x and y coordinates of four corner points of MSU with fine movements adjusted as decimals
    def __init__(self):
        try:
            logHandle.debug("CONF_PARAMS : {}".format(CONF_PARAMS))
            self.x1 = float(CONF_PARAMS["corner_points"]["a_pan"]) + ((float(CONF_PARAMS["corner_points"]["a_pan_fine"]) // 0.255) / 1000)
            self.y1 = float(CONF_PARAMS["corner_points"]["a_tilt"]) + ((float(CONF_PARAMS["corner_points"]["a_tilt_fine"]) // 0.255) / 1000)
            self.x2 = float(CONF_PARAMS["corner_points"]["b_pan"]) + ((float(CONF_PARAMS["corner_points"]["b_pan_fine"]) // 0.255) / 1000)
            self.y2 = float(CONF_PARAMS["corner_points"]["b_tilt"]) + ((float(CONF_PARAMS["corner_points"]["b_tilt_fine"]) // 0.255) / 1000)
            self.x3 = float(CONF_PARAMS["corner_points"]["c_pan"]) + ((float(CONF_PARAMS["corner_points"]["c_pan_fine"]) // 0.255) / 1000)
            self.y3 = float(CONF_PARAMS["corner_points"]["c_tilt"]) + ((float(CONF_PARAMS["corner_points"]["c_tilt_fine"]) // 0.255) / 1000)
            self.x4 = float(CONF_PARAMS["corner_points"]["d_pan"]) + ((float(CONF_PARAMS["corner_points"]["d_pan_fine"]) // 0.255) / 1000)
            self.y4 = float(CONF_PARAMS["corner_points"]["d_tilt"]) + ((float(CONF_PARAMS["corner_points"]["d_tilt_fine"]) // 0.255) / 1000)

            # Important Measurements
            self.msu_widH = CONF_PARAMS["site"]["RACK_WIDTH"]/2
            self.msu_proj_dist = CONF_PARAMS["site"]["RACK_PROJ_DISTANCE"]
            self.msu_H = CONF_PARAMS["site"]["RACK_HEIGHT"]
        except Exception as e:
            logHandle.error("Exception occurred: {}".format(e))

    def mounterrortilt(self, delX):
        """
        mounterrY produces the dmx value compensation in Y for every X pan movements
        """
        try:
            x = self.x1 - delX
            m = (self.y2 - self.y1) / (self.x2 - self.x1)
            return m * x
        except Exception as e:
            logHandle.error("Exception occurred: {}".format(e))

    def mounterrorpan(self, delY):
        """
        mounterrX produces the dmx value compensation in X for every Y pan movements
        """
        try:
            x = delY - self.y1
            m = (self.x4 - self.x1) / (self.y4 - self.y1)
            return m * x
        except Exception as e:
            logHandle.error("Exception occurred: {}".format(e))

    """Least Count calculation using MSU calibration"""

    def panLeastCount(self) -> float:
        """
        Least count value for pan movement at given MSU distance
        """
        try:
            diff = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
            ang = 2 * (math.degrees(math.atan(self.msu_widH/self.msu_proj_dist)))
            res = (ang/diff)
            formatted_string = "{:.3f}".format(res)
            res = float(formatted_string)
            return res
        except Exception as e:
            logHandle.error("Exception occurred: {}".format(e))

    def tiltLeastCount(self) -> float:
        """
        Least count value for tilt movement at given MSU distance
        """
        try:
            diff = math.sqrt((self.x2 - self.x3)**2 + (self.y2 - self.y3)**2)
            hypot = math.sqrt((self.msu_H)**2 + (self.msu_widH)**2 + (self.msu_proj_dist)**2)
            ang = (math.degrees(math.asin(self.msu_H/hypot)))
<<<<<<< HEAD
=======
            if diff == 0:
                diff = 1
>>>>>>> 2ece7f8308ec7cf31214e209819466cc35908b3b
            res = (ang / diff)
            formatted_string = "{:.3f}".format(res)
            res = float(formatted_string)
            return res
        except Exception as e:
            logHandle.error("Exception occurred: {}".format(e))
