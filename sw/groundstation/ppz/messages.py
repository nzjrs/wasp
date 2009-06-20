# vim: ai ts=4 sts=4 et sw=4

import re
import os.path
import struct

import xmlobject

class Field:

    ARRAY_LENGTH = re.compile("^([a-z0-9]+)\[(\d{1,2})\]$")
    TYPE_LENGTH = {
        "char"      :   1,
        "uint8"     :   1,
        "int8"      :   1,
        "uint16"    :   2,
        "int16"     :   2,
        "uint32"    :   4,
        "int32"     :   4,
        "float"     :   4,
    }

    def __init__(self, f):
        self.name = f.name
        self.ctype = f.type
        self.type, self.length = self._get_field_length(f.type)

    def _get_field_length(self, _type):
        #check if it is an array
        m = self.ARRAY_LENGTH.match(_type)
        if m:
            _type, _len = m.groups()
            _len = self.TYPE_LENGTH[_type] * int(_len)
            self.num_elements = int(_len)
            self.element_length = self.TYPE_LENGTH[_type]
            self.is_array = True
        else:
            _len = self.TYPE_LENGTH[_type]
            self.num_elements = 1
            self.element_length = None
            self.is_array = False

        return _type, _len

    def __str__(self):
        return "<Field: %s (%s)>" % (self.name, self.ctype)

class Message:

    def __init__(self, m, field_klass):
        self.name = m.name.upper()
        if int(m.id) <= 255:
            self.id = int(m.id)
        else:
            raise Exception("Message IDs must be <= 255")
        try:
            self.fields = [field_klass(f) for f in xmlobject.ensure_list(m.field)]
        except AttributeError:
            self.fields = []

        self.size = 0
        self.num_values = 0
        for f in self.fields:
            self.size += f.length
            self.num_values += f.num_elements

        self.num_fields = len(self.fields)

    def __str__(self):
        return "<Message: %s (%s)>" % (self.name, self.id)

class PyField(Field):

    #maps user defined names to python struct compatible ids
    TYPE_TO_STRUCT_MAP = {
            "char"  :   "B",    #treat char as uint8 internally, only modify how they are displayed
            "uint8" :   "B",
            "int8"  :   "b",
            "uint16":   "H",
            "int16" :   "h",
            "uint32":   "I",
            "int32" :   "i",
            "float" :   "f"
    }

    def __init__(self, node):
        Field.__init__(self, node)

        if self.type == "uint8":
            try:
                self._enum_values = node.values.split("|")
            except AttributeError:
                self._enum_values = []

        if self.is_array:
            self.format = "%d%s" % (self.num_elements, self.TYPE_TO_STRUCT_MAP[self.type])
        else:
            self.format = self.TYPE_TO_STRUCT_MAP[self.type]
        self._size = struct.calcsize(self.format)
    
        try:
            self._fstr = node.format
        except AttributeError:
            self._fstr = "%s"

        try:
            self._fstr += " %s" % node.unit
        except AttributeError:
            pass

        try:
            self._coef = float(node.alt_unit_coef)
        except:
            self._coef = 1

        self._isenum = self.type == "uint8" and self._enum_values

    def _get_python_type(self):
        if self.type == "float":
            return float
        elif self.type == "char":
            if self.is_array:
                return str
            else:
                return chr
        else:
            return int    

    def get_default_value(self):
        klass = self._get_python_type()
        if self.is_array and self.type != "char":
            return list( [klass() for i in range(self.num_elements)] )
        else:
            return klass()

    def interpret_value_from_user_string(self, string, default=None, sep=","):
        klass = self._get_python_type()
        try:
            if self.is_array and self.type != "char":
                vals = string.split(sep)
                if len(vals) != self.num_elements:
                    raise ValueError
                return list( [klass(v) for v in vals] )
            else:
                return klass(string)
        except ValueError:
            #invalid user input for type
            if default:
                return default
            else:
                return self.get_default_value()

    def get_printable_value(self, value):
        if self.is_array:
            if self.type == "char":
                return "".join([chr(c) for c in value])
            else:
                #Returns a printable array, e.g '[1, 2, 3]'
                return str(value)
        else:
            #Return a single formatted number string
            if self._isenum:
                #If this is an uint8 enum type then return the
                #enum value
                try:
                    return "%s" % self._enum_values[value]
                except IndexError:
                    return "?%s?" % value
            else:
                return self._fstr % (self._coef * value)

class PyMessage(Message):

    #Messages are packed in the payload in little endian format
    MESSAGE_ENDIANESS = "<"

    def __init__(self, name, id, node):
        Message.__init__(self, node, PyField)
        self._fields_by_name = {}
        
        format = self.MESSAGE_ENDIANESS
        for f in self.fields:
            format += f.format
            self._fields_by_name[f.name] = f

        #cache the struct for performace reasons
        self._struct = struct.Struct(format)

    def get_fields(self):
        return self.fields

    def get_field_by_name(self, name):
        try:
            return self._fields_by_name[name]
        except KeyError:
            return None

    def get_field_values(self, vals):
        i = 0
        v = []
        for f in self.fields:
            ne = f.num_elements
            if f.is_array:
                v.append( vals[i:i+ne] )
            else:
                v.append( vals[i] )
            i += ne
        return v

    def pack_values(self, *values):
        assert len(values) == self.num_values, "%s != %s" % (len(values), self.num_values)

        if self.fields:
            return self._struct.pack(*values)
        return ""

    def unpack_values(self, string):
        if self.fields:
            assert type(string) == str
            assert len(string) == self._struct.size, "%s != %s" % (len(string), self._struct.size)
            return self._struct.unpack(string)
        return ()

    def unpack_printable_values(self, string, joiner=" "):
        if self.fields:

            vals = self.unpack_values(string)
            assert len(vals) == self.num_values
            fvals = self.get_field_values(vals)
            assert len(fvals) == self.num_fields

            #fastest way to do string concentation
            #http://www.skymind.com/~ocrow/python_string/
            #equivilent to
            return joiner.join([
                        self.fields[i].get_printable_value(fvals[i]) 
                            for i in range(self.num_fields)])
        else:
            return ""

class MessagesFile:
    def __init__(self, **kwargs):
        self._debug = kwargs.get("debug", False)
        
        path = kwargs.get("path")
        if path and not os.path.exists(path):
            raise Exception("Could not find message file")

        try:
            #Must have >= 1 message element
            messages = xmlobject.XMLFile(**kwargs).root.message
            self._messages = xmlobject.ensure_list(messages)
        except AttributeError:
            raise Exception("Error parsing messages")
        
        self._msgs_by_id = {}
        self._msgs_by_name = {}

    def parse(self):
        for m in self._messages:
            msg = PyMessage(m.name, m.id, m)
            self._msgs_by_id[int(m.id)] = msg
            self._msgs_by_name[m.name] = msg

    def get_messages(self):
        return self._msgs_by_id.values()

    def get_message_by_name(self, name):
        try:
            return self._msgs_by_name[name]
        except KeyError:
            if self._debug:
                print "ERROR: No message %s" % name
            return None

    def get_message_by_id(self, id):
        try:
            return self._msgs_by_id[id]
        except KeyError:
            if self._debug:
                print "ERROR: No message %s" % id
            return None


