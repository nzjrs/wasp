import optparse
import os.path
import struct

import xmlobject

#maps user defined names to python struct compatible ids
TYPE_TO_STRUCT_MAP = {
        "uint8" :   "B",
        "int8"  :   "b",
        "uint16":   "H",
        "int16" :   "h",
        "uint32":   "I",
        "int32" :   "i",
        "float" :   "f"
}
#Messages are packed in the payload in little endian format
MESSAGE_ENDIANESS = "<"


class MessageError(Exception):
    pass

class Field:
    def __init__(self, name, typ, node):
        self._type = typ
        self._name = name

        if self._type == "uint8":
            try:
                self._enum_values = node.values.split("|")
            except AttributeError:
                self._enum_values = []
    
        if self._type.endswith("[]"):
            typ = self._type.split("[]")[0]
            self._is_array = True
            self._format = TYPE_TO_STRUCT_MAP[typ]
            self._size = struct.calcsize(self._format)
        else:
            self._is_array = False
            self._format = MESSAGE_ENDIANESS+TYPE_TO_STRUCT_MAP[self._type]
            self._size = struct.calcsize(self._format)

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

        self._isenum = self._type == "uint8" and self._enum_values

    def is_array(self):
        return self._is_array

    def get_size(self, buf, start):
        if self._is_array:
            l = struct.unpack("B",buf[start])[0]
            return l*self._size
        else:
            return self._size

    def unpack_value_from_buffer(self, buf, start):
        if self._is_array:
            l = struct.unpack("B",buf[start])[0]
            start += 1
            return struct.unpack(MESSAGE_ENDIANESS+(l*self._format),buf[start:]), start
        else:
            return struct.unpack(self._format,buf[start]), start + self._size
            

    def get_printable_value(self, value):
        if self._is_array:
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

    def __str__(self):
        return "<Field: %s (%s)>" % (self._name, self._type)


class Message:

    def __init__(self, name, id, node):
        self._name = name
        self._id = id
        self._fields = []
        self._fields_by_name = {}
        self._contains_array_field = False
        
        try:
            #
            #FIXME: Work around a bug in xmlobject where single children are
            #not seen
            fields = node.field
            if len(fields) == 0:
                fields = [fields]

            format = MESSAGE_ENDIANESS
            for f in fields:
                try:
                    if f.type.endswith("[]"):
                        self._contains_array_field = True
                    else:
                        format += TYPE_TO_STRUCT_MAP[f.type]

                    field = Field(f.name, f.type, f)
                    self._fields.append(field)
                    self._fields_by_name[f.name] = field
                except KeyError:
                    #messages must contain a type we know how to process
                    raise MessageError("Field in %s message is an unknown type (%s)" % (self._name, f.type))
                except AttributeError:
                    #messages must contain a name and a type at least
                    raise MessageError("Field in %s message %s is missing a name or type attribute" % self._name)

            #cache the struct for performace reasons
            self._struct = struct.Struct(format)

        except AttributeError:
            #messages can contain 0 fields
            pass


    def get_fields(self):
        return self._fields

    def get_field_by_name(self, name):
        try:
            return self._fields_by_name[name]
        except KeyError:
            return None

    def unpack_values(self, string):
        if self._fields:
            if self._contains_array_field:
                start = 0
                vals = []
                for f in self._fields:
                    v, start = f.unpack_value_from_buffer(string, start)
                    vals += v
                return vals
            else:
                return self._struct.unpack(string)
        return ()

    def unpack_printable_values(self, string, joiner=" "):
        if self._contains_array_field:
                start = 0
                strings = []
                for f in self._fields:
                    vals, start = f.unpack_value_from_buffer(string, start)
                    strings.append(
                                f.get_printable_value(vals)
                    )
                return joiner.join(strings)
        else:
            vals = self.unpack_values(string)
            assert len(vals) == len(self._fields)
            #fastest way to do string concentation
            #http://www.skymind.com/~ocrow/python_string/
            #equivilent to
            #for i in range(len(self._fields)):
            #    v = self._fields[i].get_printable_value(vals[i])
            return joiner.join([
                        self._fields[i].get_printable_value(vals[i]) 
                            for i in range(len(self._fields))])

    def get_id(self):
        return int(self._id)

    def __str__(self):
        return "<Message: %s (%s)>" % (self._name, self._id)

class MessagesFile:
    def __init__(self, xmlfile, debug):
        self._debug = debug
        if not os.path.exists(xmlfile):
            raise Exception("Message file not found: %s" % xmlfile)

        try:
            self._messages = xmlobject.XMLFile(path=xmlfile).root.message
        except AttributeError:
            raise Exception("Error parsing messages")
        
        self._msgs_by_id = {}
        self._msgs_by_name = {}

    def parse(self):
        for m in self._messages:
            try:
                msg = Message(m.name, m.id, m)
                self._msgs_by_id[int(m.id)] = msg
                self._msgs_by_name[m.name] = msg
            except AttributeError, e:
                if self._debug:
                    print "INVALID MESSAGES", e
            except MessageError, e:
                if self._debug:
                    print "SKIPPED MESSAGE %s" % e

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


