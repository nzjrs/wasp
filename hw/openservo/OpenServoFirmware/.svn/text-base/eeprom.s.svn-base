	.file	"eeprom.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
	.type	eeprom_checksum, @function
eeprom_checksum:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	movw r30,r24
	rjmp .L2
.L3:
	ld r24,Z+
	add r20,r24
	subi r22,lo8(-(-1))
	sbci r23,hi8(-(-1))
.L2:
	cp r22,__zero_reg__
	cpc r23,__zero_reg__
	brne .L3
	mov r24,r20
	clr r25
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function eeprom_checksum size 12 (11) */
	.size	eeprom_checksum, .-eeprom_checksum
.global	eeprom_erase
	.type	eeprom_erase, @function
eeprom_erase:
/* prologue: frame size=16 */
	push r16
	push r17
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
	sbiw r28,16
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
/* prologue end (size=12) */
	ldi r20,lo8(16)
	ldi r21,hi8(16)
	ldi r22,lo8(255)
	ldi r23,hi8(255)
	movw r16,r28
	subi r16,lo8(-(1))
	sbci r17,hi8(-(1))
	movw r24,r16
	call memset
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	ldi r20,lo8(16)
	movw r18,r16
.L7:
	movw r26,r24
	movw r30,r18
/* #APP */
	mov __zero_reg__,r20
	call __eeprom_write_block_1F2021
/* #NOAPP */
	adiw r24,16
	ldi r31,hi8(512)
	cpi r24,lo8(512)
	cpc r25,r31
	brne .L7
	ldi r24,lo8(1)
	ldi r25,hi8(1)
/* epilogue: frame size=16 */
	adiw r28,16
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
	pop r29
	pop r28
	pop r17
	pop r16
	ret
/* epilogue end (size=11) */
/* function eeprom_erase size 50 (27) */
	.size	eeprom_erase, .-eeprom_erase
.global	eeprom_save_registers
	.type	eeprom_save_registers, @function
eeprom_save_registers:
/* prologue: frame size=2 */
	push r16
	push r17
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
	sbiw r28,2
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
/* prologue end (size=12) */
	ldi r24,lo8(3)
	std Y+1,r24
	ldi r16,lo8(registers+32)
	ldi r17,hi8(registers+32)
	ldi r20,lo8(3)
	ldi r22,lo8(40)
	ldi r23,hi8(40)
	movw r24,r16
	call eeprom_checksum
	std Y+2,r24
	ldi r24,lo8(2)
	ldi r26,lo8(0)
	ldi r27,hi8(0)
	movw r30,r28
	adiw r30,1
/* #APP */
	mov __zero_reg__,r24
	call __eeprom_write_block_1F2021
/* #NOAPP */
	ldi r24,lo8(40)
	ldi r26,lo8(2)
	ldi r27,hi8(2)
	movw r30,r16
/* #APP */
	mov __zero_reg__,r24
	call __eeprom_write_block_1F2021
/* #NOAPP */
	ldi r24,lo8(1)
	ldi r25,hi8(1)
/* epilogue: frame size=2 */
	adiw r28,2
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
	pop r29
	pop r28
	pop r17
	pop r16
	ret
/* epilogue end (size=11) */
/* function eeprom_save_registers size 53 (30) */
	.size	eeprom_save_registers, .-eeprom_save_registers
.global	eeprom_restore_registers
	.type	eeprom_restore_registers, @function
eeprom_restore_registers:
/* prologue: frame size=2 */
	push r17
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
	sbiw r28,2
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
/* prologue end (size=11) */
	ldi r24,lo8(2)
	ldi r26,lo8(0)
	ldi r27,hi8(0)
	movw r30,r28
	adiw r30,1
/* #APP */
	mov __zero_reg__,r24
	call __eeprom_read_block_1F2021
/* #NOAPP */
	ldd r24,Y+1
	cpi r24,lo8(3)
	breq .L15
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	rjmp .L17
.L15:
	ldi r24,lo8(40)
	ldi r18,lo8(registers+32)
	ldi r19,hi8(registers+32)
	ldi r26,lo8(2)
	ldi r27,hi8(2)
	movw r30,r18
/* #APP */
	mov __zero_reg__,r24
	call __eeprom_read_block_1F2021
/* #NOAPP */
	ldd r17,Y+2
	ldi r20,lo8(3)
	ldi r22,lo8(40)
	ldi r23,hi8(40)
	movw r24,r18
	call eeprom_checksum
	ldi r25,lo8(0)
	cpse r17,r24
	ldi r25,lo8(1)
.L18:
	ldi r24,lo8(1)
	eor r25,r24
	mov r24,r25
	clr r25
.L17:
/* epilogue: frame size=2 */
	adiw r28,2
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
	pop r29
	pop r28
	pop r17
	ret
/* epilogue end (size=10) */
/* function eeprom_restore_registers size 61 (40) */
	.size	eeprom_restore_registers, .-eeprom_restore_registers
/* File "eeprom.c": code  176 = 0x00b0 ( 108), prologues  35, epilogues  33 */
