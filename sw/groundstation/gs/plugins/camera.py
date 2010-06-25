import logging
import subprocess
import gtk
import gst

import gs.plugin as plugin
import gs.config as config

LOG = logging.getLogger('camera')

class _Camera(gtk.DrawingArea):
    V4L2_SOURCE = "v4l2src"
    def __init__(self, source=V4L2_SOURCE, device="/dev/video0", norm="", input_channel=""):
        gtk.DrawingArea.__init__(self)
        self._playing = False
        self._pb = None

        if source == self.V4L2_SOURCE:
            #configure the v4l_source (likely if it is a tv card)
            v4lcmds = []
            if norm:
                v4lcmds.append(["setnorm", norm])
            if input_channel:
                v4lcmds.append(["setinput", input_channel])
            for cmd in v4lcmds:
                cmd = ['v4lctl', '-c', device] + cmd
                LOG.debug("Setting video parameter: %s" % " ".join(cmd))
                try:
                    if subprocess.call(cmd, executable='v4lctl') != 0:
                        LOG.warning("Error calling %s" % ' '.join(cmd))
                except OSError:
                    LOG.warning("Error calling %s" % ' '.join(cmd), exc_info=True)

        #configure the pipeline
        #gst-launch-0.10 v4l2src ! autovideosink"
        # Set up the gstreamer pipeline
        try:
            if source == self.V4L2_SOURCE:
                source = "%s device=%s" % (source, device)

            pipeline = "%s ! autovideosink" % source
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
                gtk.gdk.threads_enter()
                gtk.gdk.display_get_default().sync()
                message.src.set_property("force-aspect-ratio", True)
                message.src.set_xwindow_id(self.window.xid)
                gtk.gdk.threads_leave()

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

class CameraWindow(plugin.Plugin, config.ConfigurableIface):

    CONFIG_SECTION = "CAMERA"

    DEFAULT_SOURCE = "v4l2src"
    DEFAULT_DEVICE = "/dev/video0"
    DEFAULT_NORM = "PAL-N"
    DEFAULT_INPUT_CHANNEL = "Composite1"

    def __init__(self, conf, source, messages_file, groundstation_window):
        config.ConfigurableIface.__init__(self, conf)

        #add an entry to the window menu
        item = gtk.ImageMenuItem("Camera View")
        item.set_image(gtk.image_new_from_stock(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU))
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("Window", item)

        #initialize self._source, etc with the default ^^^ values
        self.autobind_config("source", "device", "norm", "input_channel")

        self._cam = None
        self._win = gtk.Window()
        self._win.connect("destroy", self.stop)

    def _show_window(self, *args):
        if not self._cam:
            self._cam = _Camera(self._source, self._device, self._norm, self._input_channel)
            self._win.add(self._cam)
            self._win.show_all()
            self._cam.start()

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
        sg = self.build_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Source",          items[0], sg=sg),
            self.build_label("Device",          items[1], sg=sg),
            self.build_label("Norm",            items[2], sg=sg),
            self.build_label("Input Channel",   items[3], sg=sg),
        ])

        return "Camera", frame, items

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    gtk.gdk.threads_init()

    def make_win(cam):
        win = gtk.Window()
        win.add(cam)
        win.connect("destroy", lambda w,c: c.stop(), cam)
        win.connect("destroy", gtk.main_quit)
        win.show_all()
        return win

    cam = _Camera(
            device='/dev/video0',
            norm='PAL-N',
            input_channel='Composite1')
    w1 = make_win(cam)
    cam.start()

    test = _Camera(source="videotestsrc")
    w2 = make_win(test)
    test.start()

    gtk.main()


