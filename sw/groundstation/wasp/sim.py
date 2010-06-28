EXECUTABLE = "fgfs"

VIS_HOST = ""
VIS_PORT = 6000

SIM_HOST = ""
SIM_PORT = 5501

def get_flightgear_vis(host=VIS_HOST, port=VIS_PORT):
    return "%s --native-fdm=socket,in,30,%s,%d,udp --fdm=external --disable-sound --timeofday=noon" % (EXECUTABLE, host, port)

def get_flightgear_sim(model_path, host=SIM_HOST, port=SIM_PORT):
    return "%s --fdm=null --native-gui=socket,in,30,%s,%d,udp --prop:/sim/model/path=%s.xml" % (EXECUTABLE, host, port, model_path)

class FlightGearSim:
    def __init__(self, model_path):
        self.cmd = get_flightgear_sim(model_path)
