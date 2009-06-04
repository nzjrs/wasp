import datetime
import gobject

ROLL =          "roll"
PITCH =         "pitch"
YAW =           "yaw"
LAT =           "lat"
LAT_HEM =       "latHem"
LON =           "lon"
LON_HEM =       "lonHem"
ALT =           "alt"
P =             "p"
Q =             "q"
R =             "r"
AX =            "ax"
AY =            "ay"
AZ =            "az"
TIME =          "time"
HEADING =       "heading"
GROUND_SPEED =  "groundSpeed"
MSG_PER_SEC =   "msgPerSec"
NUM_MSG_RX =    "numberOfMessagesReceived"
IS_CONNECTED =  "isConnected"
ERROR =         "error"
WARNING =       "warning"
AUTO =          "autopilot"
MANUAL =        "manual"

DEFAULT_ATTRIBUTES = [v for k,v in globals().items() if not k.startswith('_') and type(v) == str]
DEFAULT_ATTRIBUTES.sort()

class _TypeDict:
    def __getitem__(self, name):
        if name in (TIME, LAT_HEM, LON_HEM):
            return str
        elif name in (NUM_MSG_RX, IS_CONNECTED):
            return int
        else:
            return float
ATTRIBUTE_TYPE = _TypeDict()

#A dynamic mechanism to declare additional types at
#runtime
class _AttributeManager(gobject.GObject):

    __gsignals__ = {
        "new-attribute" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_STRING,        #the attribute name
            gobject.TYPE_PYOBJECT]),    #the attribute type
    }

    def __init__(self):
        gobject.GObject.__init__(self)
        self._attributes = {}
        for d in DEFAULT_ATTRIBUTES:
            self._attributes[d] = ATTRIBUTE_TYPE[d]

    def add_attribute(self, attributeName, attributeType):
        self._attributes[attributeName] = attributeType
        self.emit("new-attribute", attributeName, attributeType)

    def get_attributes(self):
        return self._attributes.keys()

    def get_attribute_type(self, attributeName):
        return self._attributes[attributeName]
AttributeManagerSingleton = _AttributeManager()

class _CommandManager(gobject.GObject):

    ENTRY_NUMBER = 1
    ENTRY_SLIDER = 2
    ENTRY_ENTRY = 3

    __gsignals__ = {
        "new-command" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_STRING,        #the attribute name
            gobject.TYPE_PYOBJECT,      #the attribute type
            gobject.TYPE_INT,           #the attribute entry type
            gobject.TYPE_PYOBJECT]),    #extra specifiers for the entry type
    }

    def __init__(self):
        gobject.GObject.__init__(self)
        self._commands = {}

    def add_command(self, commandName, commandType, entryType, *extra):
        self._commands[commandName] = (
                commandType,
                entryType,
                extra)
        self.emit("new-command", 
                commandName,
                commandType,
                entryType,
                extra)

    def get_commands(self):
        return self._commands.keys()

    def get_command_information(self, commandName):
        return self._commands[commandName]
CommandManagerSingleton = _CommandManager()

