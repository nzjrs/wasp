import gtk

import gs.ui

class StatusIcon(gtk.StatusIcon):
    def __init__(self, pixbuf):
        gtk.StatusIcon.__init__(self)
        self.set_visible(True)

        #build two composite pixbufs, one for connected, and one for
        #not connected
        self._normalpb = pixbuf
        self._connectedpb = self._composite_pixbuf(pixbuf, gtk.STOCK_YES)
        self._disconnectedpb = self._composite_pixbuf(pixbuf, gtk.STOCK_NO)

        self.set_from_pixbuf(self._normalpb)

    def uav_connected(self):
        self.set_from_pixbuf(self._connectedpb)

    def uav_disconnected(self):
        self.set_from_pixbuf(self._disconnectedpb)

    def _composite_pixbuf(self, icon, accentName):
        #  _______
        # |       |
        # |    ___|
        # |i  | a |
        # |___|___|
        assert icon.get_width() == icon.get_height()

        isize = icon.get_width()
        asize = isize / 2
        bwidth = isize
        bheight = isize

        accent = gtk.icon_theme_get_default().load_icon(accentName, asize, 0)

        #Composite the accent to the right of the icon
        dest = gtk.gdk.Pixbuf(
                        colorspace=gtk.gdk.COLORSPACE_RGB,
                        has_alpha=True,
                        bits_per_sample=8,
                        width=bwidth,
                        height=bheight
                        )
        dest.fill(0)

        #Composite the icon on the left
        icon.composite(
                    dest=dest,
                    dest_x=0,           #right of icon
                    dest_y=0,           #at the top
                    dest_width=isize,   #use whole accent 1:1
                    dest_height=isize,  #ditto
                    offset_x=0,
                    offset_y=0,
                    scale_x=1,
                    scale_y=1,
                    interp_type=gtk.gdk.INTERP_NEAREST,
                    overall_alpha=255
                    )
        #accent on the right
        accent.composite(
                    dest=dest,
                    dest_x=isize-asize, #right half icon
                    dest_y=isize-asize, #at the bottom
                    dest_width=asize,   #use whole accent 1:1
                    dest_height=asize,  #ditto
                    offset_x=isize-asize,#move self over to the right
                    offset_y=isize-asize,#at the bottom
                    scale_x=1,
                    scale_y=1,
                    interp_type=gtk.gdk.INTERP_NEAREST,
                    overall_alpha=255
                    )

        return dest

if __name__ == "__main__":
    s = StatusIcon(gs.ui.get_icon_pixbuf("rocket.svg"))
    s.connect("activate", lambda s_: s_.uav_connected())
    s.connect("popup-menu", lambda s_,b,t: s_.uav_disconnected())
    gtk.main()

