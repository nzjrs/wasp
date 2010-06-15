''' 
Copyright 2009 Jezra Lickter 
 
This software is distributed AS IS. Use at your own risk. 
If it borks your system, you have  been forewarned. 
 
This software is licensed under the LGPL Version 3 
http://www.gnu.org/licenses/lgpl-3.0.txt 
 
 
for documentation on Linux Joystick programming please see 
http://www.mjmwired.net/kernel/Documentation/input/joystick-api.txt 
''' 
import logging
import gobject
import struct
import os.path

import gtk
import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('control.joystick')

class ControlJoystick(plugin.Plugin):

    DEFAULT_DEVICE = "/dev/input/js0"

    def __init__(self, conf, source, messages_file, groundstation_window):

        if not os.path.exists(self.DEFAULT_DEVICE):
            raise plugin.PluginNotSupported("Joystick %s not connected" % self.DEFAULT_DEVICE)

        self.joystick = Joystick(device=self.DEFAULT_DEVICE)

        groundstation_window.add_control_widget(
                "Joystick Control",
                gtk.Label("disabled"))

        LOG.info("Joystick Control initialized")
 
class Joystick(gobject.GObject): 
    '''The Joystick class is a GObject that sends signals that represent 
    Joystick events''' 
    EVENT_BUTTON = 0x01 #button pressed/released 
    EVENT_AXIS = 0x02  #axis moved  
    EVENT_INIT = 0x80  #button/axis initialized  
    #see http://docs.python.org/library/struct.html for the format determination 
    EVENT_FORMAT = "IhBB" 
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT) 
     
    # we need a few signals to send data to the main 
    '''signals will return 4 variables as follows: 
    1. a string representing if the signal is from an axis or a button 
    2. an integer representation of a particular button/axis 
    3. an integer representing axis direction or button press/release 
    4. an integer representing the "init" of the button/axis 
    ''' 
    __gsignals__ = { 
    'axis' : 
    (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
    (gobject.TYPE_INT,gobject.TYPE_INT,gobject.TYPE_INT)), 
    'button' : 
    (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
    (gobject.TYPE_INT,gobject.TYPE_INT,gobject.TYPE_INT)) 
    } 
     
 
    def __init__(self,dev_num,device=None): 
        gobject.GObject.__init__(self) 
        #define the device
        if not device:
            device = '/dev/input/js%s' % dev_num 
        #error check that this can be read 
        try: 
            #open the joystick device 
            self.device = open(device) 
            #keep an eye on the device, when there is data to read, execute the read function 
            gobject.io_add_watch(self.device,gobject.IO_IN,self.read_buttons) 
        except Exception,ex: 
            #raise an exception 
            raise Exception( ex ) 
         
    def read_buttons(self, arg0='', arg1=''): 
        ''' read the button and axis press event from the joystick device 
        and emit a signal containing the event data 
        ''' 
        #read self.EVENT_SIZE bytes from the joystick 
        read_event = self.device.read(self.EVENT_SIZE)   
        #get the event structure values from  the read event 
        time, value, type, number = struct.unpack(self.EVENT_FORMAT, read_event) 
        #get just the button/axis press event from the event type  
        event = type & ~self.EVENT_INIT 
        #get just the INIT event from the event type 
        init = type & ~event 
        if event == self.EVENT_AXIS: 
            signal = "axis" 
        elif event == self.EVENT_BUTTON: 
            signal = "button" 
        if signal: 
            print("%s %s %s %s" % (signal,number,value,init) ) 
            self.emit(signal,number,value,init) 
         
        return True 
         
if __name__ == "__main__": 
    try: 
        j = Joystick(0) 
        loop = gobject.MainLoop() 
        loop.run() 
    except Exception,e: 
        print(e) 
