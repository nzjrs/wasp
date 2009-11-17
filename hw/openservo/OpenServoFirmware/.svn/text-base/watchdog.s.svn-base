	.file	"watchdog.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	watchdog_init
	.type	watchdog_init, @function
watchdog_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	in r24,84-0x20
	andi r24,lo8(-9)
	out 84-0x20,r24
	ldi r30,lo8(96)
	ldi r31,hi8(96)
	ld r24,Z
	ori r24,lo8(24)
	st Z,r24
	st Z,__zero_reg__
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function watchdog_init size 10 (9) */
	.size	watchdog_init, .-watchdog_init
.global	watchdog_hard_reset
	.type	watchdog_hard_reset, @function
watchdog_hard_reset:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	lds r24,registers+5
	andi r24,lo8(-2)
	sts registers+5,r24
	call pwm_stop
	ldi r24,lo8(-120)
	sts 96,r24
.L4:
	rjmp .L4
/* epilogue: frame size=0 */
/* epilogue: noreturn */
/* epilogue end (size=0) */
/* function watchdog_hard_reset size 11 (11) */
	.size	watchdog_hard_reset, .-watchdog_hard_reset
/* File "watchdog.c": code   21 = 0x0015 (  20), prologues   0, epilogues   1 */
