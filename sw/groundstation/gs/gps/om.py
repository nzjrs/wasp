#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Open GPS Daemon

(C) 2008 Jan 'Shoragan' Lübbe <jluebbe@lasnet.de>
(C) 2008 Daniel Willmann <daniel@totalueberwachung.de>
(C) 2008 Openmoko, Inc.
GPLv2 or later
"""

DBUS_INTERFACE = "org.freesmartphone.GPS"

import dbus
import dbus.service
import os
import sys
import marshal
import time
from ubx import UBXDevice
from ubx import CLIDPAIR

import logging
logger = logging.getLogger('ogpsd')

class GTA02Device( UBXDevice ):
    """GTA02 specific GPS device"""

    def __init__( self, bus, gpschannel ):
        self.power = False
        self.aidingFile = "aiding.dat"
        self.aidingData = {}

        super( GTA02Device, self ).__init__( bus, gpschannel )

    def configure(self):
        # Reset the device
        #self.send("CFG-RST", 4, {"nav_bbr" : 0xffff, "Reset" : 0x01})

        # Load aiding data
        self.loadAidingData()

        super( GTA02Device, self ).configure()

        # Enable NAV-POSECEF, AID-REQ (AID-DATA), AID-ALM, AID-EPH messages
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-POSECEF"][0] , "MsgID" : CLIDPAIR["NAV-POSECEF"][1] , "Rate": 8 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-REQ"][0] , "MsgID" : CLIDPAIR["AID-REQ"][1] , "Rate": 1 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-ALM"][0] , "MsgID" : CLIDPAIR["AID-ALM"][1] , "Rate": 1 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-EPH"][0] , "MsgID" : CLIDPAIR["AID-EPH"][1] , "Rate": 1 })

    def deconfigure(self):
        # Save collected aiding data
        self.saveAidingData()

        super( GTA02Device, self ).deconfigure()

        # Disable NAV-POSECEF, AID-REQ (AID-DATA), AID-ALM, AID-EPH messages
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-POSECEF"][0] , "MsgID" : CLIDPAIR["NAV-POSECEF"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-REQ"][0] , "MsgID" : CLIDPAIR["AID-REQ"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-ALM"][0] , "MsgID" : CLIDPAIR["AID-ALM"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["AID-EPH"][0] , "MsgID" : CLIDPAIR["AID-EPH"][1] , "Rate" : 0 })

    def loadAidingData( self ):
        logger.info("Loading aiding data")
        try:
            self.aidingData = marshal.load(open(self.aidingFile, "r"))
        except:
            self.aidingData = { "almanac": {}, "ephemeris": {}, "position": {} }

    def saveAidingData( self ):
        logger.info("Saving aiding data")
        FILE = open(self.aidingFile, 'w+')
        marshal.dump(self.aidingData, FILE)
        FILE.close()

    def handle_NAV_POSECEF( self, data ):
        data = data[0]
        self.aidingData["position"]["x"] = data["ECEF_X"]
        self.aidingData["position"]["y"] = data["ECEF_Y"]
        self.aidingData["position"]["z"] = data["ECEF_Z"]

    def handle_AID_DATA( self, data ):
        pos = self.aidingData["position"]

        # Position accuracy needs to rough, because device may have been moved
        pacc = 30000000 # in cm (300 KM)

        # GPS week number
        wn = int((time.time() - time.mktime(time.strptime("5 Jan 1980", "%d %b %Y"))) / (86400 * 7))

        # GPS time of week
        tow = int(time.time() - (time.mktime(time.strptime("5 Jan 1980", "%d %b %Y")) + wn * 86400 * 7)) * 1000

        # Time accuracy needs to be changed, because the RTC is imprecise
        tacc = 120000 # in ms (2 minutes)

        # Feed GPS with position and time
        self.send("AID-INI", 48, {"X" : pos["x"] , "Y" : pos["y"] , "Z" : pos["z"], "POSACC" : pos["accuracy"], \
                                  "TM_CFG" : 0 , "WN" : wn , "TOW" : tow , "TOW_NS" : 0 , "TACC_MS" : tacc , "TACC_NS" : 0 , \
                                  "CLKD" : 0 , "CLKDACC" : 0 , "FLAGS" : 0x3 })

        # Feed gps with almanac
        for k, a in self.aidingData["almanac"].iteritems():
            logger.debug("Loaded almanac for SV %d" % a["SVID"])
            self.send("AID-ALM", 40, a);

        # Feed gps with ephemeris
        for k, a in self.aidingData["ephemeris"].iteritems():
            logger.debug("Loaded ephemeris for SV %d" % a["SVID"])
            self.send("AID-EPH", 104, a);

    def handle_AID_ALM( self, data ):
        data = data[0]
        # Save only, if there are values
        if "DWRD0" in data:
            self.aidingData["almanac"][ data["SVID"] ] = data

    def handle_AID_EPH( self, data ):
        data = data[0]
        # Save only, if there are values
        if "SF1D0" in data:
            self.aidingData["ephemeris"][ data["SVID"] ] = data

    #
    # dbus methods
    #
    @dbus.service.method( DBUS_INTERFACE, "b", "" )
    def SetPower( self, power ):
        if self.power == power:
            return

        logger.debug( "Setting GPS Power to %s" % power )
        if not power:
            self.deconfigure()

        proxy = self.bus.get_object( "org.freesmartphone.odeviced" , "/org/freesmartphone/Device/PowerControl/GPS" )
        gps = dbus.Interface( proxy, "org.freesmartphone.Device.PowerControl" )
        gps.SetPower( power, reply_handler=self._replyCallback, error_handler=self._errorCallback )

    def _replyCallback( self ):
        self.power = not self.power

        if self.power:
            self.configure()

    def _errorCallback( self, e ):
        pass


#vim: expandtab
