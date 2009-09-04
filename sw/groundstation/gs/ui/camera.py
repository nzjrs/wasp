import logging
import subprocess
import gtk
import gst

import gs.config as config

LOG = logging.getLogger('camera')

class Camera(gtk.DrawingArea):
    def __init__(self, source="v4l2src", device="/dev/video0", norm="PAL-N", input_channel="Composite1"):
        gtk.DrawingArea.__init__(self)
        self._playing = False
        self._pb = None

        v4lcmds = []
        if norm:
            v4lcmds.append(["setnorm", norm])
        if input_channel:
            v4lcmds.append(["setinput", input_channel])

        #configure the camera
        for cmd in v4lcmds:
            cmd = ['v4lctl', '-c', device] + cmd
            LOG.debug("Setting video parameter: %s" % " ".join(cmd))
            try:
                if subprocess.call(cmd, executable='v4lctl') != 0:
                    print "Error calling %s" % ' '.join(cmd)
            except OSError: pass


        #configure the pipeline
        #gst-launch-0.10 v4l2src ! autovideosink"
        # Set up the gstreamer pipeline
        try:
            pipeline = "%s device=%s ! autovideosink" % (source, device)

            LOG.debug("Video pipeline: %s" % pipeline)
            self.pipeline = gst.parse_launch (pipeline)

            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect("message", self._on_message)
            bus.enable_sync_message_emission()
            bus.connect("sync-message::element", self._on_sync_message)
        except:
            LOG.warning("Error configuring camera window", exc_info=True)
            self._pipeline = None

    def _on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.stop()
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            self.stop()

    def _on_sync_message(self, bus, message):
        if message.structure != None:
            message_name = message.structure.get_name()
            if message_name == "prepare-xwindow-id":
                # Assign the viewport so the video does not
                # show in a new window
                #imagesink = message.src
                message.src.set_property("force-aspect-ratio", True)
                message.src.set_xwindow_id(self.window.xid)

    def start(self, *args):
        if self.pipeline:
            self._playing = True
            self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self, *args):
        if self.pipeline:
            self._playing = False
            self.pipeline.set_state(gst.STATE_NULL)

    def pause(self, *args):
        if self.pipeline:
            self._playing = False
            self.pipeline.set_state(gst.STATE_PAUSED)

class CameraWindow(gtk.Window, config.ConfigurableIface):

    CONFIG_SECTION = "CAMERA"

    DEFAULT_SOURCE = "v4l2src"
    DEFAULT_DEVICE = "/dev/video0"
    DEFAULT_NORM = "PAL-N"
    DEFAULT_INPUT_CHANNEL = "Composite1"

    def __init__(self, conf):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        config.ConfigurableIface.__init__(self, conf)

        #initialize self._source, etc with the default ^^^ values
        self.autobind_config("source", "device", "norm", "input_channel")

        self._cam = Camera(self._source, self._device, self._norm, self._input_channel)
        self._cam.show()
        self.add(self._cam)
        self.connect("destroy", self.stop)

    def start(self, *args):
        self._cam.start()

    def stop(self, *args):
        self._cam.stop()

    def pause(self, *args):
        self._cam.pause()

    def get_preference_widgets(self):
        #all following items configuration is saved
        items = [
            self.build_entry("source"),
            self.build_entry("device"),
            self.build_entry("norm"),
            self.build_entry("input_channel")
        ]

        #the gui looks like
        sg = self.make_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Source", items[0], sg),
            self.build_label("Device", items[1], sg),
            self.build_label("Norm", items[2], sg),
            self.build_label("Input Channel", items[3], sg),
        ])

        return "Camera", frame, items

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    gtk.gdk.threads_init()

    win = gtk.Window()
    cam = Camera(
            device='/dev/video0',
            norm='PAL-N',
            input_channel='Composite1')
    win.add(cam)
    win.connect("destroy", lambda w,c: c.stop(), cam)
    win.connect("destroy", gtk.main_quit)
    win.show_all()
    cam.start()
    gtk.main()


