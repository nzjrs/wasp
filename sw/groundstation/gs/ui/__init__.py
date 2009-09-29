import logging
import os.path
import gtk

LOG = logging.getLogger('gs.ui')

def make_label(text, width=None):
    l = gtk.Label(text)
    if width == None:
        width = len(text)
    if width > 0:
        l.set_width_chars(width)
    l.set_single_line_mode(True)
    l.set_alignment(0.0, 0.5)
    l.set_padding(5, 0)
    return l

def get_icon_pixbuf(name, size=gtk.ICON_SIZE_DIALOG):
    mydir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(mydir, "..", "..", "data", "icons", name)
    try:
        pb = gtk.gdk.pixbuf_new_from_file_at_size(
                        os.path.abspath(filename),
                        *gtk.icon_size_lookup(size)
        )
    except Exception:
        LOG.warn("Error loading icon: %s" % filename, exc_info=True)
        pb = gtk.icon_theme_get_default().load_icon(
                    gtk.STOCK_MISSING_IMAGE, 
                    gtk.icon_size_lookup(size)[0],
                    0)

    return pb

def get_ui_file(name):
    mydir = os.path.dirname(os.path.abspath(__file__))
    ui = os.path.abspath(os.path.join(mydir, name))
    if not os.path.exists(ui):
        raise Exception("Could not find ui file: %s" % ui)
    return ui

class GtkBuilderWidget:
    def __init__(self, uifile):
        self._builder = gtk.Builder()
        self._builder.add_from_file(uifile)
        self._resources = {}

    def set_instance_resources(self, *resources):
        for r in resources:
            setattr(self, "_%s" % r.lower(), self.get_resource(r))

    def get_resource(self, name):
        if name not in self._resources:
            w = self._builder.get_object(name)
            if not w:
                raise Exception("Could not find widget: %s" % name)
            self._resources[name] = w

        return self._resources[name]

    def builder_connect_signals(self):
        self._builder.connect_signals(self)

