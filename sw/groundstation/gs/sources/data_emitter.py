import datetime
import os.path
import gtk.gdk
import gobject
import threading

import gs.database as database
import gs.utils as utils
import gs.data as data

class DataEmitter(gobject.GObject):

    #Too high values of this number can starve the mainloop
    MAX_EMISSION_FREQ = 20

    __gsignals__ = {
        'uav-data-emitted': (gobject.SIGNAL_RUN_LAST,gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
        'connected': (gobject.SIGNAL_RUN_LAST,gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))
    }

    def __init__(self, *args, **kwargs):
        gobject.GObject.__init__(self)
        self._enabled = False
        self._db = database.Database(None)

        #initialize to all default available known values. Derived types may
        #include additional information as they see fit
        self._data = {}
        for k in data.DEFAULT_ATTRIBUTES:
            self._data[k] = 0.0

        #cache the insert string so it is not recreated
        self._dbInsertString =  "INSERT INTO flight_data VALUES (?"
        self._dbInsertString += ",?" * (len(data.DEFAULT_ATTRIBUTES) - 1)
        self._dbInsertString += ")"

        self._lastt = datetime.datetime.now()
        self._tsum = 0.0
        self._ti = 0

        self._se = 0
        self._sk = 0

    def connect_to_aircraft(self, *args):
        raise NotImplementedError

    def disconnect_from_aircraft(self, *args):
        raise NotImplementedError

    def get_db(self):
        return self._db

    def _connect(self, db_name):
        d = os.path.dirname(db_name)
        if not os.path.isdir(d):
            os.mkdir(d)

        self._enabled = True
        self._db.open_from_file(db_name)
        rows = self._db.fetchall("SELECT 1 FROM flight WHERE rowid=1")
        if not len(rows):
            time = datetime.datetime.now()
            self._db.execute("INSERT INTO flight VALUES (NULL, ?, ?, NULL, NULL)", (1, time))

    def _disconnect(self):
        self._enabled = False
        time = datetime.datetime.now()
        try:
            self._db.execute("UPDATE flight SET end_time=? WHERE rowid=?", (time, 1))
            self._db.close()
        except:
            pass

    def log_data(self):
        self._data[data.TIME] = datetime.datetime.now()
        d = []

        #store data in DB
        for k in data.DEFAULT_ATTRIBUTES:
            d.append(self._data[k])
        if self._db.is_open():
            self._db.execute(self._dbInsertString, d)

        #emit to GUI
        if self._enabled:
            self._lastt, enough, dt = utils.has_elapsed_time_passed(
                                        then=self._lastt,
                                        now=self._data[data.TIME],
                                        dt=1.0/self.MAX_EMISSION_FREQ)
        else:
            enough = False
            dt = utils.calculate_dt_seconds(
                                        then=self._lastt,
                                        now=self._data[data.TIME])

        #update the #messages / second esitmate twice / second
        self._tsum += dt
        self._ti += 1
        if self._tsum > 0.5:
            self._data[data.MSG_PER_SEC] = 1.0 / (self._tsum/self._ti)
            self._tsum = 0.0
            self._ti = 0
       
        if enough:
            self.emit_to_gui("uav-data-emitted", self._data)
            self._se += 1
        else:
            self._sk += 1

    def connected(self):
        self.emit_to_gui("connected", True)

    def disconnected(self):
        self.emit_to_gui("connected", False)

    def quit(self):
        raise NotImplementedError

class IdleEmissionMixin:
    def emit_to_gui(self, *args):
        gobject.idle_add(gobject.GObject.emit, self, *args)

class NormalEmissionMixin:
    def emit_to_gui(self, *args):
        self.emit(*args)

class ThreadedDataEmitter(DataEmitter, threading.Thread):
    def __init__(self, *args, **kwargs):
        DataEmitter.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)
        self._started = False
        self._cancelled = False

    def _connect(self, *args, **kwargs):
        DataEmitter._connect(self, *args, **kwargs)
        if not self._started:
            self.start()
            self._started = True
        

    def _disconnect(self, *args, **kwargs):
        self._cancelled = True

