	.file	"power.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	power_update
	.type	power_update, @function
power_update:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	lds r18,power_index
	mov r30,r18
	clr r31
	lsl r30
	rol r31
	subi r30,lo8(-(power_array))
	sbci r31,hi8(-(power_array))
	std Z+1,r25
	st Z,r24
	subi r18,lo8(-(1))
	andi r18,lo8(7)
	sts power_index,r18
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r30,lo8(power_array)
	ldi r31,hi8(power_array)
.L2:
	ld r24,Z+
	ld r25,Z+
	add r20,r24
	adc r21,r25
	ldi r24,hi8(power_array+16)
	cpi r30,lo8(power_array+16)
	cpc r31,r24
	brne .L2
	ldi r24,3
1:	lsr r21
	ror r20
	dec r24
	brne 1b
	ldi r22,lo8(13)
	ldi r24,lo8(12)
	call registers_write_word
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function power_update size 36 (35) */
	.size	power_update, .-power_update
.global	power_init
	.type	power_init, @function
power_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	sts power_index,__zero_reg__
	ldi r30,lo8(power_array)
	ldi r31,hi8(power_array)
.L8:
	st Z+,__zero_reg__
	st Z+,__zero_reg__
	ldi r24,hi8(power_array+16)
	cpi r30,lo8(power_array+16)
	cpc r31,r24
	brne .L8
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(13)
	ldi r24,lo8(12)
	call registers_write_word
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function power_init size 17 (16) */
	.size	power_init, .-power_init
	.lcomm power_index,1
	.lcomm power_array,16
/* File "power.c": code   53 = 0x0035 (  51), prologues   0, epilogues   2 */
