"""
libwasp is a library for interacting with UAVs running the wasp software system.
This library can be used to create groundstation and other monitoring software
for interacting with the UAV. The library is coupled with the onboard sofware 
througn

* *messages.xml* - the defintion of messages sent over the chosen communication
  channel from the UAV to the groundstation
* *settings.xml* - a concept of a semi-persistant setting on the UAV. The setting
  may be read/updated from the groundstation and stored on the UAV
"""

import random
import time
import math

#: dictionary mapping the C type to its length in bytes (e.g char -> 1)
TYPE_TO_LENGTH_MAP = {
    "char"      :   1,
    "uint8"     :   1,
    "int8"      :   1,
    "uint16"    :   2,
    "int16"     :   2,
    "uint32"    :   4,
    "int32"     :   4,
    "float"     :   4,
}

#: dictionary mapping the C type to correct format string
TYPE_TO_PRINT_MAP = {
        float   :   "%f",
        str     :   "%s",
        chr     :   "%c",
        int     :   "%d"
}

def setup_comm_optparse_options(parser, default_messages="/dev/null"):
    """
    Adds a number of communication related command line options to an
    optparse parser instance. These options are
    "-m", "--messages" : messages xml file
    "-p", "--port"     : serial port
    "-s", "--speed"    : serial port baud rate
    "-t", "--timeout"  : serial timeout
    """
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="messages xml file", metavar="FILE")
    parser.add_option("-p", "--port",
                    default="/dev/ttyUSB0",
                    help="serial port")
    parser.add_option("-s", "--speed",
                    type="int", default=57600,
                    help="serial port baud rate")
    parser.add_option("-t", "--timeout",
                    type="int", default=1,
                    help="serial timeout")

class _Noisy:
    """
    An interface for objects providing noisy data (usually for testing)
    """
    def value(self):
        """
        :returns: the next value
        """
        raise NotImplementedError

class NoisySine(_Noisy):
    """
    Generates a noisy sinewave
    """
    def __init__(self, freq=1.0, amplitude=50.0, value_type=float, positive=True, noise_pct=10):
        self.t = time.time()
        self.dt = 0.0

        self.freq = freq
        self.amp = amplitude
        self.type = value_type

        #add 1 to sine to keep +ve
        if positive:
            self.offset = 1.0
        else:
            self.offset = 0.0

        #the noise is x percent of the amplitude
        n = (noise_pct/100.0) * self.amp
        self.n1 = self.amp - n
        self.n2 = self.amp + n
        
    def value(self):
        t = time.time()
        self.dt += (self.freq * (t - self.t))
        self.t = t

        val = (self.offset * math.sin(self.dt)) * self.amp
        noise = random.randrange(self.n1, self.n2, int=self.type)
        return self.type(noise + val)

class NoisyWalk(_Noisy):
    """
    Generates a noisy random walk
    """
    def __init__(self, start, end, delta, value_type=float):
        self.v = start
        self.end = end
        self.start = start
        self.delta = delta
        self.type = value_type

    def value(self):
        v = self.v + (self.delta * random.randrange(0.0,1.0, int=float))
        if self.start > self.end:
            if v > self.end and v < self.start:
                self.v = v
        else:
            if v < self.end and v > self.start:
                self.v = v
        return self.type(self.v)

class Noisy(_Noisy):
    def __init__(self, value, delta, value_type=float):
        self.v = value
        self.delta = delta
        self.type = value_type

    def value(self):
        return self.type(self.v + (self.delta * random.randrange(0.0,1.0, int=float)))

