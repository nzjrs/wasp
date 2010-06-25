import sys
import os.path
import optparse

_thisdir = os.path.dirname(os.path.abspath(__file__))

NAME = "Wasp Groundstation"
VERSION = "0.1"

IS_WINDOWS = os.name == "nt"
if IS_WINDOWS:
    IS_INSTALLED = sys.argv[0].endswith(".exe")
    if IS_INSTALLED:
        #report a dir relative to the executable. these values
        #must be kept in sync with the py2exe configuration
        ICON_DIR = os.path.join("..","share","groundstation", "icons")
        UI_DIR = os.path.join("..", "share", "groundstation", "ui")
        PLUGIN_DIR = os.path.join("..", "lib", "groundstation", "plugins")
        CONFIG_DIR = os.path.join("..", "etc", "groundstation", "config")
    else:
        #report absolute dir
        ICON_DIR = os.path.abspath(os.path.join(_thisdir, "..", "data", "icons"))
        UI_DIR = os.path.abspath(os.path.join(_thisdir, "..", "data", "ui"))
        PLUGIN_DIR = os.path.abspath(os.path.join(_thisdir, "plugins"))
        CONFIG_DIR = os.path.abspath(os.path.join(_thisdir, "..", "..", "onboard", "config"))
else:
    #FIXME: dont support running installed yet..
    IS_INSTALLED = False
    ICON_DIR = os.path.join(_thisdir, "..", "data", "icons")
    UI_DIR = os.path.join(_thisdir, "..", "data", "ui")
    PLUGIN_DIR = os.path.join(_thisdir, "plugins")
    CONFIG_DIR = os.path.join(_thisdir, "..", "..", "onboard", "config")

USER_CONFIG_DIR = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ.get("HOME","."), ".config", "wasp"))

del(_thisdir)

def linspace(xmin, xmax, N):
    """
    Return a list of N linearly spaced floats in
    the range [xmin,xmax], i.e. including the endpoints
    """
    if N==1: return [xmax]
    dx = (xmax-xmin)/(N-1)
    return [xmin] + [xmin + (dx*float(i)) for i in range(1,N)]

def user_file_path(filename):
    """
    Returns a file path with the given filename,
    on the users Desktop
    """
    return os.path.join(
                os.path.expanduser("~"),
                "Desktop",
                filename)

def scale_to_range(val, oldrange, newrange=(0.0,1.0), reverse=False):
    oldmin = float(oldrange[0])
    oldmax = float(oldrange[1])
    newmin = float(newrange[0])
    newmax = float(newrange[1])
    val += newmin - oldmin
    val *= (newmax-newmin)/(oldmax-oldmin)
    if reverse:
        return newmin + (newmax - val)
    return val

class _SourceOptionParser(optparse.OptionParser):
    #override parse_args so that -t is the same as --source=test
    #it is easier to do it this was instead of with a 
    #optparse callback
    def parse_args(self):
        options, args = optparse.OptionParser.parse_args(self)
        if options.use_test_source:
            options.source = "test"
        return options, args
                
def get_default_command_line_parser(include_prefs, include_plugins, include_sources, messages_name="messages.xml", settings_name="settings.xml", preferences_name="groundstation.ini"):
    default_messages = os.path.join(CONFIG_DIR, "messages.xml")
    default_settings = os.path.join(CONFIG_DIR, "settings.xml")

    if include_prefs:
        if not os.path.exists(USER_CONFIG_DIR):
            os.makedirs(USER_CONFIG_DIR)
        prefs = os.path.join(USER_CONFIG_DIR, "groundstation.ini")

    if include_sources:
        parser = _SourceOptionParser()
    else:
        parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="Messages xml file", metavar="FILE")
    parser.add_option("-s", "--settings",
                    default=default_settings,
                    help="Settings xml file", metavar="FILE")
    parser.add_option("-d", "--debug",
                    action="store_true",
                    help="Print extra debugging information")
    if include_prefs:
        parser.add_option("-p", "--preferences",
                        default=prefs,
                        help="User preferences file", metavar="FILE")
    if include_plugins:
        parser.add_option("-P", "--plugin-dir",
                        default=PLUGIN_DIR,
                        help="Directory to load plugins from", metavar="DIRECTORY")
        parser.add_option("-D", "--disable-plugins",
                        action="store_true", default=False,
                        help="Disable loading plugins")
    if include_sources:
        parser.add_option("-t", "--use-test-source",
                        action="store_true", default=False,
                        help="Use a test source, equiv to --source=test")
        parser.add_option("-S", "--source",
                        default="serial",
                        help="Source of uav data (serial,test,etc)", metavar="SOURCE")

    return parser

