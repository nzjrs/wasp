import gtk

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

