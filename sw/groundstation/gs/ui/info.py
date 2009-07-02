import os.path
import gtk

import gs.ui

def set_image_from_file(image, filename):
    pass

class InfoBox(gs.ui.GtkBuilderWidget):
    def __init__(self):
        me = os.path.abspath(__file__)
        uifile = os.path.join(os.path.dirname(me), "info.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self.box = self.get_resource("info_hbox")

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
