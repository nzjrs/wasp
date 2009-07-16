#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import xmlobject
import gentools

try:
    import wasp.messages as messages
except ImportError:
    import messages

import string
import optparse
import re
import os.path
import sys

class CField(messages.Field):

    def get_wasp_type(self):
        if self.type == "char":
            return self.type
        else:
            return self.type+"_t"

class Periodic:

    STRUCT =                                                                   \
    "/**\n"                                                                    \
    " * Description of a periodic message.\n"                                  \
    " */\n"                                                                    \
    "typedef struct __PeriodicMessage {\n"                                     \
    "    uint16_t    target;\n"                                                \
    "    uint16_t    cnt;\n"                                                   \
    "    uint8_t     msgid;\n"                                                 \
    "} PeriodicMessage_t;"
    #use a uint8_t for counting how many main iterations
    #to wait until releasing this message for transmission
    CNT_MAX = (2 ** 16) - 1

    def __init__(self, m, periodicfreq=60.0):
        self._periodicfreq = periodicfreq
        self._message = m.name
        self._frequency = float(m.frequency)

        #the main loop runs at periodicfreq. We want to run at frequency
        #calculate how many iterations we must wait before we run
        maxfreq = periodicfreq                      #can't run faster than main
        minfreq = periodicfreq/self.CNT_MAX         #can only count to n

        if self._frequency > minfreq and self._frequency < maxfreq:
            self._target = int(60/self._frequency)
        else:
            raise Exception("periodic freq, f=%s, must be %s < f < %s" % (self._frequency, minfreq, maxfreq))

    def get_initializer(self):
        return "{ %d, %d, MESSAGE_ID_%s }" % (self._target, 0, self._message)

class CMessage(messages.Message):

    STRUCT =                                                                     \
    "/**\n"                                                                      \
    " * A message to be sent.\n"                                                 \
    " */\n"                                                                      \
    "typedef struct __CommMessage {\n"                                           \
    "    uint8_t acid;   /**< Aircraft ID, id of message sender */\n"            \
    "    uint8_t msgid;  /**< ID of message in payload */\n"                     \
    "    uint8_t len;    /**< Length of payload */\n"                            \
    "    uint8_t payload[COMM_MAX_PAYLOAD_LEN] __attribute__ ((aligned));\n"     \
    "    uint8_t ck_a;   /**< Checksum high byte */\n"                           \
    "    uint8_t ck_b;   /**< Checksum low byte */\n"                            \
    "    uint8_t idx;    /**< State vaiable when filling payload. Not sent */\n" \
    "} CommMessage_t;" 

    def __init__(self, m):
        messages.Message.__init__(self, m, CField)
        self.sizes = ["0"] + [str(f.length) for f in self.fields]

    def print_id(self):
        print "#define MESSAGE_ID_%s %d" % (self.name, self.id)

    def print_length(self):
        print "#define MESSAGE_LENGTH_%s (%s)" % (self.name, "+".join(self.sizes))

class _Writer(object):

    def __init__(self, messages, periodic, note, messages_file):
        self.messages = messages
        self.periodic = periodic
        self.note = note
        self.messages_path = messages_path

    def preamble(self):
        pass

    def body(self):
        raise NotImplementedError

    def postamble(self):
        pass

class _CWriter(_Writer):

    def preamble(self):
        gentools.print_header(
            "%s_H" % self.note.upper(),
            generatedfrom=self.messages_path)

        print "#include \"std.h\""
        print
        print "#define COMM_STX 0x99"
        print "#define COMM_MAX_PAYLOAD_LEN 256"
        print "#define COMM_DEFAULT_ACID 120"
        print "#define COMM_NUM_NON_PAYLOAD_BYTES 6"
        print
        print Periodic.STRUCT
        print
        print CMessage.STRUCT
        print
        for m in self.messages:
            m.print_id()
        print
        for m in self.messages:
            m.print_length()
        print
        print "#define NUM_PERIODIC_MESSAGES %d" % len(self.periodic)
        print "#define PERIODIC_MESSAGE_INITIALIZER {", ", ".join([p.get_initializer() for p in self.periodic]), "};"
        print

    def postamble(self):
        gentools.print_footer("%s_H" % self.note.upper())

class MacroWriter(_CWriter):

    CHECK_FN    = "comm_check_free_space"
    START_FN    = "comm_start_message"
    END_FN      = "comm_end_message"
    OVERRUN_FN  = "comm_overrun"
    PUT_CH_FN   = "comm_send_message_ch"

    def _print_send_function(self, m):
        first_params = ["_chan"]

        print "#define MESSAGE_SEND_%s(" % m.name, 
        print ", ".join(first_params + [f.name for f in m.fields]), ") \\"
        print "{ \\"
        print "\tif (%s(_chan, MESSAGE_LENGTH_%s)) { \\" % (self.CHECK_FN, m.name)
        print "\t\t%s(_chan, MESSAGE_ID_%s, MESSAGE_LENGTH_%s); \\" % (self.START_FN, m.name, m.name)
        for f in m.fields:
            if f.is_array:
                offset = 0;
                for i in range(f.num_elements):
                    print "\t\t_Put%sByAddr(_chan, &(%s[%d])) \\" % (f.type.title(), f.name, i)
                    offset += f.element_length
            else:
                print "\t\t_Put%sByAddr(_chan, (%s)) \\" % (f.type.title(), f.name)
        print "\t\t%s(_chan); \\" % self.END_FN
        print "\t} else \\"
        print "\t\t%s(_chan); \\" % self.OVERRUN_FN
        print "}"
        print

    def _print_accessor(self, m):
        offset = 0
        for f in m.fields:
            print "#define MESSAGE_%s_GET_FROM_BUFFER_%s(_payload)" % (m.name, f.name),
            _type = f.get_wasp_type()
            if f.is_array:
                l = f.length * f.element_length
                print "(%s *)((uint8_t*)_payload+%d)" % (_type, offset)
            else:
                l = f.length
                if l == 1:
                    print "(%s)(*((uint8_t*)_payload+%d))" % (_type, offset)
                elif l == 2:
                    print "(%s)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8)" % (_type, offset, offset)
                elif l == 4:
                    if _type == "float_t":
                        print "({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8|((uint32_t)*((uint8_t*)_payload+%d+2))<<16|((uint32_t)*((uint8_t*)_payload+%d+3))<<24); _f.f; })" % (offset, offset, offset, offset)
                    else:
                        print "(%s)(*((uint8_t*)_payload+%d)|*((uint8_t*)_payload+%d+1)<<8|((uint32_t)*((uint8_t*)_payload+%d+2))<<16|((uint32_t)*((uint8_t*)_payload+%d+3))<<24)" % (_type, offset, offset, offset, offset)
            offset += l


    def preamble(self):
        _CWriter.preamble(self)
        print "#define _Put1ByteByAddr(_chan, _byte) {     \\"
        print "\tuint8_t _x = *(_byte);         \\"
        print "\t%s(_chan, _x);     \\" % self.PUT_CH_FN
        print "}"
        print "#define _Put2ByteByAddr(_chan, _byte) { \\"
        print "\t_Put1ByteByAddr(_chan, _byte);    \\"
        print "\t_Put1ByteByAddr(_chan, (const uint8_t*)_byte+1);    \\"
        print "}"
        print "#define _Put4ByteByAddr(_chan, _byte) { \\"
        print "\t_Put2ByteByAddr(_chan, _byte);    \\"
        print "\t_Put2ByteByAddr(_chan, (const uint8_t*)_byte+2);    \\"
        print "}"
        print "#define _PutInt8ByAddr(_chan, _x) _Put1ByteByAddr(_chan, _x)"
        print "#define _PutCharByAddr(_chan, _x) _Put1ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutUint8ByAddr(_chan, _x) _Put1ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutInt16ByAddr(_chan, _x) _Put2ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutUint16ByAddr(_chan, _x) _Put2ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutInt32ByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutUint32ByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print "#define _PutFloatByAddr(_chan, _x) _Put4ByteByAddr(_chan, (const uint8_t*)_x)"
        print

    def body(self):
        for m in self.messages:
            self._print_send_function(m)
        print
        for m in self.messages:
            self._print_accessor(m)

class FunctionWriter(_CWriter):

    def _print_pack_function(self, m):
        name = m.name.lower()
        print "static inline void message_send_%s(" % name,
        print ", ".join(["%s %s" % (f.get_wasp_type(), f.name) for f in m.fields]), ")"
        print "{"
        print "}"

    def preamble(self):
        _CWriter.preamble(self)
        print "static inline void message_start(uint8_t id, uint8_t len)\n{\n}"

    def body(self):
        for m in self.messages:
            self._print_pack_function(m)

class RSTWriter(_Writer):

    TABLE_COL_W  = 10
    TABLE_GAP_W  = 1
    TABLE_HEADER = '='*TABLE_COL_W
    HEADING_LEVELS = ('=','-','^','"')

    def _write_header(self, name, level=0):
        print name
        print self.HEADING_LEVELS[level]*len(name)
        
    def _write_table(self, m, indent=None):
        def _print_field(name, _type, center=False, gap=" "):
            if center:
                f = string.center
            else:
                f = string.ljust

            if indent:
                print indent,
            print "%s%s%s" % ( f(name,self.TABLE_COL_W), gap*self.TABLE_GAP_W, f(_type, self.TABLE_COL_W))

        def _print_header():
            _print_field(self.TABLE_HEADER, self.TABLE_HEADER, center=True)

        def _print_title(name):
            title_w = 2*self.TABLE_COL_W + self.TABLE_GAP_W
            title_ul = "-"*self.TABLE_COL_W

            if indent:
                print indent,
            print string.center(name, title_w)
            _print_field(title_ul, title_ul, gap="-")

        _print_header()
        _print_title("Payload")
        _print_field("name", "type", center=True)
        _print_header()
        
        for f in m.fields:
            _print_field(f.name, f.ctype)
        
        _print_header()

    def preamble(self):
        self._write_header("Messages")
        print
        self._write_header("Message Definitions", level=2)
        print

    def body(self):
        for m in self.messages:

            print " * **%s**" % m.name
            print 
            print "   *ID:* %s" % m.id
            print
            print "   *Payload Length:* %s" % m.size
            print
            self._write_table(m, indent="  ")
            print

        

if __name__ == "__main__":
    OUTPUT_MODES = {
        "macro"     :   MacroWriter,
        "function"  :   FunctionWriter,
        "rst"          :   RSTWriter,
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

        #must have a periodic element
        p = x.root.periodic
        #but periodic messages are optional
        try: 
            pm = xmlobject.ensure_list(p.message)
        except AttributeError:
            pm = []
        periodic = [Periodic(m) for m in pm]
    except:
        import traceback
        parser.error("invalid xml\n%s" % traceback.format_exc())

    writer = klass(messages, periodic, "messages", messages_path)
    writer.preamble()
    writer.body()
    writer.postamble()




