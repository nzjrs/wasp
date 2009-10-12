/* Generated from /home/john/Programming/paparazzi.git/conf/ubx.xml */
/* Please DO NOT EDIT */

#define UBX_SYNC1 0xB5
#define UBX_SYNC2 0x62

#define UBX_NAV_ID 0x01

#define UBX_NAV_POSLLH_ID 0x02
#define UBX_NAV_POSLLH_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_POSLLH_LON(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+4))<<24)
#define UBX_NAV_POSLLH_LAT(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+8))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+8))<<24)
#define UBX_NAV_POSLLH_HEIGHT(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+12))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+12))<<24)
#define UBX_NAV_POSLLH_HMSL(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+16)|*((uint8_t*)_ubx_payload+1+16)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+16))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+16))<<24)
#define UBX_NAV_POSLLH_Hacc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+20)|*((uint8_t*)_ubx_payload+1+20)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+20))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+20))<<24)
#define UBX_NAV_POSLLH_Vacc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+24)|*((uint8_t*)_ubx_payload+1+24)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+24))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+24))<<24)

#define UbxSend_NAV_POSLLH(itow,lon,lat,height,hmsl,hacc,vacc) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_POSLLH_ID, 28);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  int32_t _lon = lon; UbxSend4ByAddr((uint8_t*)&_lon);\
  int32_t _lat = lat; UbxSend4ByAddr((uint8_t*)&_lat);\
  int32_t _height = height; UbxSend4ByAddr((uint8_t*)&_height);\
  int32_t _hmsl = hmsl; UbxSend4ByAddr((uint8_t*)&_hmsl);\
  uint32_t _hacc = hacc; UbxSend4ByAddr((uint8_t*)&_hacc);\
  uint32_t _vacc = vacc; UbxSend4ByAddr((uint8_t*)&_vacc);\
  UbxTrailer();\
}

#define UBX_NAV_DOP_ID 0x04
#define UBX_NAV_DOP_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_DOP_GDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8)
#define UBX_NAV_DOP_PDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+6)|*((uint8_t*)_ubx_payload+1+6)<<8)
#define UBX_NAV_DOP_TDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8)
#define UBX_NAV_DOP_VDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+10)|*((uint8_t*)_ubx_payload+1+10)<<8)
#define UBX_NAV_DOP_HDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8)
#define UBX_NAV_DOP_NDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+14)|*((uint8_t*)_ubx_payload+1+14)<<8)
#define UBX_NAV_DOP_EDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+16)|*((uint8_t*)_ubx_payload+1+16)<<8)

#define UbxSend_NAV_DOP(itow,gdop,pdop,tdop,vdop,hdop,ndop,edop) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_DOP_ID, 18);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  uint16_t _gdop = gdop; UbxSend2ByAddr((uint8_t*)&_gdop);\
  uint16_t _pdop = pdop; UbxSend2ByAddr((uint8_t*)&_pdop);\
  uint16_t _tdop = tdop; UbxSend2ByAddr((uint8_t*)&_tdop);\
  uint16_t _vdop = vdop; UbxSend2ByAddr((uint8_t*)&_vdop);\
  uint16_t _hdop = hdop; UbxSend2ByAddr((uint8_t*)&_hdop);\
  uint16_t _ndop = ndop; UbxSend2ByAddr((uint8_t*)&_ndop);\
  uint16_t _edop = edop; UbxSend2ByAddr((uint8_t*)&_edop);\
  UbxTrailer();\
}

#define UBX_NAV_SOL_ID 0x06
#define UBX_NAV_SOL_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_SOL_Frac(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+4))<<24)
#define UBX_NAV_SOL_week(_ubx_payload) (int16_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8)
#define UBX_NAV_SOL_GPSfix(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+10))
#define UBX_NAV_SOL_Flags(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+11))
#define UBX_NAV_SOL_ECEF_X(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+12))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+12))<<24)
#define UBX_NAV_SOL_ECEF_Y(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+16)|*((uint8_t*)_ubx_payload+1+16)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+16))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+16))<<24)
#define UBX_NAV_SOL_ECEF_Z(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+20)|*((uint8_t*)_ubx_payload+1+20)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+20))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+20))<<24)
#define UBX_NAV_SOL_Pacc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+24)|*((uint8_t*)_ubx_payload+1+24)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+24))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+24))<<24)
#define UBX_NAV_SOL_ECEFVX(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+28)|*((uint8_t*)_ubx_payload+1+28)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+28))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+28))<<24)
#define UBX_NAV_SOL_ECEFVY(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+32)|*((uint8_t*)_ubx_payload+1+32)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+32))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+32))<<24)
#define UBX_NAV_SOL_ECEFVZ(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+36)|*((uint8_t*)_ubx_payload+1+36)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+36))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+36))<<24)
#define UBX_NAV_SOL_Sacc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+40)|*((uint8_t*)_ubx_payload+1+40)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+40))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+40))<<24)
#define UBX_NAV_SOL_PDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+44)|*((uint8_t*)_ubx_payload+1+44)<<8)
#define UBX_NAV_SOL_res1(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+46))
#define UBX_NAV_SOL_numSV(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+47))
#define UBX_NAV_SOL_res2(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+48)|*((uint8_t*)_ubx_payload+1+48)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+48))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+48))<<24)

#define UbxSend_NAV_SOL(itow,frac,week,gpsfix,flags,ecef_x,ecef_y,ecef_z,pacc,ecefvx,ecefvy,ecefvz,sacc,pdop,res1,numsv,res2) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_SOL_ID, 52);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  int32_t _frac = frac; UbxSend4ByAddr((uint8_t*)&_frac);\
  int16_t _week = week; UbxSend2ByAddr((uint8_t*)&_week);\
  uint8_t _gpsfix = gpsfix; UbxSend1ByAddr((uint8_t*)&_gpsfix);\
  uint8_t _flags = flags; UbxSend1ByAddr((uint8_t*)&_flags);\
  int32_t _ecef_x = ecef_x; UbxSend4ByAddr((uint8_t*)&_ecef_x);\
  int32_t _ecef_y = ecef_y; UbxSend4ByAddr((uint8_t*)&_ecef_y);\
  int32_t _ecef_z = ecef_z; UbxSend4ByAddr((uint8_t*)&_ecef_z);\
  uint32_t _pacc = pacc; UbxSend4ByAddr((uint8_t*)&_pacc);\
  int32_t _ecefvx = ecefvx; UbxSend4ByAddr((uint8_t*)&_ecefvx);\
  int32_t _ecefvy = ecefvy; UbxSend4ByAddr((uint8_t*)&_ecefvy);\
  int32_t _ecefvz = ecefvz; UbxSend4ByAddr((uint8_t*)&_ecefvz);\
  uint32_t _sacc = sacc; UbxSend4ByAddr((uint8_t*)&_sacc);\
  uint16_t _pdop = pdop; UbxSend2ByAddr((uint8_t*)&_pdop);\
  uint8_t _res1 = res1; UbxSend1ByAddr((uint8_t*)&_res1);\
  uint8_t _numsv = numsv; UbxSend1ByAddr((uint8_t*)&_numsv);\
  uint32_t _res2 = res2; UbxSend4ByAddr((uint8_t*)&_res2);\
  UbxTrailer();\
}

#define UBX_NAV_POSUTM_ID 0x08
#define UBX_NAV_POSUTM_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_POSUTM_EAST(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+4))<<24)
#define UBX_NAV_POSUTM_NORTH(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+8))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+8))<<24)
#define UBX_NAV_POSUTM_ALT(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+12))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+12))<<24)
#define UBX_NAV_POSUTM_ZONE(_ubx_payload) (int8_t)(*((uint8_t*)_ubx_payload+16))
#define UBX_NAV_POSUTM_HEM(_ubx_payload) (int8_t)(*((uint8_t*)_ubx_payload+17))

#define UbxSend_NAV_POSUTM(itow,east,north,alt,zone,hem) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_POSUTM_ID, 18);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  int32_t _east = east; UbxSend4ByAddr((uint8_t*)&_east);\
  int32_t _north = north; UbxSend4ByAddr((uint8_t*)&_north);\
  int32_t _alt = alt; UbxSend4ByAddr((uint8_t*)&_alt);\
  int8_t _zone = zone; UbxSend1ByAddr((uint8_t*)&_zone);\
  int8_t _hem = hem; UbxSend1ByAddr((uint8_t*)&_hem);\
  UbxTrailer();\
}

#define UBX_NAV_STATUS_ID 0x03
#define UBX_NAV_STATUS_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_STATUS_GPSfix(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+4))
#define UBX_NAV_STATUS_Flags(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+5))
#define UBX_NAV_STATUS_DiffS(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+6))
#define UBX_NAV_STATUS_res(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+7))
#define UBX_NAV_STATUS_TTFF(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+8))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+8))<<24)
#define UBX_NAV_STATUS_MSSS(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+12))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+12))<<24)

#define UbxSend_NAV_STATUS(itow,gpsfix,flags,diffs,res,ttff,msss) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_STATUS_ID, 16);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  uint8_t _gpsfix = gpsfix; UbxSend1ByAddr((uint8_t*)&_gpsfix);\
  uint8_t _flags = flags; UbxSend1ByAddr((uint8_t*)&_flags);\
  uint8_t _diffs = diffs; UbxSend1ByAddr((uint8_t*)&_diffs);\
  uint8_t _res = res; UbxSend1ByAddr((uint8_t*)&_res);\
  uint32_t _ttff = ttff; UbxSend4ByAddr((uint8_t*)&_ttff);\
  uint32_t _msss = msss; UbxSend4ByAddr((uint8_t*)&_msss);\
  UbxTrailer();\
}

#define UBX_NAV_VELNED_ID 0x12
#define UBX_NAV_VELNED_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_VELNED_VEL_N(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+4))<<24)
#define UBX_NAV_VELNED_VEL_E(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+8))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+8))<<24)
#define UBX_NAV_VELNED_VEL_D(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+12))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+12))<<24)
#define UBX_NAV_VELNED_Speed(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+16)|*((uint8_t*)_ubx_payload+1+16)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+16))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+16))<<24)
#define UBX_NAV_VELNED_GSpeed(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+20)|*((uint8_t*)_ubx_payload+1+20)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+20))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+20))<<24)
#define UBX_NAV_VELNED_Heading(_ubx_payload) (int32_t)(*((uint8_t*)_ubx_payload+24)|*((uint8_t*)_ubx_payload+1+24)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+24))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+24))<<24)
#define UBX_NAV_VELNED_SAcc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+28)|*((uint8_t*)_ubx_payload+1+28)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+28))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+28))<<24)
#define UBX_NAV_VELNED_CAcc(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+32)|*((uint8_t*)_ubx_payload+1+32)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+32))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+32))<<24)

#define UbxSend_NAV_VELNED(itow,vel_n,vel_e,vel_d,speed,gspeed,heading,sacc,cacc) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_VELNED_ID, 36);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  int32_t _vel_n = vel_n; UbxSend4ByAddr((uint8_t*)&_vel_n);\
  int32_t _vel_e = vel_e; UbxSend4ByAddr((uint8_t*)&_vel_e);\
  int32_t _vel_d = vel_d; UbxSend4ByAddr((uint8_t*)&_vel_d);\
  uint32_t _speed = speed; UbxSend4ByAddr((uint8_t*)&_speed);\
  uint32_t _gspeed = gspeed; UbxSend4ByAddr((uint8_t*)&_gspeed);\
  int32_t _heading = heading; UbxSend4ByAddr((uint8_t*)&_heading);\
  uint32_t _sacc = sacc; UbxSend4ByAddr((uint8_t*)&_sacc);\
  uint32_t _cacc = cacc; UbxSend4ByAddr((uint8_t*)&_cacc);\
  UbxTrailer();\
}

#define UBX_NAV_SVINFO_ID 0x30
#define UBX_NAV_SVINFO_ITOW(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_NAV_SVINFO_NCH(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+4))
#define UBX_NAV_SVINFO_RES1(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+5))
#define UBX_NAV_SVINFO_RES2(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+6)|*((uint8_t*)_ubx_payload+1+6)<<8)
#define UBX_NAV_SVINFO_chn(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+8+12*_ubx_block))
#define UBX_NAV_SVINFO_SVID(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+9+12*_ubx_block))
#define UBX_NAV_SVINFO_Flags(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+10+12*_ubx_block))
#define UBX_NAV_SVINFO_QI(_ubx_payload,_ubx_block) (int8_t)(*((uint8_t*)_ubx_payload+11+12*_ubx_block))
#define UBX_NAV_SVINFO_CNO(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+12+12*_ubx_block))
#define UBX_NAV_SVINFO_Elev(_ubx_payload,_ubx_block) (int8_t)(*((uint8_t*)_ubx_payload+13+12*_ubx_block))
#define UBX_NAV_SVINFO_Azim(_ubx_payload,_ubx_block) (int16_t)(*((uint8_t*)_ubx_payload+14+12*_ubx_block)|*((uint8_t*)_ubx_payload+1+14+12*_ubx_block)<<8)
#define UBX_NAV_SVINFO_PRRes(_ubx_payload,_ubx_block) (int32_t)(*((uint8_t*)_ubx_payload+16+12*_ubx_block)|*((uint8_t*)_ubx_payload+1+16+12*_ubx_block)<<8|((int32_t)*((uint8_t*)_ubx_payload+2+16+12*_ubx_block))<<16|((int32_t)*((uint8_t*)_ubx_payload+3+16+12*_ubx_block))<<24)

#define UbxSend_NAV_SVINFO(itow,nch,res1,res2,chn,svid,flags,qi,cno,elev,azim,prres) { \
  UbxHeader(UBX_NAV_ID, UBX_NAV_SVINFO_ID, 20);\
  uint32_t _itow = itow; UbxSend4ByAddr((uint8_t*)&_itow);\
  uint8_t _nch = nch; UbxSend1ByAddr((uint8_t*)&_nch);\
  uint8_t _res1 = res1; UbxSend1ByAddr((uint8_t*)&_res1);\
  uint16_t _res2 = res2; UbxSend2ByAddr((uint8_t*)&_res2);\
  uint8_t _chn = chn; UbxSend1ByAddr((uint8_t*)&_chn);\
  uint8_t _svid = svid; UbxSend1ByAddr((uint8_t*)&_svid);\
  uint8_t _flags = flags; UbxSend1ByAddr((uint8_t*)&_flags);\
  int8_t _qi = qi; UbxSend1ByAddr((uint8_t*)&_qi);\
  uint8_t _cno = cno; UbxSend1ByAddr((uint8_t*)&_cno);\
  int8_t _elev = elev; UbxSend1ByAddr((uint8_t*)&_elev);\
  int16_t _azim = azim; UbxSend2ByAddr((uint8_t*)&_azim);\
  int32_t _prres = prres; UbxSend4ByAddr((uint8_t*)&_prres);\
  UbxTrailer();\
}

#define UBX_CFG_ID 0x06

#define UBX_CFG_PRT_ID 0x00
#define UBX_CFG_PRT_PortId(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+0+20*_ubx_block))
#define UBX_CFG_PRT_ReS0(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+1+20*_ubx_block))
#define UBX_CFG_PRT_ReS1(_ubx_payload,_ubx_block) (uint16_t)(*((uint8_t*)_ubx_payload+2+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+2+20*_ubx_block)<<8)
#define UBX_CFG_PRT_Mode(_ubx_payload,_ubx_block) (uint32_t)(*((uint8_t*)_ubx_payload+4+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+4+20*_ubx_block)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+4+20*_ubx_block))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+4+20*_ubx_block))<<24)
#define UBX_CFG_PRT_Baudrate(_ubx_payload,_ubx_block) (uint32_t)(*((uint8_t*)_ubx_payload+8+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+8+20*_ubx_block)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+8+20*_ubx_block))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+8+20*_ubx_block))<<24)
#define UBX_CFG_PRT_In_proto_mask(_ubx_payload,_ubx_block) (uint16_t)(*((uint8_t*)_ubx_payload+12+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+12+20*_ubx_block)<<8)
#define UBX_CFG_PRT_Out_proto_mask(_ubx_payload,_ubx_block) (uint16_t)(*((uint8_t*)_ubx_payload+14+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+14+20*_ubx_block)<<8)
#define UBX_CFG_PRT_Flags(_ubx_payload,_ubx_block) (uint16_t)(*((uint8_t*)_ubx_payload+16+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+16+20*_ubx_block)<<8)
#define UBX_CFG_PRT_Res2(_ubx_payload,_ubx_block) (uint16_t)(*((uint8_t*)_ubx_payload+18+20*_ubx_block)|*((uint8_t*)_ubx_payload+1+18+20*_ubx_block)<<8)

#define UbxSend_CFG_PRT(portid,res0,res1,mode,baudrate,in_proto_mask,out_proto_mask,flags,res2) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_PRT_ID, 20);\
  uint8_t _portid = portid; UbxSend1ByAddr((uint8_t*)&_portid);\
  uint8_t _res0 = res0; UbxSend1ByAddr((uint8_t*)&_res0);\
  uint16_t _res1 = res1; UbxSend2ByAddr((uint8_t*)&_res1);\
  uint32_t _mode = mode; UbxSend4ByAddr((uint8_t*)&_mode);\
  uint32_t _baudrate = baudrate; UbxSend4ByAddr((uint8_t*)&_baudrate);\
  uint16_t _in_proto_mask = in_proto_mask; UbxSend2ByAddr((uint8_t*)&_in_proto_mask);\
  uint16_t _out_proto_mask = out_proto_mask; UbxSend2ByAddr((uint8_t*)&_out_proto_mask);\
  uint16_t _flags = flags; UbxSend2ByAddr((uint8_t*)&_flags);\
  uint16_t _res2 = res2; UbxSend2ByAddr((uint8_t*)&_res2);\
  UbxTrailer();\
}

#define UBX_CFG_MSG_ID 0x01
#define UBX_CFG_MSG_Class(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+0+6*_ubx_block))
#define UBX_CFG_MSG_MsgId(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+1+6*_ubx_block))
#define UBX_CFG_MSG_Rate0(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+2+6*_ubx_block))
#define UBX_CFG_MSG_Rate1(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+3+6*_ubx_block))
#define UBX_CFG_MSG_Rate2(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+4+6*_ubx_block))
#define UBX_CFG_MSG_Rate3(_ubx_payload,_ubx_block) (uint8_t)(*((uint8_t*)_ubx_payload+5+6*_ubx_block))

#define UbxSend_CFG_MSG(class,msgid,rate0,rate1,rate2,rate3) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_MSG_ID, 6);\
  uint8_t _class = class; UbxSend1ByAddr((uint8_t*)&_class);\
  uint8_t _msgid = msgid; UbxSend1ByAddr((uint8_t*)&_msgid);\
  uint8_t _rate0 = rate0; UbxSend1ByAddr((uint8_t*)&_rate0);\
  uint8_t _rate1 = rate1; UbxSend1ByAddr((uint8_t*)&_rate1);\
  uint8_t _rate2 = rate2; UbxSend1ByAddr((uint8_t*)&_rate2);\
  uint8_t _rate3 = rate3; UbxSend1ByAddr((uint8_t*)&_rate3);\
  UbxTrailer();\
}

#define UBX_CFG_RST_ID 0x04
#define UBX_CFG_RST_nav_bbr(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8)
#define UBX_CFG_RST_Reset(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+2))
#define UBX_CFG_RST_Res(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+3))

#define UbxSend_CFG_RST(nav_bbr,reset,res) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_RST_ID, 4);\
  uint16_t _nav_bbr = nav_bbr; UbxSend2ByAddr((uint8_t*)&_nav_bbr);\
  uint8_t _reset = reset; UbxSend1ByAddr((uint8_t*)&_reset);\
  uint8_t _res = res; UbxSend1ByAddr((uint8_t*)&_res);\
  UbxTrailer();\
}

#define UBX_CFG_RATE_ID 0x08
#define UBX_CFG_RATE_Meas(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8)
#define UBX_CFG_RATE_Nav(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+2)|*((uint8_t*)_ubx_payload+1+2)<<8)
#define UBX_CFG_RATE_Time(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8)

#define UbxSend_CFG_RATE(meas,nav,time) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_RATE_ID, 6);\
  uint16_t _meas = meas; UbxSend2ByAddr((uint8_t*)&_meas);\
  uint16_t _nav = nav; UbxSend2ByAddr((uint8_t*)&_nav);\
  uint16_t _time = time; UbxSend2ByAddr((uint8_t*)&_time);\
  UbxTrailer();\
}

#define UBX_CFG_NAV_ID 0x03
#define UBX_CFG_NAV_Platform(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+0))
#define UBX_CFG_NAV_MinSvs(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+1))
#define UBX_CFG_NAV_MaxSvs(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+2))
#define UBX_CFG_NAV_MinCN0(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+3))
#define UBX_CFG_NAV_AbsCN0(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+4))
#define UBX_CFG_NAV_MinELE(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+5))
#define UBX_CFG_NAV_DGPSTTR(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+6))
#define UBX_CFG_NAV_DGPST0(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+7))
#define UBX_CFG_NAV_PRCAGE(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+8))
#define UBX_CFG_NAV_CPCAGE(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+9))
#define UBX_CFG_NAV_MinCLT(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+10)|*((uint8_t*)_ubx_payload+1+10)<<8)
#define UBX_CFG_NAV_AbsCLT(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+12)|*((uint8_t*)_ubx_payload+1+12)<<8)
#define UBX_CFG_NAV_MaxDR(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+14))
#define UBX_CFG_NAV_NAVOPT(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+15))
#define UBX_CFG_NAV_PDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+16)|*((uint8_t*)_ubx_payload+1+16)<<8)
#define UBX_CFG_NAV_TDOP(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+18)|*((uint8_t*)_ubx_payload+1+18)<<8)
#define UBX_CFG_NAV_PACC(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+20)|*((uint8_t*)_ubx_payload+1+20)<<8)
#define UBX_CFG_NAV_TACC(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+22)|*((uint8_t*)_ubx_payload+1+22)<<8)
#define UBX_CFG_NAV_FACC(_ubx_payload) (uint16_t)(*((uint8_t*)_ubx_payload+24)|*((uint8_t*)_ubx_payload+1+24)<<8)
#define UBX_CFG_NAV_StaticThres(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+26))
#define UBX_CFG_NAV_reserved(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+27))

#define UbxSend_CFG_NAV(platform,minsvs,maxsvs,mincn0,abscn0,minele,dgpsttr,dgpst0,prcage,cpcage,minclt,absclt,maxdr,navopt,pdop,tdop,pacc,tacc,facc,staticthres,reserved) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_NAV_ID, 28);\
  uint8_t _platform = platform; UbxSend1ByAddr((uint8_t*)&_platform);\
  uint8_t _minsvs = minsvs; UbxSend1ByAddr((uint8_t*)&_minsvs);\
  uint8_t _maxsvs = maxsvs; UbxSend1ByAddr((uint8_t*)&_maxsvs);\
  uint8_t _mincn0 = mincn0; UbxSend1ByAddr((uint8_t*)&_mincn0);\
  uint8_t _abscn0 = abscn0; UbxSend1ByAddr((uint8_t*)&_abscn0);\
  uint8_t _minele = minele; UbxSend1ByAddr((uint8_t*)&_minele);\
  uint8_t _dgpsttr = dgpsttr; UbxSend1ByAddr((uint8_t*)&_dgpsttr);\
  uint8_t _dgpst0 = dgpst0; UbxSend1ByAddr((uint8_t*)&_dgpst0);\
  uint8_t _prcage = prcage; UbxSend1ByAddr((uint8_t*)&_prcage);\
  uint8_t _cpcage = cpcage; UbxSend1ByAddr((uint8_t*)&_cpcage);\
  uint16_t _minclt = minclt; UbxSend2ByAddr((uint8_t*)&_minclt);\
  uint16_t _absclt = absclt; UbxSend2ByAddr((uint8_t*)&_absclt);\
  uint8_t _maxdr = maxdr; UbxSend1ByAddr((uint8_t*)&_maxdr);\
  uint8_t _navopt = navopt; UbxSend1ByAddr((uint8_t*)&_navopt);\
  uint16_t _pdop = pdop; UbxSend2ByAddr((uint8_t*)&_pdop);\
  uint16_t _tdop = tdop; UbxSend2ByAddr((uint8_t*)&_tdop);\
  uint16_t _pacc = pacc; UbxSend2ByAddr((uint8_t*)&_pacc);\
  uint16_t _tacc = tacc; UbxSend2ByAddr((uint8_t*)&_tacc);\
  uint16_t _facc = facc; UbxSend2ByAddr((uint8_t*)&_facc);\
  uint8_t _staticthres = staticthres; UbxSend1ByAddr((uint8_t*)&_staticthres);\
  uint8_t _reserved = reserved; UbxSend1ByAddr((uint8_t*)&_reserved);\
  UbxTrailer();\
}

#define UBX_CFG_SBAS_ID 0x16
#define UBX_CFG_SBAS_mode(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+0))
#define UBX_CFG_SBAS_usage(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+1))
#define UBX_CFG_SBAS_maxbas(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+2))
#define UBX_CFG_SBAS_reserved(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+3))
#define UBX_CFG_SBAS_scanmode(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+4))<<24)

#define UbxSend_CFG_SBAS(mode,usage,maxbas,reserved,scanmode) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_SBAS_ID, 8);\
  uint8_t _mode = mode; UbxSend1ByAddr((uint8_t*)&_mode);\
  uint8_t _usage = usage; UbxSend1ByAddr((uint8_t*)&_usage);\
  uint8_t _maxbas = maxbas; UbxSend1ByAddr((uint8_t*)&_maxbas);\
  uint8_t _reserved = reserved; UbxSend1ByAddr((uint8_t*)&_reserved);\
  uint32_t _scanmode = scanmode; UbxSend4ByAddr((uint8_t*)&_scanmode);\
  UbxTrailer();\
}

#define UBX_CFG_CFG_ID 0x09
#define UBX_CFG_CFG_Clear_mask(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+0)|*((uint8_t*)_ubx_payload+1+0)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+0))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+0))<<24)
#define UBX_CFG_CFG_Save_mask(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+4)|*((uint8_t*)_ubx_payload+1+4)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+4))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+4))<<24)
#define UBX_CFG_CFG_Load_mask(_ubx_payload) (uint32_t)(*((uint8_t*)_ubx_payload+8)|*((uint8_t*)_ubx_payload+1+8)<<8|((uint32_t)*((uint8_t*)_ubx_payload+2+8))<<16|((uint32_t)*((uint8_t*)_ubx_payload+3+8))<<24)

#define UbxSend_CFG_CFG(clear_mask,save_mask,load_mask) { \
  UbxHeader(UBX_CFG_ID, UBX_CFG_CFG_ID, 12);\
  uint32_t _clear_mask = clear_mask; UbxSend4ByAddr((uint8_t*)&_clear_mask);\
  uint32_t _save_mask = save_mask; UbxSend4ByAddr((uint8_t*)&_save_mask);\
  uint32_t _load_mask = load_mask; UbxSend4ByAddr((uint8_t*)&_load_mask);\
  UbxTrailer();\
}

#define UBX_ACK_ID 0x05

#define UBX_ACK_ACK_ID 0x01
#define UBX_ACK_ACK_ClsID(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+0))
#define UBX_ACK_ACK_MsgID(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+1))

#define UbxSend_ACK_ACK(clsid,msgid) { \
  UbxHeader(UBX_ACK_ID, UBX_ACK_ACK_ID, 2);\
  uint8_t _clsid = clsid; UbxSend1ByAddr((uint8_t*)&_clsid);\
  uint8_t _msgid = msgid; UbxSend1ByAddr((uint8_t*)&_msgid);\
  UbxTrailer();\
}

#define UBX_ACK_NAK_ID 0x00
#define UBX_ACK_NAK_ClsID(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+0))
#define UBX_ACK_NAK_MsgID(_ubx_payload) (uint8_t)(*((uint8_t*)_ubx_payload+1))

#define UbxSend_ACK_NAK(clsid,msgid) { \
  UbxHeader(UBX_ACK_ID, UBX_ACK_NAK_ID, 2);\
  uint8_t _clsid = clsid; UbxSend1ByAddr((uint8_t*)&_clsid);\
  uint8_t _msgid = msgid; UbxSend1ByAddr((uint8_t*)&_msgid);\
  UbxTrailer();\
}
