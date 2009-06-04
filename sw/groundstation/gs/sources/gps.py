import gobject
import serial
import threading
import NMEA

import gs.data as data

class _GPSRxThread(threading.Thread):

    def __init__(self, port, speed, callback, timeout=1, **kwargs):
        threading.Thread.__init__(self)
        
        self._callback = callback
        self._timeout = timeout
        self._cancel = False
        self._port = port
        self._speed = speed
        self._nmea = NMEA.NMEA()
        
    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            ser = serial.Serial(self._port, self._speed, timeout=self._timeout)
            ser.flushInput()
            opened = True
        except serial.SerialException:
            opened = False

        while(opened and not self._cancel):
            line = ser.readline()
            if line:
                self._nmea.handle_line(line[:-1])
                self.callback(
                        lat=self._nmea.lat,
                        lon=self._nmea.lon,
                        alt=self._nmea.altitude,
                        valid=self._nmea.valid,
                        time=self._nmea.time)
        
        if opened:
            ser.close()

class GPSReceiverDataEmitter(data_emitter.DataEmitter):

    def __init__(self, port='/dev/ttyUSB0', speed=9600):
        data_emitter.DataEmitter.__init__(self)
        try:
            self._s = _GPSRxThread(port, speed, self._send_data)
            self._s.start()
        except Exception, e:
            print "ERROR STARTING GPS RX THREAD"

    def _send_data(self, lat, lon, alt, valid, time):
        if not valid:
            print "NO FIX"
            return

        self._data[data.ALT] = alt
        self._data[data.LAT] = lat
        self._data[data.LON] = lon
        self._data[data.TIME] = time

        if self._enabled:
            #gtk is not thread safe, therefor emit the new data signal on an 
            #idle handler
            gobject.idle_add(self._emit, priority=gobject.PRIORITY_HIGH)

    def connect_to_aircraft(self, db_name=None):
        self._connect(db_name)

    def disconnect_from_aircraft(self):
        self._disconnect()

    def quit(self):
        self._s.cancel()
        data_emitter.DataEmitter.quit(self)

