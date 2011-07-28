#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import gentools

try:
    import wasp.messages as messages
    import wasp.xmlobject as xmlobject
except ImportError:
    import messages
    import xmlobject

import optparse
import re
import os.path
import sys

class _RefMixin:
    def get_pointer_to_instance(self):
        if self.is_array:
            return ""
        else:
            return "&"

    def maybe_pass_by_reference(self):
        if self.is_array:
            return "*"
        else:
            return ""

    def maybe_return_by_reference(self):
        if self.is_array:
            return "**"
        else:
            return "*"

class _ChannelField(_RefMixin):
    name = "chan"
    is_array = False
    def get_wasp_type(self):
        return "CommChannel_t"

class _PayloadField(_RefMixin):
    name = "payload"
    is_array = True
    def get_wasp_type(self):
        return "uint8_t"

    def maybe_return_by_reference(self):
        return "*"

class CField(messages.Field, _RefMixin):

    def get_wasp_type(self):
        if self.type == "char":
            return self.type
        elif self.type == "float":
            return self.type
        else:
            return self.type+"_t"

class Periodic:

    # The definition this struct is in messages.h

    #use a uint16_t for counting how many main iterations
    #to wait until releasing this message for transmission
    CNT_MAX = (2 ** 16) - 1

    AVAILABLE_CHANNELS = ("COMM_TELEMETRY", "COMM_0", "COMM_1")

    def __init__(self, name, frequency, chan, periodicfreq=60.0):
        self._periodicfreq = periodicfreq
        self._message = name
        self._frequency = float(frequency)
        self._chan = chan

        #the main loop runs at periodicfreq. We want to run at frequency
        #calculate how many iterations we must wait before we run
        maxfreq = periodicfreq                      #can't run faster than main
        minfreq = periodicfreq/self.CNT_MAX         #can only count to n

        if self._frequency > minfreq and self._frequency < maxfreq:
            self._target = int(periodicfreq/self._frequency)
        else:
            raise Exception("periodic freq, f=%s, must be %s < f < %s" % (self._frequency, minfreq, maxfreq))

        if self._chan not in self.AVAILABLE_CHANNELS:
            raise Exception("invalid channel: %s, must be one of %s" % (self._chan, ",".join(self.AVAILABLE_CHANNELS)))

    def get_initializer(self):
        return "{ %d, %d, MESSAGE_ID_%s, %s }" % (self._target, 0, self._message, self._chan)

class AdjustablePeriodic(Periodic):
    def __init__(self, chan):
        Periodic.__init__(self, "NONE", 1, chan)

class CMessage(messages.Message):

    # The definition this struct is in messages.h

    def __init__(self, m):
        messages.Message.__init__(self, m, CField)
        self.sizes = ["0"] + [str(f.length) for f in self.fields]

    def print_id(self, outfile):
        print >> outfile, "#define MESSAGE_ID_%s %d" % (self.name, self.id)

    def print_length(self, outfile):
        print >> outfile, "#define MESSAGE_LENGTH_%s (%s)" % (self.name, "+".join(self.sizes))

class _Writer(object):

    def __init__(self, messages, periodic, filename, messages_file):
        self.messages = messages
        self.periodic = periodic
        self.filename = filename
        self.messages_path = messages_path

    def _get_filename(self):
        return os.path.splitext(self.filename)[0]

    def preamble(self, outfile):
        pass

    def body(self, outfile):
        raise NotImplementedError

    def postamble(self, outfile):
        pass

class _CWriter(_Writer):

    def _get_include_guard(self):
        return "%s_GENERATED_H" % self._get_filename().upper()

    def _print_std_include(self, outfile):
        print >> outfile, "#include \"std.h\""
        print >> outfile

    def preamble(self, outfile):
        gentools.print_header(
            self._get_include_guard(),
            generatedfrom=self.messages_path,
            outfile=outfile)
        print >> outfile

    def postamble(self, outfile):
        gentools.print_footer(
            self._get_include_guard(),
            outfile=outfile)

class _MacroWriter(_CWriter):

    CHECK_FN    = "comm_check_free_space"
    START_FN    = "comm_start_message"
    END_FN      = "comm_end_message"
    OVERRUN_FN  = "comm_overrun"
    PUT_CH_FN   = "comm_send_message_ch"

    def _print_send_macro(self, m, outfile):
        first_params = ["_chan"]

        print >> outfile, "#define MESSAGE_SEND_%s(" % m.name, 
        print >> outfile, ", ".join(first_params + [f.name for f in m.fields]), ") \\"
        print >> outfile, "{ \\"
        print >> outfile, "\tif (%s(_chan, MESSAGE_LENGTH_%s)) { \\" % (self.CHECK_FN, m.name)
        print >> outfile, "\t\t%s(_chan, MESSAGE_ID_%s, MESSAGE_LENGTH_%s); \\" % (self.START_FN, m.name, m.name)
        for f in m.fields:
            if f.is_array:
                offset = 0;
                for i in range(f.num_elements):
                    print >> outfile, "\t\t_Put%sByAddr(_chan, &(%s[%d])) \\" % (f.type.title(), f.name, i)
                    offset += f.element_length
            else:
                print >> outfile, "\t\t_Put%sByAddr(_chan, (%s)) \\" % (f.type.title(), f.name)
        print >> outfile, "\t\t%s(_chan); \\" % self.END_FN
        print >> outfile, "\t} else \\"
        print >> outfile, "\t\t%s(_chan); \\" % self.OVERRUN_FN
        print >> outfile, "}"
        print >> outfile

    def _print_accessor_macro(self, m, outfile):
        offset = 0
        for f in m.fields:
            print >> outfile, "#define MESSAGE_%s_GET_FROM_BUFFER_%s(_payload)" % (m.name, f.name),
            _type = f.get_wasp_type()
            if f.is_array:
                l = f.length * f.element_length
                print >> outfile, "(%s *)((uint8_t*)_payload+%d)" % (_type, offset)
                print >> outfile, "#define MESSAGE_%s_NUM_ELEMENTS_%s %d" % (m.name, f.name, f.num_elements)
            else:
                l = f.length
                if l == 1:
                    print >> outfile, "(%s)(*((uint8_t*)_payload+%d))" % (_type, offset)
                elif l == 2:
                    print >> outfile, "(%s)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8)" % (_type, offset, offset)
                elif l == 4:
                    if _type == "float":
                        print >> outfile, "({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8|((uint32_t)*((uint8_t*)_payload+%d+2))<<16|((uint32_t)*((uint8_t*)_payload+%d+3))<<24); _f.f; })" % (offset, offset, offset, offset)
                    else:
                        print >> outfile, "(%s)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8|((uint32_t)*((uint8_t*)_payload+%d+2))<<16|((uint32_t)*((uint8_t*)_payload+%d+3))<<24)" % (_type, offset, offset, offset, offset)
            offset += l

    def _print_comm_defines(self, outfile):
        print >> outfile, "#define COMM_STX 0x99"
        print >> outfile, "#define COMM_DEFAULT_ACID 120"
        print >> outfile, "#define COMM_NUM_NON_PAYLOAD_BYTES 6"
        print >> outfile

    def _print_message_ids(self, outfile):
        print >> outfile, "#define MESSAGE_ID_NONE 0"
        for m in self.messages:
            m.print_id(outfile)
        print >> outfile

    def _print_message_lengths(self, outfile):
        for m in self.messages:
            m.print_length(outfile)
        print >> outfile

    def _print_periodic_messages(self, outfile):
        print >> outfile, "#define NUM_PERIODIC_MESSAGES %d" % len(self.periodic)
        print >> outfile, "#define PERIODIC_MESSAGE_INITIALIZER {", ", ".join([p.get_initializer() for p in self.periodic]), "};"
        print >> outfile

    def _print_byte_macros(self, outfile):
        print >> outfile, "#define _Put1ByteByAddr(_chan, _byte) {     \\"
        print >> outfile, "\tuint8_t _x = *(_byte);         \\"
        print >> outfile, "\t%s(_chan, _x);     \\" % self.PUT_CH_FN
        print >> outfile, "}"
        print >> outfile, "#define _Put2ByteByAddr(_chan, _byte) { \\"
        print >> outfile, "\t_Put1ByteByAddr(_chan, _byte);    \\"
        print >> outfile, "\t_Put1ByteByAddr(_chan, (const uint8_t*)_byte+1);    \\"
        print >> outfile, "}"
        print >> outfile, "#define _Put4ByteByAddr(_chan, _byte) { \\"
        print >> outfile, "\t_Put2ByteByAddr(_chan, _byte);    \\"
        print >> outfile, "\t_Put2ByteByAddr(_chan, (const uint8_t*)_byte+2);    \\"
        print >> outfile, "}"
        print >> outfile, "#define _PutInt8ByAddr(_chan, _x) _Put1ByteByAddr(_chan, _x)"
        print >> outfile, "#define _PutCharByAddr(_chan, _x) _Put1ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutUint8ByAddr(_chan, _x) _Put1ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutInt16ByAddr(_chan, _x) _Put2ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutUint16ByAddr(_chan, _x) _Put2ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutInt32ByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutUint32ByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile, "#define _PutFloatByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print >> outfile

class MacroWriter(_MacroWriter):

    def preamble(self, outfile):
        _CWriter.preamble(self, outfile)
        self._print_std_include(outfile)
        self._print_comm_defines(outfile)
        self._print_message_ids(outfile)
        self._print_message_lengths(outfile)
        self._print_periodic_messages(outfile)
        self._print_byte_macros(outfile)

    def body(self, outfile):
        for m in self.messages:
            self._print_send_macro(m, outfile)
        print >> outfile
        for m in self.messages:
            self._print_accessor_macro(m, outfile)

class _FunctionWriter(_MacroWriter):

    def _print_message_name_function(self, outfile, function_body, function_type):
        print >> outfile, "%s const char *\nmessage_get_name (uint8_t id)" % function_type,
        if function_body:
            print >> outfile, "\n{"
            print >> outfile, "\treturn message_name_map[id];"
            print >> outfile, "}"
        else:
            print >> outfile, ";"
        print >> outfile

    def _print_message_name_table(self, outfile):
        msgids = ["NULL"]*256
        for m in self.messages:
            msgids[m.id] = '"%s"' % m.name
        print >> outfile, "const char *message_name_map[] = {"
        print >> outfile, ", ".join(msgids)
        print >> outfile, "};"
        print >> outfile

    def _print_send_function(self, m, outfile, function_body, function_type):
        allfields = [_ChannelField()] + m.fields
        print >> outfile, "%s void\nmessage_send_%s(" % (function_type, m.name.lower()),
        print >> outfile, ", ".join(["%s%s %s" % (f.get_wasp_type(), f.maybe_pass_by_reference(), f.name) for f in allfields]), ")",
        if function_body:
            print >> outfile, "\n{"
            print >> outfile, "\t\t%s(chan, MESSAGE_ID_%s, MESSAGE_LENGTH_%s);" % (self.START_FN, m.name, m.name)
            for f in m.fields:
                if f.is_array:
                    offset = 0;
                    for i in range(f.num_elements):
                        print >> outfile, "\t\t_Put%sByAddr(chan, &(%s[%d]));" % (f.type.title(), f.name, i)
                        offset += f.element_length
                else:
                    print >> outfile, "\t\t_Put%sByAddr(chan, (&%s));" % (f.type.title(), f.name)
            print >> outfile, "\t\t%s(chan);" % self.END_FN
            print >> outfile, "}"
        else:
            print >> outfile, ";"
        print >> outfile

    def _print_unpack_function(self, m, outfile, function_body, function_type):
        allfields = [_PayloadField()] + m.fields
        print >> outfile, "%s void\nmessage_unpack_%s(" % (function_type,m.name.lower()),
        print >> outfile, ", ".join(["%s%s %s" % (f.get_wasp_type(), f.maybe_return_by_reference(), f.name) for f in allfields]), ")",
        if function_body:
            print >> outfile, "\n{"
            for f in m.fields:
                print >> outfile, "\t*%s = MESSAGE_%s_GET_FROM_BUFFER_%s(payload);" % (f.name, m.name.upper(), f.name)
            print >> outfile, "}"
        else:
            print >> outfile, ";"
        print >> outfile

class FunctionWriter(_FunctionWriter):

    def preamble(self, outfile):
        self._print_std_include(outfile)
        print >> outfile, "#include \"%s.h\"" % self._get_filename()
        print >> outfile, "#include \"comm.h\""
        print >> outfile
        self._print_message_lengths(outfile)
        self._print_periodic_messages(outfile)
        self._print_byte_macros(outfile)
        self._print_message_name_table(outfile)
        print >> outfile

    def body(self, outfile):
        for m in self.messages:
            self._print_accessor_macro(m, outfile)
        print >> outfile
        self._print_message_name_function(outfile, True, "")
        print >> outfile
        for m in self.messages:
            self._print_send_function(m, outfile, True, "")
        print >> outfile
        for m in self.messages:
            self._print_unpack_function(m, outfile, True, "")
        print >> outfile

    def postamble(self, outfile):
        pass

class FunctionWriterInline(_FunctionWriter):

    def preamble(self, outfile):
        _CWriter.preamble(self, outfile)
        self._print_std_include(outfile)
        print >> outfile, "#include \"messages_types.h\""
        print >> outfile, "#include \"comm.h\""
        print >> outfile
        self._print_comm_defines(outfile)
        self._print_message_ids(outfile)
        self._print_message_lengths(outfile)
        self._print_periodic_messages(outfile)
        self._print_byte_macros(outfile)

        self._print_message_name_table(outfile)

    def body(self, outfile):
        self._print_message_name_function(outfile, True, "static inline")
        print >> outfile
        for m in self.messages:
            self._print_accessor_macro(m, outfile)
        print >> outfile
        for m in self.messages:
            self._print_send_function(m, outfile, True, "static inline")
        print >> outfile
        for m in self.messages:
            self._print_unpack_function(m, outfile, True, "static inline")
        print >> outfile

class FunctionWriterHeader(_FunctionWriter):

    def preamble(self, outfile):
        _CWriter.preamble(self, outfile)
        self._print_std_include(outfile)
        print >> outfile, "#include \"messages_types.h\""
        print >> outfile
        self._print_comm_defines(outfile)
        self._print_message_ids(outfile)

    def body(self, outfile):
        self._print_message_name_function(outfile, False, "")
        print >> outfile
        for m in self.messages:
            self._print_send_function(m, outfile, False, "")
        print >> outfile
        for m in self.messages:
            self._print_unpack_function(m, outfile, False, "")
        print >> outfile

class RSTWriter(_Writer, gentools.RSTHelper):

    def preamble(self, outfile):
        self.rst_write_header(self._get_filename().replace("-"," ").title(), outfile, level=0)
        print >> outfile
        self.rst_write_comment(outfile, "begin-body")
        print >> outfile

    def body(self, outfile):
        self.rst_write_header("Message Definitions", outfile, level=2)
        print >> outfile
        #sort the messages alphabetically
        self.messages.sort(lambda a,b: cmp(a.name,b.name))
        for m in self.messages:
            self.rst_write_header(m.name, outfile, level=3)
            print >> outfile
            if m.doc:
                #capitalise the first letter
                print >> outfile, "%s%s" % (m.doc[0].upper(), m.doc[1:])
                print >> outfile
            self.rst_write_list(outfile, "ID: %s" % m.id)
            self.rst_write_list(outfile, "Payload Length: %s" % m.size)
            if m.fields:
                print >> outfile
                self.rst_write_table(outfile,
                        "Payload",
                        ("name","type"),
                        [(f.name, f.ctype) for f in m.fields])
            print >> outfile

    def postamble(self, outfile):
        self.rst_write_comment(outfile, "end-body")
        print >> outfile

if __name__ == "__main__":
    OUTPUT_MODES = {
        "macro"         :   MacroWriter,
        "function"      :   FunctionWriter,
        "inlinefunction":   FunctionWriterInline,
        "header"        :   FunctionWriterHeader,
        "rst"           :   RSTWriter,
    }
    OUTPUT_MODES_DEFAULT = "macro"
    OUTPUT_MODES_LIST = ", ".join(OUTPUT_MODES)

    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default="messages.xml",
                    help="messages xml file", metavar="FILE")
    parser.add_option("-f", "--format",
                    default=OUTPUT_MODES_DEFAULT,
                    help="output format: %s [default: %s]" % (OUTPUT_MODES_LIST, OUTPUT_MODES_DEFAULT))
    parser.add_option("-o", "--output",
                    default="",
                    help="output file [default: stdout]", metavar="FILE")

    options, args = parser.parse_args()

    if not os.path.exists(options.messages):
        parser.error("could not find messages.xml")

    try:
        klass = OUTPUT_MODES[options.format]
    except KeyError:
        parser.error("output mode must be one of %s" % OUTPUT_MODES_LIST)

    try:
        messages_path = os.path.abspath(options.messages)
        x = xmlobject.XMLFile(path=messages_path)

        #must have some valid messaeges
        messages = [CMessage(m) for m in x.root.message]
        #check for duplicate message IDs
        ids = {}
        for m in messages:
            try:
                dup = ids[m.id]
                raise Exception("Duplicate Message ID %d in %s and %s" % (m.id, dup.name, m.name))
            except KeyError:
                ids[m.id] = m
        #check for duplicate message names
        names = {}
        for m in messages:
            try:
                dup = names[m.name]
                raise Exception("Duplicate Message names %s and %s" % (dup.name, m.name))
            except KeyError:
                names[m.name] = m

        #must have one or more periodic element(s)
        periodic = []
        for p in xmlobject.ensure_list(x.root.periodic):
            #and it must specify a channel
            chan = p.channel
            
            #but periodic messages are optional
            try: 
                pm = xmlobject.ensure_list(p.message)
            except AttributeError:
                pm = []
            periodic += [Periodic(m.name, m.frequency, chan) for m in pm]

            #the number of adjustable periodic messages are also optional
            try:
                num_adj = int(p.adjustable)
            except AttributeError:
                num_adj = 0

            #leave a number of spaces for adjustable periodic messages
            periodic += [AdjustablePeriodic(chan) for i in range(num_adj)]
    except:
        import traceback
        parser.error("invalid xml\n%s" % traceback.format_exc())

    if options.output:
        f = open(options.output, 'w')
        filename = os.path.basename(options.output)
    else:
        f = sys.stdout
        filename = "messages"

    writer = klass(messages, periodic, filename, messages_path)
    writer.preamble(outfile=f)
    writer.body(outfile=f)
    writer.postamble(outfile=f)

    f.close()




