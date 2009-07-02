import gtk
import gobject

import gs.data as data

class DBWidget(gtk.TreeView):
    def __init__(self, db):
        gtk.TreeView.__init__(self)

        self._populate_treestore(db)
        self._build_treeview()
        self.set_model(self._db_liststore)

    def _populate_treestore(self, db):
        types = []
        for k in data.DEFAULT_ATTRIBUTES:
            attrType = data.ATTRIBUTE_TYPE[k]
            if attrType == str:
                types.append(gobject.TYPE_STRING)
            elif attrType == float:
                types.append(gobject.TYPE_FLOAT)
            else:
                raise Exception("Unknown attribute type")
        self._db_liststore = gtk.ListStore(*types)

        if db.is_open():
            #calculate the select statment to be sure that we get the data in
            #the same order we inserted it
            stmt = "SELECT "
            sep = ""
            for k in data.DEFAULT_ATTRIBUTES:
                stmt += "%s %s" % (sep, k)
                sep = ","
            stmt += " FROM flight_data LIMIT 100"

            for row in db.execute(stmt):
                self._db_liststore.append( row )

    def _build_treeview(self):
        idx = 0
        for k in data.DEFAULT_ATTRIBUTES:
            col = gtk.TreeViewColumn(k.title())
            cell = gtk.CellRendererText()
            col.pack_start(cell, True)
            col.add_attribute(cell, 'text', idx)
            self.append_column(col)
            idx += 1

