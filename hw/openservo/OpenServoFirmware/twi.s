	.file	"twi.c"
	.arch atmega168
__SREG__ = 0x3f
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__tmp_reg__ = 0
__zero_reg__ = 1
	.global __do_copy_data
	.global __do_clear_bss
	.text
	.type	twi_registers_read, @function
twi_registers_read:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	andi r24,lo8(127)
	cpi r24,lo8(56)
	brlo .L14
	cpi r24,lo8(96)
	brlo .L5
	cpi r24,lo8(112)
	brsh .L12
	subi r24,lo8(-(-40))
.L14:
	mov r30,r24
	clr r31
	subi r30,lo8(-(registers))
	sbci r31,hi8(-(registers))
	ld r24,Z
	rjmp .L13
.L12:
	subi r24,lo8(-(-56))
	mov r30,r24
	clr r31
	subi r30,lo8(-(registers))
	sbci r31,hi8(-(registers))
	ld r24,Z
	clr r25
	cpi r24,lo8(112)
	brsh .L5
	call twi_registers_read
.L13:
	clr r25
	ret
.L5:
	ldi r24,lo8(0)
	ldi r25,hi8(0)
	ret
/* epilogue: frame size=0 */
/* epilogue: noreturn */
/* epilogue end (size=0) */
/* function twi_registers_read size 30 (30) */
	.size	twi_registers_read, .-twi_registers_read
	.type	twi_registers_write, @function
twi_registers_write:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	mov r30,r24
	lds r24,registers+5
	clr r25
	andi r24,lo8(2)
	andi r25,hi8(2)
.L17:
	andi r30,lo8(127)
	cpi r30,lo8(16)
	brlo .L29
	cpi r30,lo8(32)
	brlo .L32
	sbiw r24,0
	breq .L29
	cpi r30,lo8(56)
	brlo .L32
	cpi r30,lo8(96)
	brlo .L29
	cpi r30,lo8(112)
	brsh .L31
	subi r30,lo8(-(-40))
.L32:
	clr r31
	subi r30,lo8(-(registers))
	sbci r31,hi8(-(registers))
	st Z,r22
	ret
.L31:
	subi r30,lo8(-(-72))
	clr r31
	subi r30,lo8(-(registers))
	sbci r31,hi8(-(registers))
	ld r30,Z
	cpi r30,lo8(112)
	brlo .L17
.L29:
	ret
/* epilogue: frame size=0 */
/* epilogue: noreturn */
/* epilogue end (size=0) */
/* function twi_registers_write size 33 (33) */
	.size	twi_registers_write, .-twi_registers_write
.global	twi_slave_init
	.type	twi_slave_init, @function
twi_slave_init:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	sts twi_rxtail,__zero_reg__
	sts twi_rxhead,__zero_reg__
	lsl r24
	sts 186,r24
	ldi r24,lo8(-1)
	sts 187,r24
	ldi r24,lo8(-59)
	sts 188,r24
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function twi_slave_init size 14 (13) */
	.size	twi_slave_init, .-twi_slave_init
.global	twi_receive_byte
	.type	twi_receive_byte, @function
twi_receive_byte:
/* prologue: frame size=0 */
/* prologue end (size=0) */
.L37:
	lds r25,twi_rxhead
	lds r24,twi_rxtail
	cp r25,r24
	breq .L37
	lds r24,twi_rxtail
	subi r24,lo8(-(1))
	andi r24,lo8(3)
	sts twi_rxtail,r24
	lds r30,twi_rxtail
	clr r31
	subi r30,lo8(-(twi_rxbuf))
	sbci r31,hi8(-(twi_rxbuf))
	ld r24,Z
	clr r25
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function twi_receive_byte size 20 (19) */
	.size	twi_receive_byte, .-twi_receive_byte
.global	twi_data_in_receive_buffer
	.type	twi_data_in_receive_buffer, @function
twi_data_in_receive_buffer:
/* prologue: frame size=0 */
/* prologue end (size=0) */
	lds r25,twi_rxhead
	lds r24,twi_rxtail
	ldi r18,lo8(0)
	ldi r19,hi8(0)
	cp r25,r24
	breq .L43
	ldi r18,lo8(1)
	ldi r19,hi8(1)
.L43:
	movw r24,r18
/* epilogue: frame size=0 */
	ret
/* epilogue end (size=1) */
/* function twi_data_in_receive_buffer size 12 (11) */
	.size	twi_data_in_receive_buffer, .-twi_data_in_receive_buffer
.global	__vector_24
	.type	__vector_24, @function
__vector_24:
/* prologue: frame size=0 */
	push __zero_reg__
	push __tmp_reg__
	in __tmp_reg__,__SREG__
	push __tmp_reg__
	clr __zero_reg__
	push r16
	push r17
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
/* prologue end (size=19) */
	lds r24,185
	cpi r24,lo8(-96)
	brne .+2
	rjmp .L46
	cpi r24,lo8(-95)
	brsh .L54
	cpi r24,lo8(96)
	brne .+2
	rjmp .L48
	cpi r24,lo8(97)
	brsh .L55
	tst r24
	brne .+2
	rjmp .L47
	rjmp .L46
.L55:
	cpi r24,lo8(-128)
	breq .L49
	rjmp .L46
.L54:
	cpi r24,lo8(-64)
	brne .+2
	rjmp .L46
	cpi r24,lo8(-63)
	brsh .L56
	cpi r24,lo8(-88)
	breq .L51
	cpi r24,lo8(-72)
	breq .+2
	rjmp .L46
	rjmp .L51
.L56:
	cpi r24,lo8(-56)
	brne .+2
	rjmp .L46
	cpi r24,lo8(-8)
	breq .+2
	rjmp .L46
	rjmp .L79
.L51:
	lds r24,twi_address
	call twi_registers_read
	mov r25,r24
	lds r24,twi_data_state
	cpi r24,lo8(4)
	brne .L57
	lds r19,twi_chk_count
	lds r24,twi_chk_count_target
	lds r18,twi_chk_sum
	cp r19,r24
	brsh .L59
	add r18,r25
	sts twi_chk_sum,r18
	subi r19,lo8(-(1))
	sts twi_chk_count,r19
	rjmp .L57
.L59:
	mov r25,r18
	rjmp .L61
.L57:
	lds r24,twi_address
	subi r24,lo8(-(1))
	sts twi_address,r24
.L61:
	mov r24,r25
	clr r25
	sts 187,r24
	rjmp .L46
.L48:
	sts twi_data_state,__zero_reg__
	rjmp .L46
.L49:
	lds r22,187
	lds r24,twi_data_state
	cpi r24,lo8(2)
	breq .L65
	cpi r24,lo8(3)
	brsh .L68
	tst r24
	breq .L63
	cpi r24,lo8(1)
	breq .+2
	rjmp .L46
	rjmp .L64
.L68:
	cpi r24,lo8(3)
	breq .L66
	cpi r24,lo8(4)
	breq .+2
	rjmp .L46
	rjmp .L67
.L63:
	sbrc r22,7
	rjmp .L69
	sts twi_address,r22
	ldi r24,lo8(1)
	rjmp .L80
.L69:
	cpi r22,lo8(-127)
	brne .L71
	ldi r24,lo8(2)
.L80:
	sts twi_data_state,r24
	rjmp .L46
.L71:
	lds r24,twi_rxhead
	subi r24,lo8(-(1))
	andi r24,lo8(3)
	sts twi_rxhead,r24
	lds r30,twi_rxhead
	clr r31
	subi r30,lo8(-(twi_rxbuf))
	sbci r31,hi8(-(twi_rxbuf))
	st Z,r22
	rjmp .L46
.L64:
	lds r24,twi_address
	call twi_registers_write
	lds r24,twi_address
	subi r24,lo8(-(1))
	sts twi_address,r24
	rjmp .L46
.L65:
	mov r24,r22
	andi r24,lo8(15)
	sts twi_chk_count_target,r24
	sts twi_chk_sum,r24
	sts twi_chk_count,__zero_reg__
	ldi r24,lo8(3)
	rjmp .L80
.L66:
	lds r24,twi_chk_sum
	sts twi_address,r22
	lds r25,twi_address
	add r24,r25
	sts twi_chk_sum,r24
	ldi r24,lo8(4)
	rjmp .L80
.L67:
	lds r24,twi_chk_count
	lds r16,twi_chk_count_target
	lds r18,twi_chk_sum
	cp r24,r16
	brsh .L73
	mov r30,r24
	clr r31
	andi r30,lo8(15)
	andi r31,hi8(15)
	subi r30,lo8(-(twi_chk_write_buffer))
	sbci r31,hi8(-(twi_chk_write_buffer))
	st Z,r22
	add r18,r22
	sts twi_chk_sum,r18
	subi r24,lo8(-(1))
	sts twi_chk_count,r24
	rjmp .L46
.L73:
	cp r22,r18
	brne .L46
	sts twi_chk_count,__zero_reg__
	ldi r17,lo8(0)
	rjmp .L76
.L77:
	lds r24,twi_address
	mov r30,r17
	clr r31
	andi r30,lo8(15)
	andi r31,hi8(15)
	subi r30,lo8(-(twi_chk_write_buffer))
	sbci r31,hi8(-(twi_chk_write_buffer))
	ld r22,Z
	call twi_registers_write
	lds r24,twi_address
	subi r24,lo8(-(1))
	sts twi_address,r24
	subi r17,lo8(-(1))
.L76:
	cp r17,r16
	brlo .L77
	sts twi_chk_count,r17
	rjmp .L46
.L47:
	ldi r24,lo8(-43)
	rjmp .L81
.L46:
	ldi r24,lo8(-59)
.L81:
	sts 188,r24
.L79:
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
	pop r17
	pop r16
	pop __tmp_reg__
	out __SREG__,__tmp_reg__
	pop __tmp_reg__
	pop __zero_reg__
	reti
/* epilogue end (size=19) */
/* function __vector_24 size 244 (206) */
	.size	__vector_24, .-__vector_24
	.lcomm twi_address,1
	.lcomm twi_data_state,1
	.lcomm twi_rxhead,1
	.lcomm twi_rxtail,1
	.lcomm twi_rxbuf,4
	.lcomm twi_chk_count,1
	.lcomm twi_chk_count_target,1
	.lcomm twi_chk_sum,1
	.lcomm twi_chk_write_buffer,16
/* File "twi.c": code  353 = 0x0161 ( 312), prologues  19, epilogues  22 */
