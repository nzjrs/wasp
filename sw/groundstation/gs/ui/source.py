import datetime
import gobject

import gs.utils as utils

class _UpdateSource:
    def __init__(self):
        self._sm = None

    def set_source_manager(self, sourceManager):
        self._sm = sourceManager

    def get_source_manager(self):
        return self._sm

    def get_source(self):
        if self._sm:
            return self._sm.get_source()
        else:
            return None

class ManualUpdateFromSource(_UpdateSource):
    pass

class PeriodicUpdateFromSource(_UpdateSource):
    def __init__(self, freq=10, immediate=False):
        _UpdateSource.__init__(self)
        self._dt = 1.0/freq
        self._lastt = datetime.datetime.now()
        self._immediate = immediate
        self._freq = freq

    def set_source_manager(self, sourceManager):
        _UpdateSource.set_source_manager(self, sourceManager)
        source = self.get_source()

        if self._immediate:
            source.install_data_callback(self.__got_data)
        else:
            gobject.timeout_add(1000.0 * self._dt, self.__update_from_data)

    def __enough_time_passed(self):
        self._lastt, enough, dt = utils.has_elapsed_time_passed(
                                        then=self._lastt,
                                        now=datetime.datetime.now(),
                                        dt=self._dt)
        return enough

    def __got_data(self, source):
        if self.__enough_time_passed():
            gobject.idle_add(self._update_from_data, source)

    def __update_from_data(self):
        self.update_from_data(self._sm.get_source())
        return True

    def update_from_data(self, source):
        raise NotImplementedError

        
