import logging
import os.path
import gtk

import gs

LOG = logging.getLogger('gs.ui')

def message_dialog(message, parent, dialogtype=gtk.MESSAGE_ERROR, secondary=None):
    m = gtk.MessageDialog(
                parent,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                dialogtype,
                gtk.BUTTONS_OK,
                message)
    if secondary:
        m.format_secondary_text(secondary)
    m.run()
    m.destroy()

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

def get_icon_pixbuf(name=None, stock=None, size=gtk.ICON_SIZE_DIALOG):
    ok = True
    if name:
        #use png icons on windows
        if gs.IS_WINDOWS:
            name = os.path.splitext(name)[0] + ".png"
        filename = os.path.join(gs.ICON_DIR, name)
        try:
            pb = gtk.gdk.pixbuf_new_from_file_at_size(
                            os.path.abspath(filename),
                            *gtk.icon_size_lookup(size)
            )
        except Exception:
            LOG.warn("Error loading icon: %s" % filename, exc_info=True)
            ok = False
    elif stock:
        try:
            pb = gtk.icon_theme_get_default().load_icon(
                        stock,
                        gtk.icon_size_lookup(size)[0],
                        0)
        except Exception:
            ok = False
            LOG.warn("Error loading stock icon: %s" % stock, exc_info=True)
    else:
        raise ValueError("Must pass and icon name or a stock name")

    if not ok:
        pb = gtk.icon_theme_get_default().load_icon(
                    gtk.STOCK_MISSING_IMAGE, 
                    gtk.icon_size_lookup(size)[0],
                    0)

    return pb

def get_icon_image(*args, **kwargs):
    return gtk.image_new_from_pixbuf(get_icon_pixbuf(*args,**kwargs))

def get_ui_file(name):
    mydir = os.path.dirname(os.path.abspath(__file__))
    ui = os.path.abspath(os.path.join(mydir, name))
    if not os.path.exists(ui):
        raise Exception("Could not find ui file: %s" % ui)
    return ui

class GtkBuilderWidget:
    def __init__(self, filename, abspath=None):
        if not abspath:
            abspath = os.path.join(gs.UI_DIR, filename)
        self._builder = gtk.Builder()
        self._builder.add_from_file(abspath)
        self._resources = {}

    def set_instance_resources(self, *resources):
        for r in resources:
            setattr(self, "_%s" % r.lower(), self.get_resource(r))

    def get_resource(self, name, cache=True):
        if name not in self._resources:
            w = self._builder.get_object(name)
            if not w:
                raise Exception("Could not find widget: %s" % name)
            if not cache:
                return w
            self._resources[name] = w

        return self._resources[name]

    def builder_connect_signals(self):
        self._builder.connect_signals(self)

