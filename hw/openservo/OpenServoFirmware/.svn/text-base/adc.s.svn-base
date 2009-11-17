	.file	"adc.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	adc_init
	.type	adc_init, @function
adc_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	ldi r24,lo8(1)
	sts adc_channel,r24
	sts adc_power_ready,__zero_reg__
	sts (adc_power_value)+1,__zero_reg__
	sts adc_power_value,__zero_reg__
	sts adc_position_ready,__zero_reg__
	sts (adc_position_value)+1,__zero_reg__
	sts adc_position_value,__zero_reg__
	sts adc_voltage_needed,r24
	in r24,40-0x20
	andi r24,lo8(-8)
	out 40-0x20,r24
	ldi r30,lo8(126)
	ldi r31,hi8(126)
	ld r24,Z
	ori r24,lo8(7)
	st Z,r24
	ldi r24,lo8(66)
	sts 124,r24
	ldi r24,lo8(3)
	sts 123,r24
	ldi r24,lo8(-82)
	sts 122,r24
	ldi r25,lo8(2)
	out 68-0x20,r25
	ldi r24,lo8(5)
	out 69-0x20,r24
	sts 110,r25
	ldi r24,lo8(78)
	out 71-0x20,r24
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function adc_init size 43 (42) */
	.size	adc_init, .-adc_init
.global	__vector_21
	.type	__vector_21, @function
__vector_21:
/* prologue: frame size=0 */
	push __zero_reg__
	push __tmp_reg__
	in __tmp_reg__,__SREG__
	push __tmp_reg__
	clr __zero_reg__
	push r18
	push r19
	push r20
	push r21
	push r22
	push r23
	push r24
	push r25
	push r26
	push r27
	push r30
	push r31
/* prologue end (size=17) */
	lds r20,120
	lds r21,(120)+1
	lds r24,adc_channel
	cpi r24,lo8(1)
	breq .L6
	cpi r24,lo8(1)
	brlo .L5
	cpi r24,lo8(2)
	brne .L10
	rjmp .L7
.L6:
	sts (adc_position_value)+1,r21
	sts adc_position_value,r20
	sts adc_position_ready,r24
	sts adc_channel,__zero_reg__
	ldi r24,lo8(64)
	rjmp .L11
.L5:
	sts (adc_power_value)+1,r21
	sts adc_power_value,r20
	ldi r25,lo8(1)
	sts adc_power_ready,r25
	lds r24,adc_voltage_needed
	tst r24
	breq .L8
	ldi r24,lo8(2)
	sts adc_channel,r24
	ldi r24,lo8(65)
.L11:
	sts 124,r24
	lds r24,122
	ori r24,lo8(64)
	sts 122,r24
	rjmp .L10
.L8:
	sts adc_channel,r25
	rjmp .L12
.L7:
	sts adc_voltage_needed,__zero_reg__
	ldi r22,lo8(21)
	ldi r24,lo8(20)
	call registers_write_word
	ldi r24,lo8(1)
	sts adc_channel,r24
.L12:
	ldi r24,lo8(66)
	sts 124,r24
.L10:
/* epilogue: frame size=0 */
	pop r31
	pop r30
	pop r27
	pop r26
	pop r25
	pop r24
	pop r23
	pop r22
	pop r21
	pop r20
	pop r19
	pop r18
	pop __tmp_reg__
	out __SREG__,__tmp_reg__
	pop __tmp_reg__
	pop __zero_reg__
	reti
/* epilogue end (size=17) */
/* function __vector_21 size 95 (61) */
	.size	__vector_21, .-__vector_21
.global	__vector_14
	.type	__vector_14, @function
__vector_14:
/* prologue: frame size=0 */
	push __zero_reg__
	push __tmp_reg__
	in __tmp_reg__,__SREG__
	push __tmp_reg__
	clr __zero_reg__
	push r18
	push r19
	push r20
	push r21
	push r22
	push r23
	push r24
	push r25
	push r26
	push r27
	push r30
	push r31
/* prologue end (size=17) */
	lds r24,adc_channel
	cpi r24,lo8(1)
	brne .L16
	ldi r22,lo8(7)
	ldi r24,lo8(6)
	call registers_read_word
	adiw r24,1
	movw r20,r24
	ldi r22,lo8(7)
	ldi r24,lo8(6)
	call registers_write_word
.L16:
/* epilogue: frame size=0 */
	pop r31
	pop r30
	pop r27
	pop r26
	pop r25
	pop r24
	pop r23
	pop r22
	pop r21
	pop r20
	pop r19
	pop r18
	pop __tmp_reg__
	out __SREG__,__tmp_reg__
	pop __tmp_reg__
	pop __zero_reg__
	reti
/* epilogue end (size=17) */
/* function __vector_14 size 48 (14) */
	.size	__vector_14, .-__vector_14
	.comm adc_power_ready,1,1
	.comm adc_power_value,2,1
	.comm adc_position_ready,1,1
	.comm adc_position_value,2,1
	.comm adc_voltage_needed,1,1
	.comm adc_channel,1,1
/* File "adc.c": code  186 = 0x00ba ( 117), prologues  34, epilogues  35 */
