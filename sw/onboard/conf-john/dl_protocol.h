/* Automatically generated from /home/john/Programming/paparazzi.git/conf/messages.xml */
/* Please DO NOT EDIT */
/* Macros to send and receive messages of class datalink */
#define DL_ACINFO 1
#define DL_MOVE_WP 2
#define DL_WIND_INFO 3
#define DL_SETTING 4
#define DL_BLOCK 5
#define DL_HITL_UBX 6
#define DL_HITL_INFRARED 7
#define DL_PING 8
#define DL_FORMATION_SLOT 9
#define DL_FORMATION_STATUS 10
#define DL_JOYSTICK_RAW 11
#define DL_COMMANDS_RAW 12
#define DL_DGPS_RAW 13
#define DL_BOOZ2_FMS_COMMAND 149
#define DL_SET_ACTUATOR 100
#define DL_CSC_SERVO_CMD 101
#define DL_MSG_datalink_NB 16

#define MSG_datalink_LENGTHS {0,(2+0+2+4+4+4+4+2+2+1),(2+0+1+1+4+4+4),(2+0+1+1+4+4+4),(2+0+1+1+4),(2+0+1+1),(2+0+1+1+1+1+nb_ubx_payload*1),(2+0+2+2+2+1),(2+0),(2+0+1+1+4+4+4),(2+0+1+1+1),(2+0+1+1+1+1),(2+0+1+1+nb_commands*1),(2+0+1+1+1+nb_rtcm*1),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,(2+0+2+1+1),(2+0+2+2+2+2),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,(2+0+1+1+4+4+4+4+1),}

#define DOWNLINK_SEND_ACINFO(course, utm_east, utm_north, alt, itow, speed, climb, ac_id){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+2+4+4+4+4+2+2+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+2+4+4+4+4+2+2+1)); \
	  DownlinkStartMessage("ACINFO", DL_ACINFO, 0+2+4+4+4+4+2+2+1) \
	  DownlinkPutInt16ByAddr((course)); \
	  DownlinkPutInt32ByAddr((utm_east)); \
	  DownlinkPutInt32ByAddr((utm_north)); \
	  DownlinkPutInt32ByAddr((alt)); \
	  DownlinkPutUint32ByAddr((itow)); \
	  DownlinkPutUint16ByAddr((speed)); \
	  DownlinkPutInt16ByAddr((climb)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_MOVE_WP(wp_id, ac_id, lat, lon, alt){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+4+4+4))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+4+4+4)); \
	  DownlinkStartMessage("MOVE_WP", DL_MOVE_WP, 0+1+1+4+4+4) \
	  DownlinkPutUint8ByAddr((wp_id)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutInt32ByAddr((lat)); \
	  DownlinkPutInt32ByAddr((lon)); \
	  DownlinkPutInt32ByAddr((alt)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_WIND_INFO(ac_id, pad0, east, north, airspeed){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+4+4+4))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+4+4+4)); \
	  DownlinkStartMessage("WIND_INFO", DL_WIND_INFO, 0+1+1+4+4+4) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutUint8ByAddr((pad0)); \
	  DownlinkPutFloatByAddr((east)); \
	  DownlinkPutFloatByAddr((north)); \
	  DownlinkPutFloatByAddr((airspeed)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_SETTING(index, ac_id, value){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+4))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+4)); \
	  DownlinkStartMessage("SETTING", DL_SETTING, 0+1+1+4) \
	  DownlinkPutUint8ByAddr((index)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutFloatByAddr((value)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_BLOCK(block_id, ac_id){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1)); \
	  DownlinkStartMessage("BLOCK", DL_BLOCK, 0+1+1) \
	  DownlinkPutUint8ByAddr((block_id)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_HITL_UBX(class, id, ac_id, nb_ubx_payload, ubx_payload){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+1+1+nb_ubx_payload*1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+1+1+nb_ubx_payload*1)); \
	  DownlinkStartMessage("HITL_UBX", DL_HITL_UBX, 0+1+1+1+1+nb_ubx_payload*1) \
	  DownlinkPutUint8ByAddr((class)); \
	  DownlinkPutUint8ByAddr((id)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutUint8Array(nb_ubx_payload, ubx_payload); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_HITL_INFRARED(roll, pitch, top, ac_id){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+2+2+2+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+2+2+2+1)); \
	  DownlinkStartMessage("HITL_INFRARED", DL_HITL_INFRARED, 0+2+2+2+1) \
	  DownlinkPutInt16ByAddr((roll)); \
	  DownlinkPutInt16ByAddr((pitch)); \
	  DownlinkPutInt16ByAddr((top)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_PING(){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0)); \
	  DownlinkStartMessage("PING", DL_PING, 0) \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_FORMATION_SLOT(ac_id, mode, slot_east, slot_north, slot_alt){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+4+4+4))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+4+4+4)); \
	  DownlinkStartMessage("FORMATION_SLOT", DL_FORMATION_SLOT, 0+1+1+4+4+4) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutUint8ByAddr((mode)); \
	  DownlinkPutFloatByAddr((slot_east)); \
	  DownlinkPutFloatByAddr((slot_north)); \
	  DownlinkPutFloatByAddr((slot_alt)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_FORMATION_STATUS(ac_id, leader_id, status){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+1)); \
	  DownlinkStartMessage("FORMATION_STATUS", DL_FORMATION_STATUS, 0+1+1+1) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutUint8ByAddr((leader_id)); \
	  DownlinkPutUint8ByAddr((status)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_JOYSTICK_RAW(ac_id, roll, pitch, throttle){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+1+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+1+1)); \
	  DownlinkStartMessage("JOYSTICK_RAW", DL_JOYSTICK_RAW, 0+1+1+1+1) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutInt8ByAddr((roll)); \
	  DownlinkPutInt8ByAddr((pitch)); \
	  DownlinkPutInt8ByAddr((throttle)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_COMMANDS_RAW(ac_id, nb_commands, commands){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+nb_commands*1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+nb_commands*1)); \
	  DownlinkStartMessage("COMMANDS_RAW", DL_COMMANDS_RAW, 0+1+1+nb_commands*1) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutInt8Array(nb_commands, commands); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_DGPS_RAW(ac_id, length, nb_rtcm, rtcm){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+1+nb_rtcm*1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+1+nb_rtcm*1)); \
	  DownlinkStartMessage("DGPS_RAW", DL_DGPS_RAW, 0+1+1+1+nb_rtcm*1) \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkPutUint8ByAddr((length)); \
	  DownlinkPutUint8Array(nb_rtcm, rtcm); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_BOOZ2_FMS_COMMAND(h_mode, v_mode, v_sp, h_sp_1, h_sp_2, h_sp_3, ac_id){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+1+1+4+4+4+4+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+1+1+4+4+4+4+1)); \
	  DownlinkStartMessage("BOOZ2_FMS_COMMAND", DL_BOOZ2_FMS_COMMAND, 0+1+1+4+4+4+4+1) \
	  DownlinkPutUint8ByAddr((h_mode)); \
	  DownlinkPutUint8ByAddr((v_mode)); \
	  DownlinkPutInt32ByAddr((v_sp)); \
	  DownlinkPutInt32ByAddr((h_sp_1)); \
	  DownlinkPutInt32ByAddr((h_sp_2)); \
	  DownlinkPutInt32ByAddr((h_sp_3)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_SET_ACTUATOR(value, no, ac_id){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+2+1+1))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+2+1+1)); \
	  DownlinkStartMessage("SET_ACTUATOR", DL_SET_ACTUATOR, 0+2+1+1) \
	  DownlinkPutUint16ByAddr((value)); \
	  DownlinkPutUint8ByAddr((no)); \
	  DownlinkPutUint8ByAddr((ac_id)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}

#define DOWNLINK_SEND_CSC_SERVO_CMD(servo_1, servo_2, servo_3, servo_4){ \
	if (DownlinkCheckFreeSpace(DownlinkSizeOf(0+2+2+2+2))) {\
	  DownlinkCountBytes(DownlinkSizeOf(0+2+2+2+2)); \
	  DownlinkStartMessage("CSC_SERVO_CMD", DL_CSC_SERVO_CMD, 0+2+2+2+2) \
	  DownlinkPutUint16ByAddr((servo_1)); \
	  DownlinkPutUint16ByAddr((servo_2)); \
	  DownlinkPutUint16ByAddr((servo_3)); \
	  DownlinkPutUint16ByAddr((servo_4)); \
	  DownlinkEndMessage() \
	} else \
	  DownlinkOverrun(); \
}


#define DL_ACINFO_course(_payload) ((int16_t)(*((uint8_t*)_payload+2)|*((uint8_t*)_payload+2+1)<<8))
#define DL_ACINFO_utm_east(_payload) ((int32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24))
#define DL_ACINFO_utm_north(_payload) ((int32_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8|((uint32_t)*((uint8_t*)_payload+8+2))<<16|((uint32_t)*((uint8_t*)_payload+8+3))<<24))
#define DL_ACINFO_alt(_payload) ((int32_t)(*((uint8_t*)_payload+12)|*((uint8_t*)_payload+12+1)<<8|((uint32_t)*((uint8_t*)_payload+12+2))<<16|((uint32_t)*((uint8_t*)_payload+12+3))<<24))
#define DL_ACINFO_itow(_payload) ((uint32_t)(*((uint8_t*)_payload+16)|*((uint8_t*)_payload+16+1)<<8|((uint32_t)*((uint8_t*)_payload+16+2))<<16|((uint32_t)*((uint8_t*)_payload+16+3))<<24))
#define DL_ACINFO_speed(_payload) ((uint16_t)(*((uint8_t*)_payload+20)|*((uint8_t*)_payload+20+1)<<8))
#define DL_ACINFO_climb(_payload) ((int16_t)(*((uint8_t*)_payload+22)|*((uint8_t*)_payload+22+1)<<8))
#define DL_ACINFO_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+24)))

#define DL_MOVE_WP_wp_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_MOVE_WP_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_MOVE_WP_lat(_payload) ((int32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24))
#define DL_MOVE_WP_lon(_payload) ((int32_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8|((uint32_t)*((uint8_t*)_payload+8+2))<<16|((uint32_t)*((uint8_t*)_payload+8+3))<<24))
#define DL_MOVE_WP_alt(_payload) ((int32_t)(*((uint8_t*)_payload+12)|*((uint8_t*)_payload+12+1)<<8|((uint32_t)*((uint8_t*)_payload+12+2))<<16|((uint32_t)*((uint8_t*)_payload+12+3))<<24))

#define DL_WIND_INFO_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_WIND_INFO_pad0(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_WIND_INFO_east(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24); _f.f; }))
#define DL_WIND_INFO_north(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8|((uint32_t)*((uint8_t*)_payload+8+2))<<16|((uint32_t)*((uint8_t*)_payload+8+3))<<24); _f.f; }))
#define DL_WIND_INFO_airspeed(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+12)|*((uint8_t*)_payload+12+1)<<8|((uint32_t)*((uint8_t*)_payload+12+2))<<16|((uint32_t)*((uint8_t*)_payload+12+3))<<24); _f.f; }))

#define DL_SETTING_index(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_SETTING_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_SETTING_value(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24); _f.f; }))

#define DL_BLOCK_block_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_BLOCK_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))

#define DL_HITL_UBX_class(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_HITL_UBX_id(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_HITL_UBX_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+4)))
#define DL_HITL_UBX_ubx_payload_length(_payload) ((uint8_t)(*((uint8_t*)_payload+5)))
#define DL_HITL_UBX_ubx_payload(_payload) ((uint8_t*)_payload+6)

#define DL_HITL_INFRARED_roll(_payload) ((int16_t)(*((uint8_t*)_payload+2)|*((uint8_t*)_payload+2+1)<<8))
#define DL_HITL_INFRARED_pitch(_payload) ((int16_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8))
#define DL_HITL_INFRARED_top(_payload) ((int16_t)(*((uint8_t*)_payload+6)|*((uint8_t*)_payload+6+1)<<8))
#define DL_HITL_INFRARED_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+8)))


#define DL_FORMATION_SLOT_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_FORMATION_SLOT_mode(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_FORMATION_SLOT_slot_east(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24); _f.f; }))
#define DL_FORMATION_SLOT_slot_north(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8|((uint32_t)*((uint8_t*)_payload+8+2))<<16|((uint32_t)*((uint8_t*)_payload+8+3))<<24); _f.f; }))
#define DL_FORMATION_SLOT_slot_alt(_payload) (({ union { uint32_t u; float f; } _f; _f.u = (uint32_t)(*((uint8_t*)_payload+12)|*((uint8_t*)_payload+12+1)<<8|((uint32_t)*((uint8_t*)_payload+12+2))<<16|((uint32_t)*((uint8_t*)_payload+12+3))<<24); _f.f; }))

#define DL_FORMATION_STATUS_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_FORMATION_STATUS_leader_id(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_FORMATION_STATUS_status(_payload) ((uint8_t)(*((uint8_t*)_payload+4)))

#define DL_JOYSTICK_RAW_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_JOYSTICK_RAW_roll(_payload) ((int8_t)(*((uint8_t*)_payload+3)))
#define DL_JOYSTICK_RAW_pitch(_payload) ((int8_t)(*((uint8_t*)_payload+4)))
#define DL_JOYSTICK_RAW_throttle(_payload) ((int8_t)(*((uint8_t*)_payload+5)))

#define DL_COMMANDS_RAW_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_COMMANDS_RAW_commands_length(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_COMMANDS_RAW_commands(_payload) ((int8_t*)_payload+4)

#define DL_DGPS_RAW_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_DGPS_RAW_length(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_DGPS_RAW_rtcm_length(_payload) ((uint8_t)(*((uint8_t*)_payload+4)))
#define DL_DGPS_RAW_rtcm(_payload) ((uint8_t*)_payload+5)

#define DL_BOOZ2_FMS_COMMAND_h_mode(_payload) ((uint8_t)(*((uint8_t*)_payload+2)))
#define DL_BOOZ2_FMS_COMMAND_v_mode(_payload) ((uint8_t)(*((uint8_t*)_payload+3)))
#define DL_BOOZ2_FMS_COMMAND_v_sp(_payload) ((int32_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8|((uint32_t)*((uint8_t*)_payload+4+2))<<16|((uint32_t)*((uint8_t*)_payload+4+3))<<24))
#define DL_BOOZ2_FMS_COMMAND_h_sp_1(_payload) ((int32_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8|((uint32_t)*((uint8_t*)_payload+8+2))<<16|((uint32_t)*((uint8_t*)_payload+8+3))<<24))
#define DL_BOOZ2_FMS_COMMAND_h_sp_2(_payload) ((int32_t)(*((uint8_t*)_payload+12)|*((uint8_t*)_payload+12+1)<<8|((uint32_t)*((uint8_t*)_payload+12+2))<<16|((uint32_t)*((uint8_t*)_payload+12+3))<<24))
#define DL_BOOZ2_FMS_COMMAND_h_sp_3(_payload) ((int32_t)(*((uint8_t*)_payload+16)|*((uint8_t*)_payload+16+1)<<8|((uint32_t)*((uint8_t*)_payload+16+2))<<16|((uint32_t)*((uint8_t*)_payload+16+3))<<24))
#define DL_BOOZ2_FMS_COMMAND_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+20)))

#define DL_SET_ACTUATOR_value(_payload) ((uint16_t)(*((uint8_t*)_payload+2)|*((uint8_t*)_payload+2+1)<<8))
#define DL_SET_ACTUATOR_no(_payload) ((uint8_t)(*((uint8_t*)_payload+4)))
#define DL_SET_ACTUATOR_ac_id(_payload) ((uint8_t)(*((uint8_t*)_payload+5)))

#define DL_CSC_SERVO_CMD_servo_1(_payload) ((uint16_t)(*((uint8_t*)_payload+2)|*((uint8_t*)_payload+2+1)<<8))
#define DL_CSC_SERVO_CMD_servo_2(_payload) ((uint16_t)(*((uint8_t*)_payload+4)|*((uint8_t*)_payload+4+1)<<8))
#define DL_CSC_SERVO_CMD_servo_3(_payload) ((uint16_t)(*((uint8_t*)_payload+6)|*((uint8_t*)_payload+6+1)<<8))
#define DL_CSC_SERVO_CMD_servo_4(_payload) ((uint16_t)(*((uint8_t*)_payload+8)|*((uint8_t*)_payload+8+1)<<8))
