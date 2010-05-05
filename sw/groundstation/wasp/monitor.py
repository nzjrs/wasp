import gobject

class GObjectSerialMonitor(gobject.GObject):
    """
    A GObject base class that accepts a libserial.SerialSender object 
    and sets up the appropriate watches on the underlying file descriptor. It
    also manages the connnection/disconnection logic so the port can be
    reconfigured once the app is running.

    Derived classes must implement the on_serial_data_available method
    and then emit the *got-message* signal. This means that users of this 
    class need only to connect to the "got-message" signal
    """

    __gsignals__ = {
        "got-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT]),
        }

    def __init__(self, serialsender):
        gobject.GObject.__init__(self)
        self._watch = None

        self.change_serialsender(serialsender)

    def change_serialsender(self, serialsender):
        """
        Change the underlying libserial.SerialSender, such as after reconfiguration
        """
        #remove the old watch
        if self._watch:
            gobject.source_remove(self._watch)
        #wait for connection
        serialsender.connect("serial-connected", self._on_serial_connected)

    def _on_serial_connected(self, serial, connected):
        #remove the old watch
        if self._watch:
            gobject.source_remove(self._watch)

        if connected:
            #add new watch
            self._watch = gobject.io_add_watch(
                            serial.get_fd(), 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_serial_data_available,
                            serial,
                            priority=gobject.PRIORITY_HIGH
            )



    def on_serial_data_available(self, fd, condition, serial):
        """
        Derived types must implement this function. It is called whenever there
        is data available to be read from the libserial.SerialSender
        """
        raise NotImplementedError

