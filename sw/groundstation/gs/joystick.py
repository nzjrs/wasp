# Based on code from http://www.jezra.net/blog/Python_Joystick_Class_using_Gobject
# Copyright 2009 Jezra Lickter

import logging
import gobject
import struct
import os.path

LOG = logging.getLogger('joystick')

def list_devices():
    return ["/dev/input/js%d" % i for i in range(10) if os.path.exists("/dev/input/js%d" % i)]

class Joystick(gobject.GObject): 
    """
    The Joystick class is a GObject that sends signals that represent 
    Joystick events
    """
    EVENT_BUTTON    = 0x01  #button pressed/released 
    EVENT_AXIS      = 0x02  #axis moved  
    EVENT_INIT      = 0x80  #button/axis initialized  
    #see http://docs.python.org/library/struct.html for the format determination 
    EVENT_FORMAT    = "IhBB" 
     
    # we need a few signals to send data to the main 
    # signals will return 4 variables as follows: 
    # 1. a string representing if the signal is from an axis or a button 
    # 2. an integer representation of a particular button/axis 
    # 3. an integer representing axis direction or button press/release 
    # 4. an integer representing the "init" of the button/axis 
    __gsignals__ = { 
    "axis" : 
    (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
    (gobject.TYPE_INT,gobject.TYPE_INT,gobject.TYPE_INT)), 
    "button" : 
    (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
    (gobject.TYPE_INT,gobject.TYPE_INT,gobject.TYPE_INT)) 
    } 
     
 
    def __init__(self,dev_num=0,device=None):
        gobject.GObject.__init__(self) 
        if not device:
            device = "/dev/input/js%s" % dev_num 

        self.event_struct = struct.Struct(self.EVENT_FORMAT)
        try:
            self.device = open(device)
            self.source_id = gobject.io_add_watch(self.device,gobject.IO_IN,self._read_buttons)
        except IOError, e:
            self.device = None
            LOG.warn("Error opening device", exc_info=True)

    def close(self):
        if self.device:
            self.device.close()
            gobject.source_remove(self.source_id)
         
    def _read_buttons(self, arg0='', arg1=''):
        """
        read the button and axis press event from the joystick device 
        and emit a signal containing the event data 
        """
        read_event = self.device.read(self.event_struct.size)   
        time, value, _type, number = self.event_struct.unpack(read_event) 
        # get just the button/axis press event from the event type  
        event = _type & ~self.EVENT_INIT 
        # get just the INIT event from the event type 
        init = _type & ~event 

        if event == self.EVENT_AXIS: 
            self.do_axis_event(number, value, init)
        elif event == self.EVENT_BUTTON:
            self.do_button_event(number, value, init)
         
        return True 

    def do_axis_event(self, number, value, init):
        self.emit("axis", number, value, init)

    def do_button_event(self, number, value, init):
        self.emit("button", number, value, init)

class CalibratedJoystick(Joystick):
    def __init__(self, *args, **kwargs):
        Joystick.__init__(self, *args, **kwargs)
        self._axis_remap = {}
        self._axis_remap_inverse = {}
        self._axis_reverse = {}
        self._axis_uncalibrated_values = {}

    def axis_remap(self, old_axis, new_axis):
        self._axis_remap[old_axis] = new_axis
        self._axis_remap_inverse[new_axis] = old_axis

    def axis_reverse(self, old_axis, reverse=True):
        if reverse:
            self._axis_reverse[old_axis] = -1
        else:
            self._axis_reverse[old_axis] = 1

    def get_uncalibrated_axis_and_value(self, new_axis):
        try:
            old_axis = self._axis_remap_inverse[new_axis]
        except KeyError:
            old_axis = new_axis
        return old_axis, self._axis_uncalibrated_values[old_axis]

    def do_axis_event(self, number, value, init):
        self._axis_uncalibrated_values[number] = value
        self.emit("axis",
                self._axis_remap.get(number, number),
                value * self._axis_reverse.get(number, 1),
                init)

if __name__ == "__main__":
    def on_axis(j, num, val, init):
        print "AXIS: %d = %d (%d)" % (num, val, init)
    def on_button(j, num, val, init):
        print "BUTTON: %d = %d (%d)" % (num, val, init)
    try: 
        j = Joystick(0)
        j.connect("axis", on_axis)
        j.connect("button", on_button)
        loop = gobject.MainLoop() 
        loop.run() 
    except Exception,e: 
        print(e) 
