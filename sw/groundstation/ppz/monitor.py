import gobject

class GObjectSerialMonitor(gobject.GObject):

    __gsignals__ = {
        "got-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT]),
        }

    def __init__(self, serialsender):
        gobject.GObject.__init__(self)
        self._watch = None   

        serialsender.connect("serial-connected", self._on_serial_connected)

    def _on_serial_connected(self, serial, connected):
        #remove the old watch
        if self._watch:
            gobject.source_remove(self._watch)

        if connected:
            #add new watch
            self._watch = gobject.io_add_watch(
                            serial.get_serial().fileno(), 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_serial_data_available,
                            serial,
                            priority=gobject.PRIORITY_HIGH
            )



    def on_serial_data_available(self, fd, condition, serial):
        raise NotImplementedError

