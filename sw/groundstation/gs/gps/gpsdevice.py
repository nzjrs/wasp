#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Open GPS Daemon - Parse NMEA/UBX data

(C) 2008 Michael 'Mickey' Lauer <mlauer@vanille-media.de>
(C) 2008 Jan 'Shoragan' Lübbe <jluebbe@lasnet.de>
(C) 2008 Daniel Willmann <daniel@totalueberwachung.de>
(C) 2008 Openmoko, Inc.
GPLv2 or later
"""

#DBUS_INTERFACE_PREFIX = "org.freedesktop.Gypsy"
#DBUS_PATH_PREFIX = "/org/freedesktop/Gypsy"

#import dbus
#import dbus.service

import logging
logger = logging.getLogger()

#class GPSDevice( dbus.service.Object ):
class GPSDevice:
    """An Dbus Object implementing org.freedesktop.Gypsy"""

    def __init__(self):
        self._fixstatus = 0
        self._position = [ 0, 0, 0.0, 0.0, 0.0 ]
        self._accuracy = [ 0, 0.0, 0.0, 0.0 ]
        self._course = [ 0, 0, 0.0, 0.0, 0.0 ]
        self._satellites = []
        self._time = 0

        #self.interface = DBUS_INTERFACE_PREFIX
        #self.path = DBUS_PATH_PREFIX
        #self.bus = bus
        #dbus.service.Object.__init__( self, bus, self.path )
        #logger.info("%s initialized. Serving %s at %s" % ( self.__class__.__name__, self.interface, self.path ) )

    def _reset( self ):
        if self._fixstatus:
            self._fixstatus = 0
        #    self.FixStatusChanged( self._fixstatus )
        if self._position[0]:
            self._position[0] = 0
        #    self.PositionChanged( *self._position )
        if self._accuracy[0]:
            self._accuracy[0] = 0
        #    self.AccuracyChanged( *self._accuracy )
        if self._course[0]:
            self._course[0] = 0
        #    self.CourseChanged( *self._course )
        if self._satellites != []:
            self._satellites = []
        #    self.SatellitesChanged( self._satellites )
        if self._time:
            self._time = 0
        #    self.TimeChanged( self._time )

    def _updateFixStatus( self, fixstatus ):
        if self._fixstatus != fixstatus:
            self._fixstatus = fixstatus
        #    self.FixStatusChanged( self._fixstatus )

    def _updatePosition( self, fields, lat, lon, alt ):
        changed = False
        if self._position[0] != fields:
            self._position[0] = fields
            changed = True
        if fields:
            self._position[1] = self._time
        if fields & (1 << 0) and self._position[2] != lat:
            self._position[2] = lat
            changed = True
        if fields & (1 << 1) and self._position[3] != lon:
            self._position[3] = lon
            changed = True
        if fields & (1 << 2) and self._position[4] != alt:
            self._position[4] = alt
            changed = True
        #if changed:
        #    self.PositionChanged( *self._position )

    def _updateAccuracy( self, fields, pdop, hdop, vdop ):
        changed = False
        if self._accuracy[0] != fields:
            self._accuracy[0] = fields
            changed = True
        if fields & (1 << 0) and self._accuracy[1] != pdop:
            self._accuracy[1] = pdop
            changed = True
        if fields & (1 << 1) and self._accuracy[2] != hdop:
            self._accuracy[2] = hdop
            changed = True
        if fields & (1 << 2) and self._accuracy[3] != vdop:
            self._accuracy[3] = vdop
            changed = True
        #if changed:
        #    self.AccuracyChanged( *self._accuracy )

    def _updateCourse( self, fields, speed, heading, climb ):
        changed = False
        if self._course[0] != fields:
            self._course[0] = fields
            changed = True
        if fields:
            self._course[1] = self._time
        if fields & (1 << 0) and self._course[2] != speed:
            self._course[2] = speed
            changed = True
        if fields & (1 << 1) and self._course[3] != heading:
            self._course[3] = heading
            changed = True
        if fields & (1 << 2) and self._course[4] != climb:
            self._course[4] = climb
            changed = True
        #if changed:
        #    self.CourseChanged( *self._course )

    def _updateSatellites( self, satellites ):
        # Is this check sufficient or could some SVs switch channels, but
        # otherwise stay identical?
        if self._satellites != satellites:
            self._satellites = satellites
            #self.SatellitesChanged( self._satellites )

    def _updateTime( self, time ):
        if self._time != time:
            self._time = time
            #self.TimeChanged( self._time )

    def get_lla(self):
        return self._position[2],self._position[3],self._position[4]

class DummyDevice( GPSDevice ):
    """A dummy device that reports a static position"""
    def __init__( self ):
        GPSDevice.__init__(self)

        self._updateTime( 1 )
        self._updateFixStatus( 3 )
        self._updatePosition( 7, 23.54322, -42.65648, 14.4 )
        self._updateAccuracy( 7, 2.34, 16.4, 1.4 )
        self._updateCourse( 7, 240.4, 45.4, -4.4 )
        self._updateSatellites( [(1, False, 13, 164, 0), (13, True, 72, 250, 20), (24, True, 68, 349, 31)] )

if __name__ == "__main__":
    import logging
    d = DummyDevice()
    print d.get_lla()

#vim: expandtab
