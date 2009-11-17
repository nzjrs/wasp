	.file	"registers.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	registers_read_word
	.type	registers_read_word, @function
registers_read_word:
/* prologue: frame size=0 */
/* prologue end (size=0) */
/* #APP */
	in r25,__SREG__
	cli
	
	out __SREG__,r25
	
/* #NOAPP */
	ldi r26,lo8(registers)
	ldi r27,hi8(registers)
	movw r30,r26
	add r30,r24
	adc r31,__zero_reg__
	ld r24,Z
	clr r25
	mov r25,r24
	clr r24
	add r26,r22
	adc r27,__zero_reg__
	ld r18,X
	clr r19
	or r24,r18
	or r25,r19
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function registers_read_word size 26 (25) */
	.size	registers_read_word, .-registers_read_word
.global	registers_write_word
	.type	registers_write_word, @function
registers_write_word:
/* prologue: frame size=0 */
/* prologue end (size=0) */
/* #APP */
	in r18,__SREG__
	cli
	
/* #NOAPP */
	ldi r30,lo8(registers)
	ldi r31,hi8(registers)
	movw r26,r30
	add r26,r24
	adc r27,__zero_reg__
	mov r24,r21
	clr r25
	st X,r24
	add r30,r22
	adc r31,__zero_reg__
	st Z,r20
/* #APP */
	out __SREG__,r18
	
/* #NOAPP */
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function registers_write_word size 22 (21) */
	.size	registers_write_word, .-registers_write_word
.global	registers_defaults
	.type	registers_defaults, @function
registers_defaults:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	ldi r24,lo8(16)
	sts registers+32,r24
	call pwm_registers_defaults
	call pid_registers_defaults
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function registers_defaults size 8 (7) */
	.size	registers_defaults, .-registers_defaults
.global	registers_init
	.type	registers_init, @function
registers_init:
/* prologue: frame size=0 */
	push r28
	push r29
/* prologue end (size=2) */
	ldi r28,lo8(registers)
	ldi r29,hi8(registers)
	ldi r24,lo8(72)
	movw r30,r28
	st Z+,__zero_reg__
        dec r24
	brne .-6
	ldi r24,lo8(1)
	sts registers,r24
	sts registers+1,r24
	sts registers+2,__zero_reg__
	ldi r24,lo8(2)
	sts registers+3,r24
	call eeprom_restore_registers
	tst r24
	brne .L10
	ldi r20,lo8(72)
	ldi r21,hi8(72)
	ldi r22,lo8(40)
	ldi r23,hi8(40)
	movw r24,r28
	adiw r24,32
	call memset
	call registers_defaults
.L10:
/* epilogue: frame size=0 */
	pop r29
	pop r28
	ret
/* epilogue end (size=3) */
/* function registers_init size 36 (31) */
	.size	registers_init, .-registers_init
	.comm registers,72,1
/* File "registers.c": code   92 = 0x005c (  84), prologues   2, epilogues   6 */
