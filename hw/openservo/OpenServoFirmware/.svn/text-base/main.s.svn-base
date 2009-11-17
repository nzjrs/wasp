	.file	"main.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	main
	.type	main, @function
main:
/* prologue: frame size=0 */
	push r16
	push r17
/* prologue end (size=2) */
	ldi r24,lo8(6)
	out 36-0x20,r24
	ldi r24,lo8(-7)
	out 37-0x20,r24
	out 39-0x20,__zero_reg__
	ldi r24,lo8(127)
	out 40-0x20,r24
	out 42-0x20,__zero_reg__
	ldi r24,lo8(-1)
	out 43-0x20,r24
	call watchdog_init
	call registers_init
	call pwm_init
	call adc_init
	call pid_init
	call motion_init
	call power_init
	lds r24,registers+32
	call twi_slave_init
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(7)
	ldi r24,lo8(6)
	call registers_write_word
/* #APP */
	sei
/* #NOAPP */
.L2:
	lds r24,adc_position_ready
	tst r24
	breq .L2
	sts adc_position_ready,__zero_reg__
	lds r24,adc_position_value
	lds r25,(adc_position_value)+1
	call motion_reset
	sts adc_position_ready,__zero_reg__
	lds r20,adc_position_value
	lds r21,(adc_position_value)+1
	ldi r22,lo8(17)
	ldi r24,lo8(16)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(19)
	ldi r24,lo8(18)
	call registers_write_word
	lds r24,registers+5
	ori r24,lo8(3)
.L38:
	sts registers+5,r24
.L39:
	lds r24,adc_position_ready
	tst r24
	breq .L5
	ldi r24,lo8(10)
	ldi r25,hi8(10)
	call motion_next
	sts adc_position_ready,__zero_reg__
	lds r16,adc_position_value
	lds r17,(adc_position_value)+1
	movw r24,r16
	call pid_position_to_pwm
	movw r22,r24
	movw r24,r16
	call pwm_update
.L5:
	lds r24,adc_power_ready
	tst r24
	breq .L7
	sts adc_power_ready,__zero_reg__
	lds r24,adc_power_value
	lds r25,(adc_power_value)+1
	call power_update
.L7:
	call twi_data_in_receive_buffer
	tst r24
	breq .L39
	call twi_receive_byte
	cpi r24,lo8(-121)
	breq .L16
	cpi r24,lo8(-120)
	brsh .L24
	cpi r24,lo8(-125)
	breq .L12
	cpi r24,lo8(-124)
	brsh .L25
	cpi r24,lo8(-128)
	breq .L10
	cpi r24,lo8(-126)
	brne .L39
	rjmp .L11
.L25:
	cpi r24,lo8(-123)
	breq .L14
	cpi r24,lo8(-122)
	brsh .L15
	rjmp .L35
.L24:
	cpi r24,lo8(-111)
	breq .L20
	cpi r24,lo8(-110)
	brsh .L26
	cpi r24,lo8(-119)
	breq .L18
	cpi r24,lo8(-119)
	brlo .L17
	cpi r24,lo8(-112)
	breq .+2
	rjmp .L39
	rjmp .L19
.L26:
	cpi r24,lo8(-109)
	breq .L22
	cpi r24,lo8(-109)
	brlo .L21
	cpi r24,lo8(-108)
	breq .+2
	rjmp .L39
	rjmp .L23
.L10:
	call watchdog_hard_reset
	rjmp .L39
.L11:
	lds r24,registers+5
	ori r24,lo8(1)
	rjmp .L38
.L12:
	lds r24,registers+5
	andi r24,lo8(-2)
	sts registers+5,r24
	call pwm_stop
	rjmp .L39
.L35:
	lds r24,registers+5
	ori r24,lo8(2)
	rjmp .L38
.L14:
	lds r24,registers+5
	andi r24,lo8(-3)
	rjmp .L38
.L15:
	call eeprom_save_registers
	rjmp .L39
.L16:
	call eeprom_restore_registers
	rjmp .L39
.L17:
	call registers_defaults
	rjmp .L39
.L18:
	call eeprom_erase
	rjmp .L39
.L19:
	ldi r24,lo8(1)
	sts adc_voltage_needed,r24
	rjmp .L39
.L20:
	lds r24,registers+5
	ori r24,lo8(4)
	rjmp .L38
.L21:
	lds r24,registers+5
	andi r24,lo8(-5)
	rjmp .L38
.L22:
	sts adc_position_ready,__zero_reg__
	lds r24,adc_position_value
	lds r25,(adc_position_value)+1
	call motion_reset
	rjmp .L39
.L23:
	call motion_append
	rjmp .L39
/* epilogue: frame size=0 */
/* epilogue: noreturn */
/* epilogue end (size=0) */
/* function main size 207 (205) */
	.size	main, .-main
/* File "main.c": code  207 = 0x00cf ( 205), prologues   2, epilogues   0 */
