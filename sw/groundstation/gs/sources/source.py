import datetime
import threading

import gs.utils as utils
import gs.data as data
import gs.database as database

class Source:
    def __init__(self):
        self._cbs = []
        self._lastt = datetime.datetime.now()
        self._lock = threading.Lock()

        self._data = {}
        for k in data.DEFAULT_ATTRIBUTES:
            #fill with appropriate zero value for type
            self._data[k] = data.ATTRIBUTE_TYPE[k]()

    def is_connected(self):
        return self.get_data(data.IS_CONNECTED)[0]

    def connect_to_craft(self):
        pass

    def disconnect_from_craft(self):
        pass

    def install_data_callback(self, func, *args):
        self._cbs.append( (func, args) )

    def quit(self):
        pass

    def get_data(self, *dataNames):
        self._lock.acquire()
        data = [self._data.get(d, 0) for d in dataNames]
        self._lock.release()
        return data

    def add_data(self, numBytes, **rx):
        self._lock.acquire()

        self._data[data.TIME] = datetime.datetime.now()
        self._data[data.NUM_MSG_RX] += 1

        dt = utils.calculate_dt_seconds(
                                then=self._lastt,
                                now=self._data[data.TIME]
                                )
        self._lastt = self._data[data.TIME]
        self._data[data.MSG_PER_SEC] = 1.0 / dt

        for k,v in rx.items():
            self._data[k] = v

        self._lock.release()

        for cb, args in self._cbs:
            cb(*args)


   
