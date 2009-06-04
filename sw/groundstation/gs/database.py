import sqlite3
import logging

import gs.data as data

LOG = logging.getLogger('database')

class Database:
    def __init__(self, filename):
        self._filename = None
        self._open = False
        self.open_from_file(filename)

    def open_from_file(self, filename):
        #open new database if filename is specified
        if filename and filename != self._filename:
            self.close()
            try:
                self._connection = sqlite3.connect(filename, check_same_thread=False)
            except:
                LOG.info("DB does not exist, creating: %s" % filename)
            self._open = True
            self._cursor = self._connection.cursor()
            #create the flight meta information table
            self._cursor.execute("CREATE TABLE IF NOT EXISTS flight (flight_id INTEGER PRIMARY KEY AUTOINCREMENT, data_source INTEGER, start_time TEXT, end_time TEXT, notes BLOB)")
            #create the flight data table which stores all flight data receviced
            #jump through some hoops to ensure that time is stored as the correct
            #type, and we get commas between fields
            stmt = "CREATE TABLE IF NOT EXISTS flight_data "
            sep = "("
            for k in data.DEFAULT_ATTRIBUTES:
                attrType = data.ATTRIBUTE_TYPE[k]
                if attrType == str:
                    t = "TEXT"
                elif attrType == float:
                    t = "REAL"
                else:
                    raise Exception("Unknown attribute type")

                stmt += "%s %s %s" % (sep, k, t)
                sep = ","
            stmt += ")"
            self._cursor.execute(stmt)
            self._filename = filename
        elif filename and filename == self._filename:
            self.close()
            self._connection = sqlite3.connect(self._filename)
            self._cursor = self._connection.cursor()
            self._open = True

    def fetchall(self, *args):
        self.execute(*args)
        return self._cursor.fetchall()

    def execute(self, *args):
        return self._cursor.execute(*args)

    def is_open(self):
        return self._open
    
    def get_filename(self):
        return self._filename

    def close(self):
        if self._open and self._filename:
            self._cursor.close()
            self._connection.commit()
            self._connection.close()
            self._open = False

