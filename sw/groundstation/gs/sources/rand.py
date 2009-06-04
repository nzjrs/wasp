import gobject
import datetime
import random
import time
import threading

import gs.data as data
import gs.sources.source as source

class RandomDataEmitter(source.Source, threading.Thread):

    def __init__(self, *args, **kwargs):
        source.Source.__init__(self)
        threading.Thread.__init__(self)

        #Initialize to Canterbury University, Christchurch, NZ
        self._data[data.LAT] = -43.532600
        self._data[data.LAT_HEM] = "N"
        self._data[data.LON] = 172.636200
        self._data[data.LON_HEM] = "E"
        self._data[data.ALT] = 200

        self._running = False
        self._started = False
        self._stopped = False

    def connect_to_craft(self):
        if not self._started:
            self.start()
        self._running = True

    def disconnect_from_craft(self):
        self._running = False

    def quit(self):
        self._stopped = True
        if self._started:
            self.join()

    def run(self):
        self._started = True
        while not self._stopped:
            if self._running:
                self.add_data(
                        0, **{
                        data.IS_CONNECTED   : 1,
                        data.LAT    :   self._data[data.LAT] + (random.random() * 0.00001),
                        data.LON    :   self._data[data.LON] + (random.random() * 0.00001),
                        data.ROLL   :   self._data[data.ROLL] + random.randrange(-5.0,5.0,int=float),
                        data.PITCH  :   self._data[data.PITCH] + random.randrange(-5.0,5.0,int=float),
                        data.YAW    :   self._data[data.YAW] + random.randrange(-5.0,5.0,int=float),
                        data.P      :   random.randrange(-1.0,1.0,int=float),
                        data.Q      :   random.randrange(-1.0,1.0,int=float),
                        data.R      :   random.randrange(-1.0,1.0,int=float),
                        data.AX     :   random.randrange(-1.0,1.0,int=float),
                        data.AY     :   random.randrange(-1.0,1.0,int=float),
                        data.AZ     :   random.randrange(-1.0,1.0,int=float)}
                )
            time.sleep(0.05)



