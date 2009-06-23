import ppz.messages as messages

XML = """<?xml version="1.0"?>
<messages>
   <message name="PONG" id="2"/>
   <message name="TEST_MESSAGE" id="26">
     <field name="a_uint8" type="uint8" values="OK|LOST|REALLY_LOST"/>
     <field name="a_int8" type="int8"/>
     <field name="a_uint16" type="uint16" unit="adc"/>
     <field name="a_int16" type="int16"/>
     <field name="a_uint32" type="uint32" alt_unit="deg/s" alt_unit_coef="0.0139882"/>
     <field name="a_int32" type="int32"/>
     <field name="a_float" type="float"/>
     <field name="a_array" type="uint8[3]"/>
   </message>
   <message name="REQUEST_MESSAGE" id="5">
     <field name="msgid" type="uint8"/>
   </message>
   <periodic>
      <message name="TEST_MESSAGE" frequency="0.5"/>
   </periodic>
</messages>"""
NUM_MESSAGES = 3

PONG_ID = 2
PONG_NAME = "PONG"
TEST_ID = 26
TEST_NAME = "TEST_MESSAGE"

TEST_ACID = 0x78

TEST_MESSAGE_VALUES = (1,-1, 1000, -1000, 100000, -100000, 1.5, 1, 2, 3)
TEST_MESSAGE_PRINT = "LOST -1 1000 adc -1000 1398.82 -100000 1.5 (1, 2, 3)"
TEST_MESSAGE_PAYLOAD = "\x01\xFF\xE8\x03\x18\xFC\xA0\x86\x01\x00\x60\x79\xFE\xFF\x00\x00\xC0\x3F\x01\x02\x03"

PONG_MESSAGE_VALUES = ()
PONG_MESSAGE_PRINT = ""
PONG_MESSAGE_PAYLOAD = ""

def get_mf():
    mf = messages.MessagesFile(raw=XML, debug=False)
    mf.parse()
    return mf

