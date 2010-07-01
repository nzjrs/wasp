import math
import time
import struct
import socket
import logging
import subprocess

EXECUTABLE = "fgfs"

VIS_HOST = "127.0.0.1"
VIS_PORT = 6000
VIS_REFRESH_RATE = 30

SIM_HOST = "127.0.0.1"
SIM_PORT = 5501

LOG = logging.getLogger('wasp.sim')

def get_flightgear_vis_args(host, port):
    return (
        EXECUTABLE,
        "--native-fdm=socket,in,30,%s,%d,udp" % (host, port),
        "--fdm=external",
        "--disable-sound",
        "--timeofday=noon"
    )

def get_flightgear_sim_args(model_path, host=SIM_HOST, port=SIM_PORT):
    return (
        EXECUTABLE,
        "--native-gui=socket,in,30,%s,%d,udp" % (host, port),
        "--fdm=null",
        "--disable-sound",
        "--timeofday=noon",
        "--prop:/sim/model/path=%s.xml" % model_path
    )

class _FlightGearProcess:
    def __init__(self, cmd_args):
        self.cmd_args = cmd_args
        self.process = None

    def start(self):
        LOG.info("Launching: %s" % " ".join(self.cmd_args))
        self.process = subprocess.Popen(self.cmd_args)
#                            stdout=None,
#                            stderr=None)

    def is_running(self):
        return self.process and self.process.poll() == None

    def stop(self):
        if self.is_running():
            LOG.info("Sending SIGTERM to process")
            self.process.terminate()
            self.process = None

# Convert the class FGNetFDM structure into a python struct definition
# seeL net_fdm.hxx in the FlightGear sources
FG_NET_FDM_VERSION = 24
FGNETFDM_STRUCT_DEFINITION = \
    "!"                     +\
    "II"                    +\
    "dddffffff"             +\
    "fffffffffff"           +\
    "fff"                   +\
    "ff"                    +\
    ""                      +\
    "I4I4f4f4f4f4f4f4f4f4f" +\
    "I4f"                   +\
    "I3I3f3f3f"             +\
    "Iif"                   +\
    "ffffffffff"

# Convert the class FGNetMiniFDM structure into a python struct definition
# seeL net_fdm.hxx in the FlightGear sources
# 
FG_NET_FDM_MINI_VERSION = 2
FGNETMINIFDM_STRUCT_DEFINITION = \
    "!"                     +\
    "I"                     +\
    "ddddddd"               +\
    "dd"                    +\
    "I4d"                   +\
    "Ii"

class FlightGearVisualisation(_FlightGearProcess):
    def __init__(self, host=VIS_HOST, port=VIS_PORT):
        _FlightGearProcess.__init__(self, get_flightgear_vis_args(host, port))
        self.struct = struct.Struct(FGNETFDM_STRUCT_DEFINITION)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_addr = (host, port)

    def set_attitude_position(self, lat, lon, alt, roll, pitch, yaw):
        if not self.is_running():
            return

        d = self.struct.pack(
                    FG_NET_FDM_VERSION,     #uint32_t version
                    0,                      #uint32_t padding
                    math.radians(lon),      #double longitude geodetic (radians)
                    math.radians(lat),      #double latitude geodetic (radians)
                    alt,                    #double altitude above sea level (meters)
                    0.0,                    #float agl above ground level (meters)
                    math.radians(roll),     #float phi roll (radians)
                    math.radians(pitch),    #float theta pitch (radians)
                    math.radians(yaw),      #float psi yaw or true heading (radians)
                    0.0,                    #float alpha angle of attack (radians)
                    0.0,                    #float beta side slip angle (radians)
                    0.0,                    #float phidot roll rate (radians/sec)
                    0.0,                    #float thetadot pitch rate (radians/sec)
                    0.0,                    #float psidot yaw rate (radians/sec)
                    0.0,                    #float vcas calibrated airspeed
                    0.0,                    #float climb_rate feet per second
                    0.0,                    #float v_north north velocity in local/body frame, fps
                    0.0,                    #float v_east east velocity in local/body frame, fps
                    0.0,                    #float v_down down/vertical velocity in local/body frame, fps
                    0.0,                    #float v_wind_body_north north velocity in local/body frame relative to local airmass, fps
                    0.0,                    #float v_wind_body_east east velocity in local/body frame relative to local airmass, fps
                    0.0,                    #float v_wind_body_down down/vertical velocity in local/body frame relative to local airmass, fps
                    0.0,                    #float A_X_pilot X accel in body frame ft/sec^2
                    0.0,                    #float A_Y_pilot Y accel in body frame ft/sec^2
                    0.0,                    #float A_Z_pilot Z accel in body frame ft/sec^2
                    0.0,                    #float stall_warning 0.0 - 1.0 indicating the amount of stall
                    0.0,                    #float slip_deg slip ball deflection
                    1,                      #uint32_t num_engines Number of valid engines
                    0,0,0,0,                #uint32_t eng_state[FG_MAX_ENGINES] Engine state (off, cranking, running)
                    0.0,0.0,0.0,0.0,        #float rpm[FG_MAX_ENGINES] Engine RPM rev/min
                    0.0,0.0,0.0,0.0,        #float fuel_flow[FG_MAX_ENGINES] Fuel flow gallons/hr
                    0.0,0.0,0.0,0.0,        #float fuel_px[FG_MAX_ENGINES] Fuel pressure psi
                    0.0,0.0,0.0,0.0,        #float egt[FG_MAX_ENGINES] Exhuast gas temp deg F
                    0.0,0.0,0.0,0.0,        #float cht[FG_MAX_ENGINES] Cylinder head temp deg F
                    0.0,0.0,0.0,0.0,        #float mp_osi[FG_MAX_ENGINES] Manifold pressure
                    0.0,0.0,0.0,0.0,        #float tit[FG_MAX_ENGINES] Turbine Inlet Temperature
                    0.0,0.0,0.0,0.0,        #float oil_temp[FG_MAX_ENGINES] Oil temp deg F
                    0.0,0.0,0.0,0.0,        #float oil_px[FG_MAX_ENGINES] Oil pressure psi
                    1,                      #uint32_t num_tanks Max number of fuel tanks
                    0.0,0.0,0.0,0.0,        #float fuel_quantity[FG_MAX_TANKS]
                    3,                      #uint32_t num_wheels
                    0,0,0,                  #uint32_t wow[FG_MAX_WHEELS]
                    0.0,0.0,0.0,            #float gear_pos[FG_MAX_WHEELS]
                    0.0,0.0,0.0,            #float gear_steer[FG_MAX_WHEELS]
                    0.0,0.0,0.0,            #float gear_compression[FG_MAX_WHEELS]
                    int(time.time()),       #uint32_t cur_time current unix time
                    0,                      #int32_t warp offset in seconds to unix time
                    5000.0,                 #float visibility visibility in meters (for env. effects)
                    0.0,                    #float elevator
                    0.0,                    #float elevator_trim_tab
                    0.0,                    #float left_flap
                    0.0,                    #float right_flap
                    0.0,                    #float left_aileron
                    0.0,                    #float right_aileron
                    0.0,                    #float rudder
                    0.0,                    #float nose_wheel
                    0.0,                    #float speedbrake
                    0.0                     #float spoilers
        )

        self.socket.sendto(d, self.socket_addr)

if __name__ == "__main__":
    import gobject
    import logging
    logging.basicConfig(level=logging.DEBUG)

    def update(fg):
        try:
            #these default lat/lon come from the flightgear startup defaults
            fg.set_attitude_position(
                    lat=37.4277,
                    lon=-122.357,
                    alt=1000.0,
                    roll=0.0,
                    pitch=0.0,
                    yaw=0.0)
        except Exception, e:
            print e
        return True

    f = FlightGearVisualisation()
    f.start()
    try:
        gobject.timeout_add(1000/VIS_REFRESH_RATE, update, f)
        gobject.MainLoop().run()
    except KeyboardInterrupt:
        pass
    f.stop()



    

