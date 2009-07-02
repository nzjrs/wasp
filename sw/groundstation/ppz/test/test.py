import os.path
import unittest

import ppz
import ppz.messages as messages
import ppz.transport as transport

#common constants to test against
from testcommon import *

class MessageFileTest(unittest.TestCase):

    def setUp(self):
        self.mf = get_mf()

    def testEmptyLoad(self):
        EMPTY = """<?xml version="1.0"?><messages></messages>"""
        self.failUnlessRaises( Exception, messages.MessagesFile, raw=EMPTY, debug=False)

    def testParse(self):
        XML = """<?xml version="1.0"?><messages><message name="PONG" id="300"/></messages>"""
        mf = messages.MessagesFile(raw=XML)
        self.failUnlessRaises(Exception, mf.parse)

        XML = """<?xml version="1.0"?><messages><message id="2"/></messages>"""
        mf = messages.MessagesFile(raw=XML)
        self.failUnlessRaises(Exception, mf.parse)

        XML = """<?xml version="1.0"?><messages><message name="PONG"/></messages>"""
        mf = messages.MessagesFile(raw=XML)
        self.failUnlessRaises(Exception, mf.parse)

    def testMessage(self):
        msgs = self.mf.get_messages()
        self.failUnless( len(msgs) == NUM_MESSAGES )

    def testGetMessageById(self):
        self.failUnless( self.mf.get_message_by_id(PONG_ID) )
        self.failUnless( self.mf.get_message_by_id(-1) == None )

    def testGetMessageByName(self):
        self.failUnless( self.mf.get_message_by_name(TEST_NAME) )
        self.failUnless( self.mf.get_message_by_name("FOO") == None )

class MessageTest(unittest.TestCase):
    def setUp(self):
        mf = get_mf()
        self.test = mf.get_message_by_name(TEST_NAME)
        self.pong = mf.get_message_by_name(PONG_NAME)

    def testName(self):
        self.assertEqual(self.test.name, TEST_NAME)

    def testID(self):
        _id = self.test.id
        self.failUnless( type(_id) == int )
        self.failUnless( _id == TEST_ID )

    def testPongMessage(self):
        pl = self.pong.pack_values()
        self.failUnless( pl == "" )

        d = self.pong.unpack_values(pl)
        self.failUnlessEqual(d, ())

        pr = self.pong.unpack_printable_values(pl)
        self.failUnlessEqual(pr, "")

    def testTestMessage(self):
        pl = self.test.pack_values( *TEST_MESSAGE_VALUES )
        self.failUnlessEqual(pl, TEST_MESSAGE_PAYLOAD)

        d = self.test.unpack_values(pl)
        self.failUnlessEqual(d, TEST_MESSAGE_VALUES)

        v = self.test.get_field_values(d)
        self.failUnlessEqual( len(v), self.test.num_fields )

        pr = self.test.unpack_printable_values(pl)
        self.failUnlessEqual(pr, TEST_MESSAGE_PRINT)

class FieldTest(unittest.TestCase):
    def setUp(self):
        mf = get_mf()
        self.test = mf.get_message_by_name(TEST_NAME)
        self.pong = mf.get_message_by_name(PONG_NAME)

    def testProps(self):
        u8 = self.test.get_field_by_name("a_uint8")
        self.failUnlessEqual( u8.name, "a_uint8" )
        self.failUnlessEqual( u8.ctype, "uint8" )
        self.failUnlessEqual( u8.type, "uint8" )
        self.failUnlessEqual( u8.length, 1 )
        self.failUnlessEqual( u8.num_elements, 1 )
        self.failUnlessEqual( u8.element_length, None )
        self.failUnlessEqual( u8.is_array, False )

        a = self.test.get_field_by_name("a_array")
        self.failUnlessEqual( a.name, "a_array" )
        self.failUnlessEqual( a.ctype, "uint8[3]" )
        self.failUnlessEqual( a.type, "uint8" )
        self.failUnlessEqual( a.length, 3 )
        self.failUnlessEqual( a.num_elements, 3 )
        self.failUnlessEqual( a.element_length, 1 )
        self.failUnlessEqual( a.is_array, True )

    def testGet(self):
        u8 = self.test.get_field_by_name("foo")
        self.failUnlessEqual(u8, None)

        u8 = self.test.get_field_by_name("a_uint8")
        self.failUnless(u8)

    def testDefault(self):
        u8 = self.test.get_field_by_name("a_uint8")
        self.failUnlessEqual( u8.get_default_value(), 0 )

        f = self.test.get_field_by_name("a_float")
        self.failUnlessEqual( f.get_default_value(), 0.0 )

        a = self.test.get_field_by_name("a_array")
        self.failUnlessEqual( a.get_default_value(), [0,0,0] )

    def testInterpret(self):
        u8 = self.test.get_field_by_name("a_uint8")

        v = u8.interpret_value_from_user_string(12)
        self.failUnlessEqual( v, 12 )

        v = u8.interpret_value_from_user_string(0.1)
        self.failUnlessEqual( v, 0 )

        v = u8.interpret_value_from_user_string("foo", default=42)
        self.failUnlessEqual( v, 42 )


        f = self.test.get_field_by_name("a_float")
        v = f.interpret_value_from_user_string(26.9)
        self.failUnlessEqual( v, 26.9 )

        a = self.test.get_field_by_name("a_array")
        v = a.interpret_value_from_user_string("1,2,3")
        self.failUnlessEqual( v, [1,2,3] )

        v = a.interpret_value_from_user_string("1,2,3,4,5,6")
        self.failUnlessEqual( v, [0,0,0] )

        v = a.interpret_value_from_user_string("foo")
        self.failUnlessEqual( v, [0,0,0] )

    def testPrintable(self):
        u8 = self.test.get_field_by_name("a_uint8")
        v = u8.get_printable_value(0)
        self.failUnlessEqual( v, "OK" )

        i8 = self.test.get_field_by_name("a_int8")
        v = i8.get_printable_value(0)
        self.failUnlessEqual( v, "0" )

        u16 = self.test.get_field_by_name("a_uint16")
        v = u16.get_printable_value(0)
        self.failUnlessEqual( v, "0 adc" )


        f = self.test.get_field_by_name("a_float")
        v = f.get_printable_value( [1,2,3] )
        self.failUnlessEqual( v, "[1, 2, 3]" )

class TestTransportFieldTest(unittest.TestCase):
    def setUp(self):
        mf = get_mf()
        self.test = mf.get_message_by_name(TEST_NAME)
        self.pong = mf.get_message_by_name(PONG_NAME)
        self.transport = transport.Transport(check_crc=True, debug=False)

    def testPack(self):
        data = self.transport.pack_one(
                    transport.TransportHeaderFooter(acid=TEST_ACID), 
                    self.pong,
                    self.pong.pack_values())
        self.failUnless( data )

        data = self.transport.pack_message_with_values(
                    transport.TransportHeaderFooter(acid=TEST_ACID), 
                    self.test,
                    *TEST_MESSAGE_VALUES)
        self.failUnless( data )

    def testUnpack(self):
        h = transport.TransportHeaderFooter(acid=TEST_ACID)
        d1 = self.transport.pack_message_with_values(h, self.pong)
        d2 = self.transport.pack_message_with_values(h, self.test, *TEST_MESSAGE_VALUES)

        string = d1.tostring() + d2.tostring()
        
        payloads = self.transport.parse_many(string)
        self.failUnlessEqual( len(payloads), 2 )

        (pong_header, pong_payload), (test_header, test_payload) = payloads

        #first msg is pong
        self.failUnlessEqual( pong_header.msgid, self.pong.id )
        self.failUnlessEqual( pong_header.acid, TEST_ACID )
        self.failUnlessEqual( pong_header.length, transport.NUM_NON_PAYLOAD_BYTES )
        self.failUnlessEqual( pong_payload, PONG_MESSAGE_PAYLOAD )

        #next msg is test_message
        self.failUnlessEqual( test_header.msgid, self.test.id )
        self.failUnlessEqual( test_header.length, transport.NUM_NON_PAYLOAD_BYTES + self.test.size )
        self.failUnlessEqual( test_payload, TEST_MESSAGE_PAYLOAD )
        
        d = self.test.unpack_values( test_payload )
        self.failUnlessEqual(d, TEST_MESSAGE_VALUES)

if __name__ == "__main__":
    import sys

    cov = None
    try:
        import coverage
        if coverage.__version__ >= '3.0':
           cov = coverage.coverage()
    except ImportError:
        pass

    if cov:
        cov.exclude('if self._debug:')
        cov.exclude('def __str__')
        cov.start()

    TESTS = (MessageFileTest, MessageTest, FieldTest, TestTransportFieldTest)
    r = unittest.TextTestRunner()
    l = unittest.TestLoader()

    q = l.suiteClass([ l.loadTestsFromTestCase(t) for t in TESTS ])
    r.run(q)

    if cov:
        cov.stop()
        cov.html_report(
                morfs=(ppz,ppz.messages, ppz.transport),
                directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "html"))


