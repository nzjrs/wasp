#! /usr/bin/env python

#  $Id$
#  Copyright (C) 2010 Antoine Drouin
#
# This file is part of Paparazzi.
#
# Paparazzi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# Paparazzi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Paparazzi; see the file COPYING.  If not, write to
# the Free Software Foundation, 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.  
#



import os
import optparse
import scipy
import scipy.optimize

import utils

class _Parameters:
    def __init__(self, sensor_ref, sensor_res, noise_window, noise_threshold):
        self.sensor_ref = sensor_ref
        self.sensor_res = sensor_res
        self.noise_window = noise_window
        self.noise_threshold = noise_threshold

PARAMETERS = {
    "ACCEL" :   _Parameters(9.81, 10, 20, 20),
    "MAG"   :   _Parameters(1.0, 11, 10, 1000)
}       

SENSORS = PARAMETERS.keys()

def calibrate_sensor(sensor, measurements, verbose):
    parameters = PARAMETERS[sensor]
    if verbose:
       print "found %d records" % len(measurements)

    flt_meas, flt_idx = utils.filter_meas(measurements, parameters.noise_window, parameters.noise_threshold)
    if verbose:
        print "remaining %d after low pass" % len(flt_meas)
    p0 = utils.get_min_max_guess(flt_meas, parameters.sensor_ref)
    cp0, np0 = utils.scale_measurements(flt_meas, p0)
    print "initial guess : avg %f std %f" % (np0.mean(), np0.std())

    def err_func(p,meas,y):
        cp, np = utils.scale_measurements(meas, p)
        err = y*scipy.ones(len(meas)) - np
        return err

    p1, success = scipy.optimize.leastsq(err_func, p0[:], args=(flt_meas, parameters.sensor_ref))
    cp1, np1 = utils.scale_measurements(flt_meas, p1)

    print "optimized guess : avg %f std %f" % (np1.mean(), np1.std())

    utils.print_xml(p1, sensor, parameters.sensor_res)
    print ""

    utils.plot_results(measurements, flt_idx, flt_meas, cp0, np0, cp1, np1, parameters.sensor_ref)

if __name__ == "__main__":
    sensor = "ACCEL"
    meas = utils.read_log("IMU_ACCEL_RAW.log", sensor)
    calibrate_sensor(sensor, meas, True)
