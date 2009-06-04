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
