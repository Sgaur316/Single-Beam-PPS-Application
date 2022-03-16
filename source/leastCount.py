"""This script calculates the mounting error and least count value using calibration points"""
# importing libraries
import json
import math
from config import CONF_PARAMS


class Leastcountvalue():

    # following are the x and y coordinates of four corner points of MSU with fine movements adjusted as decimals
    x1 = float(CONF_PARAMS["corner_points"]["a_pan"]) + ((float(CONF_PARAMS["corner_points"]["a_pan_fine"]) // 0.255) / 1000)
    y1 = float(CONF_PARAMS["corner_points"]["a_tilt"]) + ((float(CONF_PARAMS["corner_points"]["a_tilt_fine"]) // 0.255) / 1000)
    x2 = float(CONF_PARAMS["corner_points"]["b_pan"]) + ((float(CONF_PARAMS["corner_points"]["b_pan_fine"]) // 0.255) / 1000)
    y2 = float(CONF_PARAMS["corner_points"]["b_tilt"]) + ((float(CONF_PARAMS["corner_points"]["b_tilt_fine"]) // 0.255) / 1000)
    x3 = float(CONF_PARAMS["corner_points"]["c_pan"]) + ((float(CONF_PARAMS["corner_points"]["c_pan_fine"]) // 0.255) / 1000)
    y3 = float(CONF_PARAMS["corner_points"]["c_tilt"]) + ((float(CONF_PARAMS["corner_points"]["c_tilt_fine"]) // 0.255) / 1000)
    x4 = float(CONF_PARAMS["corner_points"]["d_pan"]) + ((float(CONF_PARAMS["corner_points"]["d_pan_fine"]) // 0.255) / 1000)
    y4 = float(CONF_PARAMS["corner_points"]["d_tilt"]) + ((float(CONF_PARAMS["corner_points"]["d_tilt_fine"]) // 0.255) / 1000)

    # Important Measurements
    station_width = (CONF_PARAMS["site"]["WINDOW_WIDTH"]*10)/2
    station_height = CONF_PARAMS["site"]["WINDOW_HEIGHT"]*10
    proj_unit_height = CONF_PARAMS["site"]["PROJECTOR_BASE_HEIGHT"]*10
    base_proj_dist = CONF_PARAMS["site"]["PROJECTOR_BASE_DISTANCE"]*10
    # h1 = math.sqrt(math.pow(proj_unit_height,2)+math.pow(base_proj_dist,2))
    # h2 = math.sqrt(math.pow(station_width,2)+math.pow(base_proj_dist,2))
    msu_widH = CONF_PARAMS["site"]["RACK_WIDTH"]/2
    msu_proj_dist = CONF_PARAMS["site"]["RACK_PROJ_DISTANCE"]
    msu_H = CONF_PARAMS["site"]["RACK_HEIGHT"]

    def mounterrortilt(self, delX):
        """
        mounterrY produces the dmx value compensation in Y for every X pan movements
        """
        x = self.x1 - delX
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        return m * x

    def mounterrorpan(self, delY):
        """
        mounterrX produces the dmx value compensation in X for every Y pan movements
        """
        x = delY - self.y1
        m = (self.x4 - self.x1) / (self.y4 - self.y1)
        return m * x


    # Least Count calculation using base station calibration
    # def panLeastCount()-> float:
    #     diff = abs(x2-x1)
    #     ang = 2 * (math.degrees(math.atan(station_width/h1)))
    #     if diff == 0:
    #         diff = 1
    #     return ang/diff
    #
    # def tiltLeastCount()-> float:
    #     diff = abs(y4-y1)
    #     prfloat(h2)
    #     prfloat(station_height-proj_unit_height)
    #     ang = (math.degrees(math.atan(proj_unit_height/h2)))+(math.degrees(math.atan((station_height-proj_unit_height)/h2)))
    #     if diff == 0:
    #         diff = 1
    #     return ang/diff
    """Least Count calculation using MSU calibration"""

    def panLeastCount(self) -> float:
        """
        Least count value for pan movement at given MSU distance
        """
        diff = abs(self.x2-self.x1)
        ang = 2 * (math.degrees(math.atan(self.msu_widH/self.msu_proj_dist)))
        if diff == 0:
            diff = 1
        res = (ang/diff)
        formatted_string = "{:.3f}".format(res)
        res = float(formatted_string)
        return res

    def tiltLeastCount(self) -> float:
        """
        Least count value for tilt movement at given MSU distance
        """
        diff = abs(self.y4-self.y1)
        ang = (math.degrees(math.atan(self.msu_H/self.msu_proj_dist)))
        if diff == 0:
            diff = 1
        res = (ang / diff)
        formatted_string = "{:.3f}".format(res)
        res = float(formatted_string)
        return res
