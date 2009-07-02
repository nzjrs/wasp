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

        source.register_interest(self._on_status, "STATUS")

    def _on_status(self, msg, payload):
        rc, gps = msg.unpack_printable_values(payload, joiner=None)
        self.get_resource("rc_value").set_text(rc)
        self.get_resource("gps_value").set_text(gps)

    def set_build_info(self, rev, branch, target, dirty, time):
        self.get_resource("rev_value").set_text(rev)


if __name__ == "__main__":
    i = InfoBox()

    w = gtk.Window()
    w.add(i.box)
    w.show_all()
    w.connect("delete-event", lambda *a: gtk.main_quit())

    i.set_build_info("123", 0, 0, 0, 0)

    gtk.main()
