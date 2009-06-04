#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Open GPS Daemon - UBX parser class

(C) 2008 Daniel Willmann <daniel@totalueberwachung.de>
(C) 2008 Openmoko, Inc.
GPLv2
"""

__version__ = "0.0.0"

import logging
logging.basicConfig(level=logging.DEBUG)
import calendar
import struct

from gpsdevice import GPSDevice

logger = logging.getLogger()

#DBUS_INTERFACE = "org.freesmartphone.GPS"

SYNC1=0xb5
SYNC2=0x62

CLASS = {
    "NAV" : 0x01,
    "RXM" : 0x02,
    "INF" : 0x04,
    "ACK" : 0x05,
    "CFG" : 0x06,
    "UPD" : 0x09,
    "MON" : 0x0a,
    "AID" : 0x0b,
    "TIM" : 0x0d,
    "USR" : 0x40
}

CLIDPAIR = {
    "ACK-ACK" : (0x05, 0x01),
    "ACK-NACK" : (0x05, 0x00),
    "AID-ALM" : (0x0b, 0x30),
    "AID-DATA" : (0x0b, 0x10),
    "AID-EPH" : (0x0b, 0x31),
    "AID-HUI" : (0x0b, 0x02),
    "AID-INI" : (0x0b, 0x01),
    "AID-REQ" : (0x0b, 0x00),
    "CFG-ANT" : (0x06, 0x13),
    "CFG-CFG" : (0x06, 0x09),
    "CFG-DAT" : (0x06, 0x06),
    "CFG-EKF" : (0x06, 0x12),
    "CFG-FXN" : (0x06, 0x0e),
    "CFG-INF" : (0x06, 0x02),
    "CFG-LIC" : (0x06, 0x80),
    "CFG-MSG" : (0x06, 0x01),
    "CFG-NAV2" : (0x06, 0x1a),
    "CFG-NMEA" : (0x06, 0x17),
    "CFG-PRT" : (0x06, 0x00),
    "CFG-RATE" : (0x06, 0x08),
    "CFG-RST" : (0x06, 0x04),
    "CFG-RXM" : (0x06, 0x11),
    "CFG-SBAS" : (0x06, 0x16),
    "CFG-TM" : (0x06, 0x10),
    "CFG-TM2" : (0x06, 0x19),
    "CFG-TMODE" : (0x06, 0x1d),
    "CFG-TP" : (0x06, 0x07),
    "CFG-USB" : (0x06, 0x1b),
    "INF-DEBUG" : (0x04, 0x04),
    "INF-ERROR" : (0x04, 0x00),
    "INF-NOTICE" : (0x04, 0x02),
    "INF-TEST" : (0x04, 0x03),
    "INF-USER" : (0x04, 0x07),
    "INF-WARNING" : (0x04, 0x01),
    "MON-EXCEPT" : (0x0a, 0x05),
    "MON-HW" : (0x0a, 0x09),
    "MON-IO" : (0x0a, 0x02),
    "MON-IPC" : (0x0a, 0x03),
    "MON-MSGPP" : (0x0a, 0x06),
    "MON-RXBUF" : (0x0a, 0x07),
    "MON-SCHD" : (0x0a, 0x01),
    "MON-TXBUF" : (0x0a, 0x08),
    "MON-USB" : (0x0a, 0x0a),
    "MON-VER" : (0x0a, 0x04),
    "NAV-CLOCK" : (0x01, 0x22),
    "NAV-DGPS" : (0x01, 0x31),
    "NAV-DOP" : (0x01, 0x04),
    "NAV-EKFSTATUS" : (0x01, 0x40),
    "NAV-POSECEF" : (0x01, 0x01),
    "NAV-POSLLH" : (0x01, 0x02),
    "NAV-POSUTM" : (0x01, 0x08),
    "NAV-SBAS" : (0x01, 0x32),
    "NAV-SOL" : (0x01, 0x06),
    "NAV-STATUS" : (0x01, 0x03),
    "NAV-SVINFO" : (0x01, 0x30),
    "NAV-TIMEGPS" : (0x01, 0x20),
    "NAV-TIMEUTC" : (0x01, 0x21),
    "NAV-VELECEF" : (0x01, 0x11),
    "NAV-VELNED" : (0x01, 0x12),
    "RXM-ALM" : (0x02, 0x30),
    "RXM-EPH" : (0x02, 0x31),
    "RXM-POSREQ" : (0x02, 0x40),
    "RXM-RAW" : (0x02, 0x10),
    "RXM-SFRB" : (0x02, 0x11),
    "RXM-SVSI" : (0x02, 0x20),
    "TIM-SVIN" : (0x0d, 0x04),
    "TIM-TM" : (0x0d, 0x02),
    "TIM-TM2" : (0x0d, 0x03),
    "TIM-TP" : (0x0d, 0x01),
    "UPD-DOWNL" : (0x09, 0x01),
    "UPD-EXEC" : (0x09, 0x03),
    "UPD-MEMCPY" : (0x09, 0x04),
    "UPD-UPLOAD" : (0x09, 0x02)
}

CLIDPAIR_INV = dict( [ [v,k] for k,v in CLIDPAIR.items() ] )

MSGFMT = {
    ("NAV-POSECEF", 20) :
        ["<IiiiI", ["ITOW", "ECEF_X", "ECEF_Y", "ECEF_Z", "Pacc"]],
    ("NAV-POSLLH", 28) :
        ["<IiiiiII", ["ITOW", "LON", "LAT", "HEIGHT", "HMSL", "Hacc", "Vacc"]],
    ("NAV-POSUTM", 18) :
        ["<Iiiibb", ["ITOW", "EAST", "NORTH", "ALT", "ZONE", "HEM"]],
    ("NAV-DOP", 18) :
        ["<IHHHHHHH", ["ITOW", "GDOP", "PDOP", "TDOP", "VDOP", "HDOP", "NDOP", "EDOP"]],
    ("NAV-STATUS", 16) :
        ["<IBBBxII", ["ITOW", "GPSfix", "Flags", "DiffS", "TTFF", "MSSS"]],
    ("NAV-SOL", 52) :
        ["<IihBBiiiIiiiIHxBxxxx", ["ITOW", "Frac", "week", "GPSFix", "Flags", "ECEF_X", "ECEF_Y", "ECEF_Z", "Pacc",
         "ECEFVX", "ECEFVY", "ECEFVZ", "SAcc", "PDOP", "numSV"]],
    ("NAV-VELECEF", 20) :
        ["<IiiiI", ["ITOW", "ECEFVX", "ECEFVY", "ECEFVZ", "SAcc"]],
    ("NAV-VELNED", 36) :
        ["<IiiiIIiII", ["ITOW", "VEL_N", "VEL_E", "VEL_D", "Speed", "GSpeed", "Heading", "SAcc", "CAcc"]],
    ("NAV-TIMEGPS", 16) :
        ["<IihbBI", ["ITOW", "Frac", "week", "LeapS", "Valid", "TAcc"]],
    ("NAV-TIMEUTC", 20) :
        ["<IIiHBBBBBB", ["ITOW", "TAcc", "Nano", "Year", "Month", "Day", "Hour", "Min", "Sec", "Valid"]],
    ("NAV-CLOCK",  20) :
        ["<IiiII", ["ITOW", "CLKB", "CLKD", "TAcc", "FAcc"]],
    ("NAV-SVINFO", None) :
        [8, "<IBxxx", ["ITOW", "NCH"], 12, "<BBBbBbhi", ["chn", "SVID", "Flags", "QI", "CNO", "Elev", "Azim", "PRRes"]],
    ("NAV-DGPS", None) :
        [16, "<IihhBBxx", ["ITOW", "AGE", "BASEID", "BASEHLTH", "NCH", "STATUS"], 12, "<BBHff", ["SVID", "Flags", "AGECH", "PRC", "PRRC"]],
    ("NAV-SBAS", None) :
        [12, "<IBBbBBxxx", ["ITOW", "GEO", "MODE", "SYS", "SERVICE", "CNT"], 12, "<BBBBBxhxxh", ["SVID", "FLAGS", "UDRE", "SYSn", "SERVICEn", "PRC", "IC"]],
# NAV-EKFSTATUS - Dead reckoning
    ("RXM-RAW", None) :
        [8, "<ihBx", ["ITOW", "Week", "NSV"], 24, "<ddfBbbB", ["CPMes", "PRMes", "DOMes", "SV", "MesQI", "CNO", "LLI"]],
    ("RXM-SVSI", None) :
        [8, "<ihBB", ["ITOW", "Week", "NumVis", "NumSv"], 6, "<BBhbB", ["SVID", "SVFlag", "Azim", "Elev", "Age"]],
# RXM-SFRB - Subframe buffer
    ("RXM-ALM", 1) :
        ["<B", ["SVID"]],
    ("RXM-ALM", 8)  :
        ["<II", ["SVID", "WEEK"]],
    ("RXM-ALM", 40) :
        ["<" + "I"*10, ["SVID", "WEEK", "DWRD0", "DWRD1", "DWRD2", "DWRD3", "DWRD4", "DWRD5", "DWRD6", "DWRD7"]],
    ("RXM-EPH", 1) :
        ["<B", ["SVID"]],
    ("RXM-EPH", 8) :
        ["<II", ["SVID", "HOW"]],
    ("RXM-EPH", 104) :
        ["<" + "I"*26, ["SVID", "HOW", "SF1D0", "SF1D1", "SF1D2", "SF1D3", "SF1D4",
            "SF1D5", "SF1D6", "SF1D7", "SF2D0", "SF2D1", "SF2D2", "SF2D3", "SF2D4",
            "SF2D5", "SF2D6", "SF1D7", "SF3D0", "SF3D1", "SF3D2", "SF3D3", "SF3D4", "SF3D5", "SF3D6", "SF3D7"]],
    ("INF-ERROR", None) :
        [0, "", [], 1, "c", ["Char"]],
    ("INF-WARNING", None) :
        [0, "", [], 1, "c", ["Char"]],
    ("INF-NOTICE", None) :
        [0, "", [], 1, "c", ["Char"]],
    ("INF-TEST", None) :
        [0, "", [], 1, "c", ["Char"]],
    ("INF-DEBUG", None) :
       [0, "", [], 1, "c", ["Char"]],
    ("INF-USER", None) :
        [0, "", [], 1, "c", ["Char"]],
    ("ACK-ACK", 2) :
        ["<BB", ["ClsID", "MsgID"]],
    ("ACK-NACK", 2) :
        ["<BB", ["ClsID", "MsgID"]],
    ("CFG-PRT", 1) :
        ["<B", ["PortID"]],
    ("CFG-PRT", None) :
        [0, "", [], 20, "<BxxxIIHHHxx", ["PortID", "Mode", "Baudrate", "In_proto_mask", "Out_proto_mask", "Flags"]],
    ("CFG-USB", 108) :
        ["<HHxxHHH32s32s32s", ["VendorID", "ProductID", "reserved2", "PowerConsumption", "Flags", "VendorString", "ProductString", "SerialNumber"]],
    ("CFG-MSG", 2) :
        ["<BB", ["Class", "MsgID"]],
    ("CFG-MSG", 3) :
        ["<BBB", ["Class", "MsgID", "Rate"]],
    ("CFG-NMEA", 4) :
        ["<BBBB", ["Filter", "Version", "NumSV", "Flags"]],
    ("CFG-RATE", 6) :
        ["<HHH", ["Meas", "Nav", "Time"]],
    ("CFG-CFG", 12) :
        ["<III", ["Clear_mask", "Save_mask", "Load_mask"]],
    ("CFG-TP", 20) :
        ["<IIbBxxhhi", ["interval", "length", "status", "time_ref", "antenna_cable_delay", "RF_group_delay", "user_delay"]],
    ("CFG-NAV2", 40) :
        ["<BxxxBBBBiBBBBBBxxHHHHBxxxxxxxxxxx", ["Platform", "MinSVInitial", "MinSVs", "MaxSVs", "FixMode",
         "FixedAltitude", "MinCN0Initial", "MinCN0After", "MinELE", "DGPSTO", "MaxDR", "NAVOPT", "PDOP",
         "TDOP", "PACC", "TACC", "StaticThres"]],
# CFG DAT - Get/Set current Datum
    ("CFG-INF", 1) :
        ["<B", ["ProtocolID"]],
    ("CFG-INF", None) :
        [0, "", [], 8, "<BxxxBBBB", ["ProtocolID", "INFMSG_mask0", "INFMSG_mask1", "INFMSG_mask2", "INFMSG_mask3"]],
    ("CFG-RST", 4) :
        ["<HBx", ["nav_bbr", "Reset"]],
    ("CFG-RXM", 2) :
        ["<BB", ["gps_mode", "lp_mode"]],
    ("CFG-ANT", 4) :
        ["<HH", ["flags", "pins"]],
    ("CFG-FXN", 36) :
        ["<IIIIIIIxxxxI", ["flags", "t_reacq", "t_acq", "t_reacq_off", "t_acq_off", "t_on", "t_off", "base_tow"]],
    ("CFG-SBAS", 8) :
        ["<BBBxI", ["mode", "usage", "maxsbas", "scanmode"]],
    ("CFG-LIC", 12) :
        ["<HHHHHH", ["lic1", "lic2", "lic3", "lic4", "lic5", "lic6"]],
    ("CFG-TM", 12) :
        ["<III", ["INTID", "RATE", "FLAGS"]],
    ("CFG-TM2", 1) :
        ["<B", ["CH"]],
    ("CFG-TM2", 12) :
        ["<BxxxII", ["CH", "RATE", "FLAGS"]],
    ("CFG-TMODE", 28) :
        ["<IiiiIII", ["TimeMode", "FixedPosX", "FixedPosY", "FixedPosZ", "FixedPosVar", "SvinMinDur", "SvinVarLimit"]],
# CFG EKF - Dead Reckoning
# UPD - Lowlevel memory manipulation
    ("MON-SCHD", 24) :
        ["<IIIIHHHBB", ["TSKRUN", "TSKSCHD", "TSKOVRR", "TSKREG", "STACK", "STACKSIZE", "CPUIDLE", "FLYSLY", "PTLSLY"]],
# MON - GPS system statistics
    ("AID-INI", 48) :
        ["<iiiIHHIiIIiII", ["X", "Y", "Z", "POSACC", "TM_CFG", "WN", "TOW", "TOW_NS", "TACC_MS", "TACC_NS", "CLKD", "CLKDACC", "FLAGS"]],
    ("AID-DATA", 0) :
        ["", []],
    ("AID-HUI", 72) :
        ["<IddiHHHHHHffffffffI", ["HEALTH", "UTC_A1", "UTC_A0", "UTC_TOT", "UTC_WNT",
         "UTC_LS", "UTC_WNF", "UTC_DN", "UTC_LSF", "UTC_SPARE", "KLOB_A0", "KLOB_A1",
         "KLOB_A2", "KLOB_A3", "KLOB_B0", "KLOB_B1", "KLOB_B2", "KLOB_B3", "FLAGS"]],
    ("AID-ALM", 1) :
        ["<B", ["SVID"]],
    ("AID-ALM", 8)  :
        ["<II", ["SVID", "WEEK"]],
    ("AID-ALM", 40) :
        ["<" + "I"*10, ["SVID", "WEEK", "DWRD0", "DWRD1", "DWRD2", "DWRD3", "DWRD4", "DWRD5", "DWRD6", "DWRD7"]],
    ("AID-EPH", 1) :
        ["<B", ["SVID"]],
    ("AID-EPH", 8) :
        ["<II", ["SVID", "HOW"]],
    ("AID-EPH", 104) :
        ["<" + "I"*26, ["SVID", "HOW", "SF1D0", "SF1D1", "SF1D2", "SF1D3", "SF1D4",
            "SF1D5", "SF1D6", "SF1D7", "SF2D0", "SF2D1", "SF2D2", "SF2D3", "SF2D4",
            "SF2D5", "SF2D6", "SF1D7", "SF3D0", "SF3D1", "SF3D2", "SF3D3", "SF3D4", "SF3D5", "SF3D6", "SF3D7"]]
# TIM - Timekeeping
}

MSGFMT_INV = dict( [ [(CLIDPAIR[clid], le),v + [clid]] for (clid, le),v in MSGFMT.items() ] )

class UBXDevice( GPSDevice ):
    def __init__( self ):
        GPSDevice.__init__(self)

        self.gpsfixstatus = 0
        self.buffer = ""
        #self.gpschannel = gpschannel
        #self.gpschannel.setCallback( self.parse )

        self.ack = {"CFG-PRT" : 0}
        self.ubx = {}

    def configure( self ):
        # Use high sensitivity mode
        #self.send("CFG-RXM", 2, {"gps_mode" : 2, "lp_mode" : 0})
        # Enable use of SBAS (even in testmode)
        #self.send("CFG-SBAS", 8, {"mode" : 3, "usage" : 7, "maxsbas" : 3, "scanmode" : 0})

        # Disable NMEA for current port
        self.ubx["CFG-PRT"] = {"In_proto_mask" : 1, "Out_proto_mask" : 1}
        self.ack["CFG-PRT"] = 0
        self.send("CFG-PRT", 0, [])
        # Send NAV STATUS
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-STATUS"][0] , "MsgID" : CLIDPAIR["NAV-STATUS"][1] , "Rate" : 1 })
        # Send NAV POSLLH
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-POSLLH"][0] , "MsgID" : CLIDPAIR["NAV-POSLLH"][1] , "Rate" : 1 })
        # Send NAV VELNED
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-VELNED"][0] , "MsgID" : CLIDPAIR["NAV-VELNED"][1] , "Rate" : 1 })
        # Send NAV POSUTM
        #self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-POSUTM"][0] , "MsgID" : CLIDPAIR["NAV-POSUTM"][1] , "Rate" : 1 })
        # Send NAV TIMEUTC
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-TIMEUTC"][0] , "MsgID" : CLIDPAIR["NAV-TIMEUTC"][1] , "Rate" : 1 })
        # Send NAV DOP
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-DOP"][0] , "MsgID" : CLIDPAIR["NAV-DOP"][1] , "Rate" : 1 })
        # Send NAV SVINFO
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-SVINFO"][0] , "MsgID" : CLIDPAIR["NAV-SVINFO"][1] , "Rate" : 5 })

    def deconfigure( self ):
        # Disable UBX packets
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-STATUS"][0] , "MsgID" : CLIDPAIR["NAV-STATUS"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-POSLLH"][0] , "MsgID" : CLIDPAIR["NAV-POSLLH"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-VELNED"][0] , "MsgID" : CLIDPAIR["NAV-VELNED"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-TIMEUTC"][0] , "MsgID" : CLIDPAIR["NAV-TIMEUTC"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-DOP"][0] , "MsgID" : CLIDPAIR["NAV-DOP"][1] , "Rate" : 0 })
        self.send("CFG-MSG", 3, {"Class" : CLIDPAIR["NAV-SVINFO"][0] , "MsgID" : CLIDPAIR["NAV-SVINFO"][1] , "Rate" : 0 })
        # Enable NMEA again for current port
        self.ubx["CFG-PRT"] = {"In_proto_mask" : 3, "Out_proto_mask" : 3}
        self.ack["CFG-PRT"] = 0
        self.send("CFG-PRT", 0, [])
        # Reset
        self.gpsfixstatus = 0
        self.buffer = ""
        self._reset()

    def parse( self, data ):
        self.buffer += data
        while len(self.buffer) > 0:
            # Find the beginning of a UBX message
            start = self.buffer.find( chr( SYNC1 ) + chr( SYNC2 ) )
            if start != 0:
                logger.info( "Discarded data not UBX \"%s\"" % repr(self.buffer[:start]) )
            self.buffer = self.buffer[start:]
            # Minimum packet length is 8
            if len(self.buffer) < 8:
                return

            (cl, id, length) = struct.unpack("<xxBBH", self.buffer[:6])
            if len(self.buffer) < length + 8:
                return

            if self.checksum(self.buffer[2:length+6]) != struct.unpack("<BB", self.buffer[length+6:length+8]):
                logger.warning( "UBX packed class 0x%x, id 0x%x, length %i failed checksum" % (cl, id, length) )
                self.buffer = self.buffer[2:]
                continue

            # Now we got a valid UBX packet, decode it
            self.decode(cl, id, length, self.buffer[6:length+6])

            # Discard packet
            self.buffer = self.buffer[length+8:]

    def send( self, clid, length, payload ):
        logger.debug( "Sending UBX packet of type %s: %s" % ( clid, payload ) )

        stream = struct.pack("<BBBBH", SYNC1, SYNC2, CLIDPAIR[clid][0], CLIDPAIR[clid][1], length)
        if length > 0:
            try:
                fmt_base = [length] + MSGFMT[(clid,length)]
                fmt_rep = [0, "", []]
                payload_base = payload
            except KeyError:
                format = MSGFMT[(clid, None)]
                fmt_base = format[:3]
                fmt_rep = format[3:]
                payload_base = payload[0]
                payload_rep = payload[1:]
                if (length - fmt_base[0])%fmt_rep[0] != 0:
                    logger.error( "Cannot send: Variable length message class \
                        0x%x, id 0x%x has wrong length %i" % ( cl, id, length ) )
                    return
            stream = stream + struct.pack(fmt_base[1], *[payload_base[i] for i in fmt_base[2]])
            if fmt_rep[0] != 0:
                for i in range(0, (length - fmt_base[0])/fmt_rep[0]):
                    stream = stream + struct.pack(fmt_rep[1], *[payload_rep[i][j] for j in fmt_rep[2]])
        stream = stream + struct.pack("<BB", *self.checksum( stream[2:] ))
        self.gpschannel.send( stream )

    def checksum( self, msg ):
        ck_a = 0
        ck_b = 0
        for i in msg:
            ck_a = ck_a + ord(i)
            ck_b = ck_b + ck_a
        ck_a = ck_a % 256
        ck_b = ck_b % 256
        return (ck_a, ck_b)

    def decode( self, cl, id, length, payload ):
        data = []
        try:
            format = MSGFMT_INV[((cl, id), length)]
            data.append(dict(zip(format[1], struct.unpack(format[0], payload))))
        except KeyError:
            try:
                # Try if this is one of the variable field messages
                format = MSGFMT_INV[((cl, id), None)]
                fmt_base = format[:3]
                fmt_rep = format[3:]
                # Check if the length matches
                if (length - fmt_base[0])%fmt_rep[0] != 0:
                    logger.error( "Variable length message class 0x%x, id 0x%x \
                        has wrong length %i" % ( cl, id, length ) )
                    return
                data.append(dict(zip(fmt_base[2], struct.unpack(fmt_base[1], payload[:fmt_base[0]]))))
                for i in range(0, (length - fmt_base[0])/fmt_rep[0]):
                    offset = fmt_base[0] + fmt_rep[0] * i
                    data.append(dict(zip(fmt_rep[2], struct.unpack(fmt_rep[1], payload[offset:offset+fmt_rep[0]]))))

            except KeyError:
                logger.info( "Unknown message class 0x%x, id 0x%x, length %i" % ( cl, id, length ) )
                return

        logger.debug( "Got UBX packet of type %s: %s" % (format[-1] , data ) )
        methodname = "handle_"+format[-1].replace("-", "_")
        try:
            method = getattr( self, methodname )
        except AttributeError:
            logger.debug( "No method to handle %s: %s" % ( format[-1], data ) )
        else:
            try:
                method( data )
            except Exception, e:
                logger.error( "Error in %s method: %s" % ( methodname, e ) )

    def handle_CFG_PRT( self, data ):
        data = data[1]
        config = {}
        for (k,v) in data.items():
            config[k] = v
        for (k,v) in self.ubx["CFG-PRT"].items():
           config[k] = v
        logger.debug( "Updating CFG-PRT %s with %s" % (data, config) )
        if not self.ack["CFG-PRT"]:
            self.ack["CFG-PRT"] = 0
            self.send( "CFG-PRT", 20, [{}, config] )

    def handle_NAV_STATUS( self, data ):
        data = data[0]
        fixtranstbl = [ 1, 1, 2, 3, 2, 1 ]
        self.gpsfixstatus = fixtranstbl[ data["GPSfix"] ]
        if data["Flags"]&0x01 == 0:
            self.gpsfixstatus = 1
        self._updateFixStatus( self.gpsfixstatus )

    def handle_NAV_POSLLH( self, data ):
        scaling = 10000000.0
        if self.gpsfixstatus == 3:
            valid = 7
        elif self.gpsfixstatus == 2:
            valid = 3
        else:
            valid = 0
        data = data[0]
        self._updatePosition( valid, data["LAT"]/scaling,
                data["LON"]/scaling, data["HEIGHT"]/1000.0 )

    def handle_NAV_DOP( self, data ):
        if self.gpsfixstatus == 3:
            valid = 7
        elif self.gpsfixstatus == 2:
            valid = 2
        else:
            valid = 0
        data = data[0]
        self._updateAccuracy( valid, data["PDOP"]/100.0,
                data["HDOP"]/100.0, data["VDOP"]/100.0 )

    def handle_NAV_VELNED( self, data ):
        if self.gpsfixstatus == 3:
            valid = 7
        elif self.gpsfixstatus == 2:
            valid = 3
        else:
            valid = 0
        data = data[0]
        self._updateCourse( valid, data["GSpeed"]*0.036,
                data["Heading"]/100000.0, data["VEL_D"]*0.036 )

    def handle_NAV_SVINFO( self, data ):
        satellites = []
        base = data[0]
        data = data[1:]
        for sat in data:
            in_use = bool(sat["Flags"] & 0x01)
            # Don't include satellites that are below the horizon
            # (Gypsy interface requires positive elevation)
            if sat["Elev"] > 0:
                satellites.append( (sat["SVID"], in_use, sat["Elev"], sat["Azim"], sat["CNO"]) )
        self._updateSatellites( satellites )

    def handle_NAV_TIMEUTC( self, data ):
        data = data[0]
#        self.time = ( data["Valid"], data["Year"], data["Month"], data["Day"],
#                data["Hour"], data["Min"], data["Sec"] )
#        self.TimeChanged( *self.time )
        time = calendar.timegm( (data["Year"], data["Month"], data["Day"], data["Hour"], data["Min"], data["Sec"]) )
        # Only update if we have the valid UTC time
        # We have valid GPS time (without leap seconds known) much earlier than
        # UTC and they differ by ~17secs at the moment. The leap seconds could
        # be cached so we would know the UTC time +- some seconds much earlier.
        if data["Valid"] & 0x04:
            self._updateTime( time )

    # Ignore ACK packets for now
    def handle_ACK_ACK( self, data ):
        data = data[0]
        logger.debug("Got ACK %s" % data )
        if (data["ClsID"], data["MsgID"]) == CLIDPAIR["CFG-PRT"]:
          self.ack["CFG-PRT"] = 1

if __name__ == "__main__":
    f = open("SERIAL_PORT_01.TXT", "rb")
    g = UBXDevice()
    data = f.read()
    g.parse(data)
    print g.get_lla()

#vim: expandtab
