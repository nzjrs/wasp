	.file	"pid.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	pid_init
	.type	pid_init, @function
pid_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	sts (previous_seek)+1,__zero_reg__
	sts previous_seek,__zero_reg__
	sts (previous_position)+1,__zero_reg__
	sts previous_position,__zero_reg__
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function pid_init size 9 (8) */
	.size	pid_init, .-pid_init
.global	pid_registers_defaults
	.type	pid_registers_defaults, @function
pid_registers_defaults:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	sts registers+33,__zero_reg__
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(35)
	ldi r24,lo8(34)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(37)
	ldi r24,lo8(36)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(39)
	ldi r24,lo8(38)
	call registers_write_word
	ldi r20,lo8(96)
	ldi r21,hi8(96)
	ldi r22,lo8(43)
	ldi r24,lo8(42)
	call registers_write_word
	ldi r20,lo8(928)
	ldi r21,hi8(928)
	ldi r22,lo8(45)
	ldi r24,lo8(44)
	call registers_write_word
	sts registers+46,__zero_reg__
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function pid_registers_defaults size 35 (34) */
	.size	pid_registers_defaults, .-pid_registers_defaults
.global	pid_position_to_pwm
	.type	pid_position_to_pwm, @function
pid_position_to_pwm:
/* prologue: frame size=0 */
	push r16
	push r17
	push r28
	push r29
/* prologue end (size=4) */
	movw r28,r24
	lds r24,filter_reg
	lds r25,(filter_reg)+1
	lds r26,(filter_reg)+2
	lds r27,(filter_reg)+3
	movw r18,r24
	movw r20,r26
	asr r21
	ror r20
	ror r19
	ror r18
	sub r24,r18
	sbc r25,r19
	sbc r26,r20
	sbc r27,r21
	movw r18,r28
	clr r20
	sbrc r19,7
	com r20
	mov r21,r20
	add r24,r18
	adc r25,r19
	adc r26,r20
	adc r27,r21
	sts filter_reg,r24
	sts (filter_reg)+1,r25
	sts (filter_reg)+2,r26
	sts (filter_reg)+3,r27
	asr r27
	ror r26
	ror r25
	ror r24
	movw r18,r24
	sts (filtered_position.1378)+1,r25
	sts filtered_position.1378,r24
	lds r20,previous_position
	lds r21,(previous_position)+1
	sub r18,r20
	sbc r19,r21
	sts (current_velocity.1377)+1,r19
	sts current_velocity.1377,r18
	sts (previous_position)+1,r25
	sts previous_position,r24
	ldi r22,lo8(17)
	ldi r24,lo8(16)
	call registers_read_word
	sts (seek_position.1373)+1,r25
	sts seek_position.1373,r24
	ldi r22,lo8(19)
	ldi r24,lo8(18)
	call registers_read_word
	sts (seek_velocity.1374)+1,r25
	sts seek_velocity.1374,r24
	ldi r22,lo8(43)
	ldi r24,lo8(42)
	call registers_read_word
	sts (minimum_position.1375)+1,r25
	sts minimum_position.1375,r24
	ldi r22,lo8(45)
	ldi r24,lo8(44)
	call registers_read_word
	sts (maximum_position.1376)+1,r25
	sts maximum_position.1376,r24
	lds r24,registers+46
	tst r24
	breq .L6
	ldi r16,lo8(1023)
	ldi r17,hi8(1023)
	movw r20,r16
	sub r20,r28
	sbc r21,r29
	ldi r22,lo8(9)
	ldi r24,lo8(8)
	call registers_write_word
	lds r20,current_velocity.1377
	lds r21,(current_velocity.1377)+1
	com r21
	neg r20
	sbci r21,lo8(-1)
	ldi r22,lo8(11)
	ldi r24,lo8(10)
	call registers_write_word
	lds r24,seek_position.1373
	lds r25,(seek_position.1373)+1
	movw r18,r16
	sub r18,r24
	sbc r19,r25
	sts (seek_position.1373)+1,r19
	sts seek_position.1373,r18
	lds r24,minimum_position.1375
	lds r25,(minimum_position.1375)+1
	movw r18,r16
	sub r18,r24
	sbc r19,r25
	sts (minimum_position.1375)+1,r19
	sts minimum_position.1375,r18
	lds r24,maximum_position.1376
	lds r25,(maximum_position.1376)+1
	sub r16,r24
	sbc r17,r25
	sts (maximum_position.1376)+1,r17
	sts maximum_position.1376,r16
	rjmp .L8
.L6:
	movw r20,r28
	ldi r22,lo8(9)
	ldi r24,lo8(8)
	call registers_write_word
	lds r20,current_velocity.1377
	lds r21,(current_velocity.1377)+1
	ldi r22,lo8(11)
	ldi r24,lo8(10)
	call registers_write_word
.L8:
	lds r24,registers+33
	clr r25
	sts (deadband.1370)+1,r25
	sts deadband.1370,r24
	lds r18,seek_position.1373
	lds r19,(seek_position.1373)+1
	lds r24,previous_seek
	lds r25,(previous_seek)+1
	cp r18,r24
	cpc r19,r25
	brne .L9
	lds r28,filtered_position.1378
	lds r29,(filtered_position.1378)+1
.L9:
	sts (previous_seek)+1,r19
	sts previous_seek,r18
	lds r24,minimum_position.1375
	lds r25,(minimum_position.1375)+1
	cp r18,r24
	cpc r19,r25
	brge .L11
	sts (seek_position.1373)+1,r25
	sts seek_position.1373,r24
.L11:
	lds r18,maximum_position.1376
	lds r19,(maximum_position.1376)+1
	lds r24,seek_position.1373
	lds r25,(seek_position.1373)+1
	cp r18,r24
	cpc r19,r25
	brge .L13
	sts (seek_position.1373)+1,r19
	sts seek_position.1373,r18
.L13:
	lds r24,seek_position.1373
	lds r25,(seek_position.1373)+1
	sub r24,r28
	sbc r25,r29
	sts (p_component.1371)+1,r25
	sts p_component.1371,r24
	lds r24,seek_velocity.1374
	lds r25,(seek_velocity.1374)+1
	lds r18,current_velocity.1377
	lds r19,(current_velocity.1377)+1
	sub r24,r18
	sbc r25,r19
	sts (d_component.1372)+1,r25
	sts d_component.1372,r24
	ldi r22,lo8(35)
	ldi r24,lo8(34)
	call registers_read_word
	sts (p_gain.1381)+1,r25
	sts p_gain.1381,r24
	ldi r22,lo8(37)
	ldi r24,lo8(36)
	call registers_read_word
	movw r28,r24
	sts (d_gain.1380)+1,r25
	sts d_gain.1380,r24
	sts pwm_output.1379,__zero_reg__
	sts (pwm_output.1379)+1,__zero_reg__
	sts (pwm_output.1379)+2,__zero_reg__
	sts (pwm_output.1379)+3,__zero_reg__
	lds r22,p_component.1371
	lds r23,(p_component.1371)+1
	lds r24,deadband.1370
	lds r25,(deadband.1370)+1
	cp r24,r22
	cpc r25,r23
	brlt .L15
	com r25
	neg r24
	sbci r25,lo8(-1)
	cp r22,r24
	cpc r23,r25
	brge .L17
.L15:
	clr r24
	sbrc r23,7
	com r24
	mov r25,r24
	lds r18,p_gain.1381
	lds r19,(p_gain.1381)+1
	clr r20
	clr r21
	call __mulsi3
	sts pwm_output.1379,r22
	sts (pwm_output.1379)+1,r23
	sts (pwm_output.1379)+2,r24
	sts (pwm_output.1379)+3,r25
.L17:
	lds r22,d_component.1372
	lds r23,(d_component.1372)+1
	clr r24
	sbrc r23,7
	com r24
	mov r25,r24
	movw r18,r28
	clr r20
	clr r21
	call __mulsi3
	lds r18,pwm_output.1379
	lds r19,(pwm_output.1379)+1
	lds r20,(pwm_output.1379)+2
	lds r21,(pwm_output.1379)+3
	add r18,r22
	adc r19,r23
	adc r20,r24
	adc r21,r25
	mov r18,r19
	mov r19,r20
	mov r20,r21
	clr r21
	sbrc r20,7
	dec r21
	sts pwm_output.1379,r18
	sts (pwm_output.1379)+1,r19
	sts (pwm_output.1379)+2,r20
	sts (pwm_output.1379)+3,r21
	cpi r18,lo8(255)
	cpc r19,__zero_reg__
	cpc r20,__zero_reg__
	cpc r21,__zero_reg__
	breq .L18
	brlt .L18
	ldi r24,lo8(255)
	ldi r25,hi8(255)
	ldi r26,hlo8(255)
	ldi r27,hhi8(255)
	rjmp .L23
.L18:
	subi r18,lo8(-255)
	sbci r19,hi8(-255)
	sbci r20,hlo8(-255)
	sbci r21,hhi8(-255)
	brge .L20
	ldi r24,lo8(-255)
	ldi r25,hi8(-255)
	ldi r26,hlo8(-255)
	ldi r27,hhi8(-255)
.L23:
	sts pwm_output.1379,r24
	sts (pwm_output.1379)+1,r25
	sts (pwm_output.1379)+2,r26
	sts (pwm_output.1379)+3,r27
.L20:
	lds r24,pwm_output.1379
	lds r25,(pwm_output.1379)+1
/* epilogue: frame size=0 */
	pop r29
	pop r28
	pop r17
	pop r16
	ret
/* epilogue end (size=5) */
/* function pid_position_to_pwm size 382 (373) */
	.size	pid_position_to_pwm, .-pid_position_to_pwm
	.lcomm p_gain.1381,2
	.lcomm d_gain.1380,2
	.lcomm pwm_output.1379,4
	.lcomm filtered_position.1378,2
	.lcomm current_velocity.1377,2
	.lcomm maximum_position.1376,2
	.lcomm minimum_position.1375,2
	.lcomm seek_velocity.1374,2
	.lcomm seek_position.1373,2
	.lcomm d_component.1372,2
	.lcomm p_component.1371,2
	.lcomm deadband.1370,2
	.lcomm filter_reg,4
	.lcomm previous_seek,2
	.lcomm previous_position,2
/* File "pid.c": code  426 = 0x01aa ( 415), prologues   4, epilogues   7 */
