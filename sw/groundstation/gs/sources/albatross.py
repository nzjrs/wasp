import data_emitter
import threading
import datetime
import gobject
import socket

import gs.data as data

class _SGSSockServer(threading.Thread):
    def __init__(self, host, port, callback, timeout=0.1, **kwargs):
        threading.Thread.__init__(self)
        self._callback = callback
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._cancel = False

        try:
            import libsgs
            self._parser = libsgs.SGSParser()
        except ImportError:
            raise Exception("Couldn't find libsgs. Please regenerate")

        try:
            self._s.bind((host, port))
            self._s.settimeout(timeout)
        except socket.error, err:
            raise Exception("Couldn't be a udp server on port %s:%d : %s" % (host,port,err))

    def cancel(self):
        self._cancel = True

    def run(self):
        while(not self._cancel):
            try:
                datagram = self._s.recv(self._parser.MAX_SIZE)
                data = self._parser.unpack_from_buffer(datagram)
                self._callback(*data)
            except socket.timeout:
                pass
            except Exception, e:
                print e
        self._s.close()

class AlbatrossSocketDataEmitter(data_emitter.DataEmitter):

    def __init__(self, host='localhost', port=7000):
        data_emitter.DataEmitter.__init__(self)
        try:
            self._f = _SGSSockServer(host,port,self._send_data)
            self._f.start()
        except Exception, e:
            print "ERROR STARTING SERVER"

    def _send_data(self, latitude, longitude, altitude, pitch, roll, yaw):
        if latitude == 0.0 and longitude == 0.0 and altitude == 0.0:
            return

        self._data[data.ROLL] = roll
        self._data[data.YAW] = yaw
        self._data[data.PITCH] = pitch
        self._data[data.ALT] = altitude
        self._data[data.LAT] = latitude
        self._data[data.LON] = longitude
        self._data[data.TIME] = datetime.datetime.now()

        if self._enabled:
            #gtk is not thread safe, therefor emit the new data signal on an 
            #idle handler
            gobject.idle_add(self._emit, priority=gobject.PRIORITY_HIGH)

    def connect_to_aircraft(self, db_name=None):
        self._connect(db_name)

    def disconnect_from_aircraft(self):
        self._disconnect()

    def quit(self):
        self._f.cancel()
        data_emitter.DataEmitter.quit(self)

