import datetime
import logging
import os.path
import gtk

import gs.ui

LOG = logging.getLogger("infobox")

def set_image_from_file(image, filename):
    pb = gtk.gdk.pixbuf_new_from_file_at_size(
                    filename,
                    *gtk.icon_size_lookup(gtk.ICON_SIZE_DIALOG)
    )
    image.set_from_pixbuf(pb)

class InfoBox(gs.ui.GtkBuilderWidget):
    def __init__(self, source):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "info.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self.box = self.get_resource("info_vbox")

        #change the status icon
        set_image_from_file(
            self.get_resource("status_image"),
            os.path.join(mydir,"icons","dashboard.svg")
        )

        source.register_interest(self._on_status, 5, "STATUS")
        source.register_interest(self._on_time, 2, "TIME")
        source.register_interest(self._on_build_info, 2, "BUILD_INFO")


    def _on_status(self, msg, payload):
        rc, gps = msg.unpack_printable_values(payload, joiner=None)
        self.get_resource("rc_value").set_text(rc)
        self.get_resource("gps_value").set_text(gps)

    def _on_time(self, msg, payload):
        runtime, = msg.unpack_printable_values(payload, joiner=None)
        self.get_resource("runtime_value").set_text(runtime)

    def _on_build_info(self, msg, payload):
        rev, branch, target, dirty, time = msg.unpack_printable_values(payload, joiner=None)

        #gtk.Label does not like strings with embedded null
        def denull(s):
            return s.replace("\x00","")

        self.get_resource("rev_value").set_text(denull(rev))
        self.get_resource("branch_value").set_text(denull(branch))
        self.get_resource("target_value").set_text(denull(target))
        self.get_resource("dirty_value").set_text(dirty)

        t = datetime.datetime.fromtimestamp(int(time))
        self.get_resource("time_value").set_text(t.strftime("%d/%m/%Y %H:%M:%S"))


if __name__ == "__main__":
    i = InfoBox()

    w = gtk.Window()
    w.add(i.box)
    w.show_all()
    w.connect("delete-event", lambda *a: gtk.main_quit())

    i.set_build_info("123", 0, 0, 0, 0)

    gtk.main()
