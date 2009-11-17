	.file	"motion.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	motion_buffer_left
	.type	motion_buffer_left, @function
motion_buffer_left:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	lds r25,motion_head
	lds r24,motion_tail
	cp r25,r24
	brsh .L2
	sub r24,r25
	subi r24,lo8(-(-1))
	rjmp .L4
.L2:
	sub r25,r24
	ldi r24,lo8(7)
	sub r24,r25
.L4:
	clr r25
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function motion_buffer_left size 14 (13) */
	.size	motion_buffer_left, .-motion_buffer_left
.global	motion_registers_reset
	.type	motion_registers_reset, @function
motion_registers_reset:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(27)
	ldi r24,lo8(26)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(29)
	ldi r24,lo8(28)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(31)
	ldi r24,lo8(30)
	call registers_write_word
	ldi r20,lo8(0)
	ldi r21,hi8(0)
	ldi r22,lo8(25)
	ldi r24,lo8(24)
	call registers_write_word
	sts registers+22,__zero_reg__
	call motion_buffer_left
	sts registers+23,r24
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function motion_registers_reset size 31 (30) */
	.size	motion_registers_reset, .-motion_registers_reset
.global	motion_reset
	.type	motion_reset, @function
motion_reset:
/* prologue: frame size=0 */
	push r10
	push r11
	push r12
	push r13
	push r14
	push r15
	push r16
	push r17
/* prologue end (size=8) */
	sts motion_counter,__zero_reg__
	sts (motion_counter)+1,__zero_reg__
	sts (motion_counter)+2,__zero_reg__
	sts (motion_counter)+3,__zero_reg__
	sts motion_duration,__zero_reg__
	sts (motion_duration)+1,__zero_reg__
	sts (motion_duration)+2,__zero_reg__
	sts (motion_duration)+3,__zero_reg__
	sts motion_head,__zero_reg__
	sts motion_tail,__zero_reg__
	sts (keys)+1,__zero_reg__
	sts keys,__zero_reg__
	clr r26
	sbrc r25,7
	com r26
	mov r27,r26
	movw r22,r24
	movw r24,r26
	call __floatsisf
	movw r18,r22
	movw r20,r24
	sts keys+2,r22
	sts (keys+2)+1,r23
	sts (keys+2)+2,r24
	sts (keys+2)+3,r25
	ldi r24,lo8(0x0)
	ldi r25,hi8(0x0)
	ldi r26,hlo8(0x0)
	ldi r27,hhi8(0x0)
	sts keys+6,r24
	sts (keys+6)+1,r25
	sts (keys+6)+2,r26
	sts (keys+6)+3,r27
	sts keys+10,r24
	sts (keys+10)+1,r25
	sts (keys+10)+2,r26
	sts (keys+10)+3,r27
	push r27
	push r26
	push r25
	push r24
	movw r10,r24
	movw r12,r26
	movw r14,r18
	movw r16,r20
	ldi r22,lo8(0)
	ldi r23,hi8(0)
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	call curve_init
	call motion_registers_reset
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
/* epilogue: frame size=0 */
	pop r17
	pop r16
	pop r15
	pop r14
	pop r13
	pop r12
	pop r11
	pop r10
	ret
/* epilogue end (size=9) */
/* function motion_reset size 99 (82) */
	.size	motion_reset, .-motion_reset
.global	motion_init
	.type	motion_init, @function
motion_init:
/* prologue: frame size=0 */
	push r10
	push r11
	push r12
	push r13
	push r14
	push r15
	push r16
	push r17
/* prologue end (size=8) */
	sts motion_counter,__zero_reg__
	sts (motion_counter)+1,__zero_reg__
	sts (motion_counter)+2,__zero_reg__
	sts (motion_counter)+3,__zero_reg__
	sts motion_duration,__zero_reg__
	sts (motion_duration)+1,__zero_reg__
	sts (motion_duration)+2,__zero_reg__
	sts (motion_duration)+3,__zero_reg__
	sts motion_head,__zero_reg__
	sts motion_tail,__zero_reg__
	sts (keys)+1,__zero_reg__
	sts keys,__zero_reg__
	ldi r24,lo8(0x44000000)
	ldi r25,hi8(0x44000000)
	ldi r26,hlo8(0x44000000)
	ldi r27,hhi8(0x44000000)
	sts keys+2,r24
	sts (keys+2)+1,r25
	sts (keys+2)+2,r26
	sts (keys+2)+3,r27
	ldi r24,lo8(0x0)
	ldi r25,hi8(0x0)
	ldi r26,hlo8(0x0)
	ldi r27,hhi8(0x0)
	sts keys+6,r24
	sts (keys+6)+1,r25
	sts (keys+6)+2,r26
	sts (keys+6)+3,r27
	sts keys+10,r24
	sts (keys+10)+1,r25
	sts (keys+10)+2,r26
	sts (keys+10)+3,r27
	push r27
	push r26
	push r25
	push r24
	movw r10,r24
	movw r12,r26
	mov __tmp_reg__,r31
	ldi r31,lo8(0x44000000)
	mov r14,r31
	ldi r31,hi8(0x44000000)
	mov r15,r31
	ldi r31,hlo8(0x44000000)
	mov r16,r31
	ldi r31,hhi8(0x44000000)
	mov r17,r31
	mov r31,__tmp_reg__
	movw r20,r16
	movw r18,r14
	ldi r22,lo8(0)
	ldi r23,hi8(0)
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	call curve_init
	call motion_registers_reset
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
/* epilogue: frame size=0 */
	pop r17
	pop r16
	pop r15
	pop r14
	pop r13
	pop r12
	pop r11
	pop r10
	ret
/* epilogue end (size=9) */
/* function motion_init size 103 (86) */
	.size	motion_init, .-motion_init
.global	motion_next
	.type	motion_next, @function
motion_next:
/* prologue: frame size=8 */
	push r10
	push r11
	push r12
	push r13
	push r14
	push r15
	push r16
	push r17
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
	sbiw r28,8
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
/* prologue end (size=18) */
	movw r18,r24
	lds r24,registers+5
	sbrs r24,2
	rjmp .L23
	lds r25,motion_tail
	lds r24,motion_head
	cp r25,r24
	brne .L15
	sts motion_counter,__zero_reg__
	sts (motion_counter)+1,__zero_reg__
	sts (motion_counter)+2,__zero_reg__
	sts (motion_counter)+3,__zero_reg__
	sts motion_duration,__zero_reg__
	sts (motion_duration)+1,__zero_reg__
	sts (motion_duration)+2,__zero_reg__
	sts (motion_duration)+3,__zero_reg__
	rjmp .L17
.L15:
	clr r20
	clr r21
	lds r24,motion_counter
	lds r25,(motion_counter)+1
	lds r26,(motion_counter)+2
	lds r27,(motion_counter)+3
	add r24,r18
	adc r25,r19
	adc r26,r20
	adc r27,r21
	sts motion_counter,r24
	sts (motion_counter)+1,r25
	sts (motion_counter)+2,r26
	sts (motion_counter)+3,r27
	rjmp .L18
.L19:
	sub r18,r14
	sbc r19,r15
	sbc r20,r16
	sbc r21,r17
	sts motion_counter,r18
	sts (motion_counter)+1,r19
	sts (motion_counter)+2,r20
	sts (motion_counter)+3,r21
	lds r24,motion_duration
	lds r25,(motion_duration)+1
	lds r26,(motion_duration)+2
	lds r27,(motion_duration)+3
	sub r24,r14
	sbc r25,r15
	sbc r26,r16
	sbc r27,r17
	sts motion_duration,r24
	sts (motion_duration)+1,r25
	sts (motion_duration)+2,r26
	sts (motion_duration)+3,r27
	lds r18,motion_tail
	subi r18,lo8(-(1))
	andi r18,lo8(7)
	sts motion_tail,r18
	lds r24,motion_head
	mov r20,r18
	clr r21
	cp r18,r24
	brne .L20
	movw r24,r20
	lsl r24
	rol r25
	movw r30,r24
	ldi r26,3
1:	lsl r30
	rol r31
	dec r26
	brne 1b
	sub r30,r24
	sbc r31,r25
	subi r30,lo8(-(keys))
	sbci r31,hi8(-(keys))
	ldd r18,Z+2
	ldd r19,Z+3
	ldd r20,Z+4
	ldd r21,Z+5
	ldi r24,lo8(0x0)
	ldi r25,hi8(0x0)
	ldi r26,hlo8(0x0)
	ldi r27,hhi8(0x0)
	push r27
	push r26
	push r25
	push r24
	movw r10,r24
	movw r12,r26
	movw r14,r18
	movw r16,r20
	ldi r22,lo8(0)
	ldi r23,hi8(0)
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	call curve_init
	sts motion_counter,__zero_reg__
	sts (motion_counter)+1,__zero_reg__
	sts (motion_counter)+2,__zero_reg__
	sts (motion_counter)+3,__zero_reg__
	sts motion_duration,__zero_reg__
	sts (motion_duration)+1,__zero_reg__
	sts (motion_duration)+2,__zero_reg__
	sts (motion_duration)+3,__zero_reg__
	rjmp .L24
.L20:
	subi r18,lo8(-(1))
	andi r18,lo8(7)
	clr r19
	movw r24,r20
	lsl r24
	rol r25
	movw r26,r24
	ldi r22,3
1:	lsl r26
	rol r27
	dec r22
	brne 1b
	sub r26,r24
	sbc r27,r25
	subi r26,lo8(-(keys))
	sbci r27,hi8(-(keys))
	movw r30,r26
	ldd r10,Z+10
	ldd r11,Z+11
	ldd r12,Z+12
	ldd r13,Z+13
	lsl r18
	rol r19
	movw r24,r18
	ldi r20,3
1:	lsl r24
	rol r25
	dec r20
	brne 1b
	sub r24,r18
	sbc r25,r19
	subi r24,lo8(-(keys))
	sbci r25,hi8(-(keys))
	movw r30,r24
	ldd r14,Z+2
	ldd r15,Z+3
	ldd r16,Z+4
	ldd r17,Z+5
	movw r30,r26
	ldd r18,Z+2
	ldd r19,Z+3
	ldd r20,Z+4
	ldd r21,Z+5
	movw r30,r24
	ld r22,Z
	ldd r23,Z+1
	ldd r24,Z+6
	ldd r25,Z+7
	ldd r26,Z+8
	ldd r27,Z+9
	push r27
	push r26
	push r25
	push r24
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	call curve_init
.L24:
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
	call motion_buffer_left
	sts registers+23,r24
.L18:
	lds r18,motion_counter
	lds r19,(motion_counter)+1
	lds r20,(motion_counter)+2
	lds r21,(motion_counter)+3
	lds r24,curve_duration
	lds r25,(curve_duration)+1
	movw r14,r24
	clr r16
	clr r17
	cp r14,r18
	cpc r15,r19
	cpc r16,r20
	cpc r17,r21
	brsh .+2
	rjmp .L19
.L17:
	movw r20,r28
	subi r20,lo8(-(1))
	sbci r21,hi8(-(1))
	movw r22,r28
	subi r22,lo8(-(5))
	sbci r23,hi8(-(5))
	lds r24,motion_counter
	lds r25,(motion_counter)+1
	call curve_solve
	ldi r18,lo8(0x41200000)
	ldi r19,hi8(0x41200000)
	ldi r20,hlo8(0x41200000)
	ldi r21,hhi8(0x41200000)
	ldd r22,Y+1
	ldd r23,Y+2
	ldd r24,Y+3
	ldd r25,Y+4
	call __mulsf3
	std Y+1,r22
	std Y+2,r23
	std Y+3,r24
	std Y+4,r25
	ldi r18,lo8(0x3f000000)
	ldi r19,hi8(0x3f000000)
	ldi r20,hlo8(0x3f000000)
	ldi r21,hhi8(0x3f000000)
	ldd r22,Y+5
	ldd r23,Y+6
	ldd r24,Y+7
	ldd r25,Y+8
	call __addsf3
	call __fixsfsi
	movw r20,r22
	movw r22,r24
	ldi r22,lo8(17)
	ldi r24,lo8(16)
	call registers_write_word
	ldi r18,lo8(0x3f000000)
	ldi r19,hi8(0x3f000000)
	ldi r20,hlo8(0x3f000000)
	ldi r21,hhi8(0x3f000000)
	ldd r22,Y+1
	ldd r23,Y+2
	ldd r24,Y+3
	ldd r25,Y+4
	call __addsf3
	call __fixsfsi
	movw r20,r22
	movw r22,r24
	ldi r22,lo8(19)
	ldi r24,lo8(18)
	call registers_write_word
.L23:
/* epilogue: frame size=8 */
	adiw r28,8
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
	pop r29
	pop r28
	pop r17
	pop r16
	pop r15
	pop r14
	pop r13
	pop r12
	pop r11
	pop r10
	ret
/* epilogue end (size=17) */
/* function motion_next size 331 (296) */
	.size	motion_next, .-motion_next
.global	motion_append
	.type	motion_append, @function
motion_append:
/* prologue: frame size=0 */
	push r5
	push r6
	push r7
	push r8
	push r9
	push r10
	push r11
	push r12
	push r13
	push r14
	push r15
	push r16
	push r17
	push r28
	push r29
/* prologue end (size=15) */
	lds r5,motion_head
	inc r5
	ldi r24,lo8(7)
	and r5,r24
	lds r24,motion_tail
	cp r5,r24
	brne .+2
	rjmp .L26
	ldi r22,lo8(27)
	ldi r24,lo8(26)
	call registers_read_word
	movw r14,r24
	ldi r22,lo8(29)
	ldi r24,lo8(28)
	call registers_read_word
	movw r12,r24
	ldi r22,lo8(31)
	ldi r24,lo8(30)
	call registers_read_word
	movw r10,r24
	ldi r22,lo8(25)
	ldi r24,lo8(24)
	call registers_read_word
	movw r28,r24
	or r24,r25
	brne .+2
	rjmp .L26
	mov r24,r5
	clr r25
	lsl r24
	rol r25
	movw r16,r24
	ldi r18,3
1:	lsl r16
	rol r17
	dec r18
	brne 1b
	sub r16,r24
	sbc r17,r25
	subi r16,lo8(-(keys))
	sbci r17,hi8(-(keys))
	movw r30,r16
	std Z+1,r29
	st Z,r28
	movw r22,r14
	clr r24
	sbrc r23,7
	com r24
	mov r25,r24
	call __floatsisf
	movw r6,r22
	movw r8,r24
	movw r30,r16
	std Z+2,r22
	std Z+3,r23
	std Z+4,r24
	std Z+5,r25
	movw r22,r12
	clr r24
	sbrc r23,7
	com r24
	mov r25,r24
	call __floatsisf
	ldi r18,lo8(0x3a800000)
	ldi r19,hi8(0x3a800000)
	ldi r20,hlo8(0x3a800000)
	ldi r21,hhi8(0x3a800000)
	call __mulsf3
	movw r30,r16
	std Z+6,r22
	std Z+7,r23
	std Z+8,r24
	std Z+9,r25
	movw r22,r10
	clr r24
	sbrc r23,7
	com r24
	mov r25,r24
	call __floatsisf
	ldi r18,lo8(0x3a800000)
	ldi r19,hi8(0x3a800000)
	ldi r20,hlo8(0x3a800000)
	ldi r21,hhi8(0x3a800000)
	call __mulsf3
	movw r30,r16
	std Z+10,r22
	std Z+11,r23
	std Z+12,r24
	std Z+13,r25
	lds r25,motion_tail
	lds r24,motion_head
	cp r25,r24
	brne .L29
	lds r18,curve_p1
	lds r19,(curve_p1)+1
	lds r20,(curve_p1)+2
	lds r21,(curve_p1)+3
	ldi r24,lo8(0x0)
	ldi r25,hi8(0x0)
	ldi r26,hlo8(0x0)
	ldi r27,hhi8(0x0)
	push r27
	push r26
	push r25
	push r24
	movw r10,r24
	movw r12,r26
	movw r16,r8
	movw r14,r6
	movw r22,r28
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	call curve_init
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
	pop __tmp_reg__
.L29:
	movw r18,r28
	clr r20
	clr r21
	lds r24,motion_duration
	lds r25,(motion_duration)+1
	lds r26,(motion_duration)+2
	lds r27,(motion_duration)+3
	add r24,r18
	adc r25,r19
	adc r26,r20
	adc r27,r21
	sts motion_duration,r24
	sts (motion_duration)+1,r25
	sts (motion_duration)+2,r26
	sts (motion_duration)+3,r27
	sts motion_head,r5
	call motion_registers_reset
	ldi r24,lo8(1)
	ldi r25,hi8(1)
	rjmp .L31
.L26:
	ldi r24,lo8(0)
	ldi r25,hi8(0)
.L31:
/* epilogue: frame size=0 */
	pop r29
	pop r28
	pop r17
	pop r16
	pop r15
	pop r14
	pop r13
	pop r12
	pop r11
	pop r10
	pop r9
	pop r8
	pop r7
	pop r6
	pop r5
	ret
/* epilogue end (size=16) */
/* function motion_append size 198 (167) */
	.size	motion_append, .-motion_append
	.lcomm keys,112
	.comm motion_head,1,1
	.comm motion_tail,1,1
	.comm motion_counter,4,1
	.comm motion_duration,4,1
/* File "motion.c": code  776 = 0x0308 ( 674), prologues  49, epilogues  53 */
