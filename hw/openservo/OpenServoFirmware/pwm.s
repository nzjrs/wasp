	.file	"pwm.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
.global	pwm_stop
	.type	pwm_stop, @function
pwm_stop:
/* prologue: frame size=0 */
/* prologue end (size=0) */
/* #APP */
	cli
/* #NOAPP */
	lds r24,pwm_a
	tst r24
	brne .L2
	lds r24,pwm_b
	tst r24
	breq .L4
.L2:
	lds r24,128
	andi r24,lo8(63)
	sts 128,r24
	lds r24,128
	andi r24,lo8(-49)
	sts 128,r24
	in r24,37-0x20
	andi r24,lo8(-7)
	out 37-0x20,r24
	ldi r24,lo8(0)
.L5:
/* #APP */
	nop
/* #NOAPP */
	subi r24,lo8(-(1))
	cpi r24,lo8(8)
	brne .L5
	sts pwm_a,__zero_reg__
	sts pwm_b,__zero_reg__
.L4:
	sts (136)+1,__zero_reg__
	sts 136,__zero_reg__
	sts (138)+1,__zero_reg__
	sts 138,__zero_reg__
/* #APP */
	sei
/* #NOAPP */
	lds r24,pwm_a
	sts registers+14,r24
	lds r24,pwm_b
	sts registers+15,r24
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function pwm_stop size 52 (51) */
	.size	pwm_stop, .-pwm_stop
.global	pwm_registers_defaults
	.type	pwm_registers_defaults, @function
pwm_registers_defaults:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	ldi r20,lo8(16)
	ldi r21,hi8(16)
	ldi r22,lo8(41)
	ldi r24,lo8(40)
	call registers_write_word
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function pwm_registers_defaults size 7 (6) */
	.size	pwm_registers_defaults, .-pwm_registers_defaults
.global	pwm_init
	.type	pwm_init, @function
pwm_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	ldi r22,lo8(41)
	ldi r24,lo8(40)
	call registers_read_word
	sts (pwm_div)+1,r25
	sts pwm_div,r24
	ldi r30,lo8(128)
	ldi r31,hi8(128)
	st Z,__zero_reg__
/* #APP */
	nop
	nop
	nop
/* #NOAPP */
	in r18,37-0x20
	andi r18,lo8(-7)
	out 37-0x20,r18
	in r18,36-0x20
	ori r18,lo8(6)
	out 36-0x20,r18
	sts (132)+1,__zero_reg__
	sts 132,__zero_reg__
	st Z,__zero_reg__
	ldi r26,lo8(129)
	ldi r27,hi8(129)
	st X,__zero_reg__
	sts 130,__zero_reg__
	sts 111,__zero_reg__
	ldi r18,4
1:	lsl r24
	rol r25
	dec r18
	brne 1b
	sbiw r24,1
	sts (134)+1,r25
	sts 134,r24
	sts (136)+1,__zero_reg__
	sts 136,__zero_reg__
	sts (138)+1,__zero_reg__
	sts 138,__zero_reg__
	st Z,__zero_reg__
	ldi r24,lo8(17)
	st X,r24
	sts registers+14,__zero_reg__
	sts registers+15,__zero_reg__
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function pwm_init size 61 (60) */
	.size	pwm_init, .-pwm_init
.global	pwm_update
	.type	pwm_update, @function
pwm_update:
/* prologue: frame size=0 */
	push r14
	push r15
	push r16
	push r17
	push r28
	push r29
/* prologue end (size=6) */
	movw r14,r24
	movw r28,r22
	ldi r22,lo8(41)
	ldi r24,lo8(40)
	call registers_read_word
	lds r18,pwm_div
	lds r19,(pwm_div)+1
	cp r24,r18
	cpc r25,r19
	breq .L15
	lds r24,128
	andi r24,lo8(63)
	sts 128,r24
	lds r24,128
	andi r24,lo8(-49)
	sts 128,r24
	in r24,37-0x20
	andi r24,lo8(-7)
	out 37-0x20,r24
	ldi r24,lo8(0)
.L17:
/* #APP */
	nop
/* #NOAPP */
	subi r24,lo8(-(1))
	cpi r24,lo8(8)
	brne .L17
	sts pwm_a,__zero_reg__
	sts pwm_b,__zero_reg__
	ldi r22,lo8(41)
	ldi r24,lo8(40)
	call registers_read_word
	sts (pwm_div)+1,r25
	sts pwm_div,r24
	ldi r26,4
1:	lsl r24
	rol r25
	dec r26
	brne 1b
	sbiw r24,1
	sts (134)+1,r25
	sts 134,r24
	sts (132)+1,__zero_reg__
	sts 132,__zero_reg__
	sts (136)+1,__zero_reg__
	sts 136,__zero_reg__
	sts (138)+1,__zero_reg__
	sts 138,__zero_reg__
.L15:
	lds r24,registers+46
	tst r24
	breq .L19
	ldi r22,lo8(45)
	ldi r24,lo8(44)
	call registers_read_word
	movw r16,r24
	ldi r22,lo8(43)
	ldi r24,lo8(42)
	call registers_read_word
	movw r20,r16
	subi r16,lo8(1024)
	sbci r17,hi8(1024)
	brlo .L21
	ldi r20,lo8(1023)
	ldi r21,hi8(1023)
.L21:
	movw r18,r24
	subi r24,lo8(1024)
	sbci r25,hi8(1024)
	brlo .L22
	ldi r18,lo8(1023)
	ldi r19,hi8(1023)
.L22:
	ldi r24,lo8(1023)
	ldi r25,hi8(1023)
	movw r22,r24
	sub r22,r20
	sbc r23,r21
	movw r20,r22
	sub r24,r18
	sbc r25,r19
	rjmp .L23
.L19:
	ldi r22,lo8(43)
	ldi r24,lo8(42)
	call registers_read_word
	movw r16,r24
	ldi r22,lo8(45)
	ldi r24,lo8(44)
	call registers_read_word
	movw r20,r16
	subi r16,lo8(1024)
	sbci r17,hi8(1024)
	brlo .L24
	ldi r20,lo8(1023)
	ldi r21,hi8(1023)
.L24:
	ldi r18,hi8(1024)
	cpi r24,lo8(1024)
	cpc r25,r18
	brlo .L23
	ldi r24,lo8(1023)
	ldi r25,hi8(1023)
.L23:
	cp r14,r20
	cpc r15,r21
	brsh .L26
	sbrs r29,7
	rjmp .L26
	ldi r28,lo8(0)
	ldi r29,hi8(0)
.L26:
	cp r24,r14
	cpc r25,r15
	brsh .L29
	cp __zero_reg__,r28
	cpc __zero_reg__,r29
	brge .L29
	ldi r28,lo8(0)
	ldi r29,hi8(0)
.L29:
	lds r24,registers+5
	sbrs r24,0
	rjmp .L32
	sbrs r29,7
	rjmp .L34
	movw r22,r28
	neg r22
	mov r16,r22
	clr r23
	clr r24
	clr r25
	lds r18,pwm_div
	lds r19,(pwm_div)+1
	clr r20
	clr r21
	ldi r31,4
1:	lsl r18
	rol r19
	rol r20
	rol r21
	dec r31
	brne 1b
	subi r18,lo8(-(-1))
	sbci r19,hi8(-(-1))
	sbci r20,hlo8(-(-1))
	sbci r21,hhi8(-(-1))
	call __mulsi3
	ldi r18,lo8(255)
	ldi r19,hi8(255)
	ldi r20,hlo8(255)
	ldi r21,hhi8(255)
	call __udivmodsi4
/* #APP */
	cli
/* #NOAPP */
	lds r24,pwm_b
	tst r24
	breq .L36
	lds r24,pwm_a
	tst r24
	breq .L38
.L36:
	lds r24,128
	andi r24,lo8(95)
	sts 128,r24
	sts (138)+1,r19
	sts 138,r18
	in r24,37-0x20
	andi r24,lo8(-7)
	out 37-0x20,r24
	ldi r24,lo8(0)
.L39:
/* #APP */
	nop
/* #NOAPP */
	subi r24,lo8(-(1))
	cpi r24,lo8(8)
	brne .L39
	ldi r24,lo8(32)
	sts 128,r24
	sts pwm_a,__zero_reg__
.L38:
	sts pwm_b,r16
	sts (136)+1,__zero_reg__
	sts 136,__zero_reg__
	sts (138)+1,r19
	sts 138,r18
/* #APP */
	sei
/* #NOAPP */
	lds r24,pwm_a
	sts registers+14,r24
	sts registers+15,r16
	rjmp .L48
.L34:
	sbiw r28,0
	brne .+2
	rjmp .L32
	mov r16,r28
	mov r22,r28
	clr r23
	clr r24
	clr r25
	lds r18,pwm_div
	lds r19,(pwm_div)+1
	clr r20
	clr r21
	ldi r30,4
1:	lsl r18
	rol r19
	rol r20
	rol r21
	dec r30
	brne 1b
	subi r18,lo8(-(-1))
	sbci r19,hi8(-(-1))
	sbci r20,hlo8(-(-1))
	sbci r21,hhi8(-(-1))
	call __mulsi3
	ldi r18,lo8(255)
	ldi r19,hi8(255)
	ldi r20,hlo8(255)
	ldi r21,hhi8(255)
	call __udivmodsi4
/* #APP */
	cli
/* #NOAPP */
	lds r24,pwm_a
	tst r24
	breq .L43
	lds r24,pwm_b
	tst r24
	breq .L45
.L43:
	lds r24,128
	andi r24,lo8(95)
	sts 128,r24
	sts (136)+1,r19
	sts 136,r18
	in r24,37-0x20
	andi r24,lo8(-7)
	out 37-0x20,r24
	ldi r24,lo8(0)
.L46:
/* #APP */
	nop
/* #NOAPP */
	subi r24,lo8(-(1))
	cpi r24,lo8(8)
	brne .L46
	lds r24,128
	ori r24,lo8(-128)
	sts 128,r24
	sts pwm_b,__zero_reg__
.L45:
	sts pwm_a,r16
	sts (136)+1,r19
	sts 136,r18
	sts (138)+1,__zero_reg__
	sts 138,__zero_reg__
/* #APP */
	sei
/* #NOAPP */
	sts registers+14,r16
	lds r24,pwm_b
	sts registers+15,r24
	rjmp .L48
.L32:
	call pwm_stop
.L48:
/* epilogue: frame size=0 */
	pop r29
	pop r28
	pop r17
	pop r16
	pop r15
	pop r14
	ret
/* epilogue end (size=7) */
/* function pwm_update size 330 (317) */
	.size	pwm_update, .-pwm_update
	.lcomm pwm_a,1
	.lcomm pwm_b,1
	.lcomm pwm_div,2
/* File "pwm.c": code  450 = 0x01c2 ( 434), prologues   6, epilogues  10 */
