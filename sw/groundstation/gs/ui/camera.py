import subprocess
import gtk
import gst

class Camera(gtk.DrawingArea):
    def __init__(self, device="/dev/video0", v4lcmds=[]):
        gtk.DrawingArea.__init__(self)
        self._playing = False
        self._pb = None

        #configure the camera
        for cmd in v4lcmds:
            cmd = ['v4lctl', '-c', device] + cmd
            print cmd
            try:
                if subprocess.call(cmd, executable='v4lctl') != 0:
                    print "Error calling %s" % ' '.join(cmd)
            except OSError: pass


        #configure the pipeline
        #gst-launch-0.10 v4l2src ! autovideosink"
        # Set up the gstreamer pipeline
        self.pipeline = gst.Pipeline("wasp-video")
        self.source = gst.element_factory_make("v4l2src", "src")
        self.source.set_property("device", device)
        self.sink = gst.element_factory_make("autovideosink", "sink")

        self.pipeline.add(self.source, self.sink)
        gst.element_link_many(self.source, self.sink)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._on_message)
        bus.enable_sync_message_emission()
        bus.connect("sync-message::element", self._on_sync_message)

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
        self._playing = True
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self, *args):
        self._playing = False
        self.pipeline.set_state(gst.STATE_NULL)

    def pause(self, *args):
        self._playing = False
        self.pipeline.set_state(gst.STATE_PAUSED)

class CameraWindow(gtk.Window):
    def __init__(self, **kwargs):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self._cam = Camera(**kwargs)
        self._cam.show()
        self.add(self._cam)
        self.connect("destroy", self.stop)

    def start(self, *args):
        self._cam.start()

    def stop(self, *args):
        self._cam.stop()

    def pause(self, *args):
        self._cam.pause()    

if __name__ == "__main__":
    gtk.gdk.threads_init()

    win = CameraWindow(
            device='/dev/video0',
            v4lcmds=[['setnorm', 'PAL-N'], ['setinput', 'Composite1']]
            )
    win.connect("destroy", gtk.main_quit)
    win.show_all()
    win.start()
    gtk.main()


