# 1 "watchdog.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "watchdog.c"
# 31 "watchdog.c"
# 1 "c:/winavr-20070525/bin/../avr/include/inttypes.h" 1 3
# 37 "c:/winavr-20070525/bin/../avr/include/inttypes.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/stdint.h" 1 3
# 121 "c:/winavr-20070525/bin/../avr/include/stdint.h" 3
typedef int int8_t __attribute__((__mode__(__QI__)));
typedef unsigned int uint8_t __attribute__((__mode__(__QI__)));
typedef int int16_t __attribute__ ((__mode__ (__HI__)));
typedef unsigned int uint16_t __attribute__ ((__mode__ (__HI__)));
typedef int int32_t __attribute__ ((__mode__ (__SI__)));
typedef unsigned int uint32_t __attribute__ ((__mode__ (__SI__)));

typedef int int64_t __attribute__((__mode__(__DI__)));
typedef unsigned int uint64_t __attribute__((__mode__(__DI__)));
# 142 "c:/winavr-20070525/bin/../avr/include/stdint.h" 3
typedef int16_t intptr_t;




typedef uint16_t uintptr_t;
# 159 "c:/winavr-20070525/bin/../avr/include/stdint.h" 3
typedef int8_t int_least8_t;




typedef uint8_t uint_least8_t;




typedef int16_t int_least16_t;




typedef uint16_t uint_least16_t;




typedef int32_t int_least32_t;




typedef uint32_t uint_least32_t;







typedef int64_t int_least64_t;






typedef uint64_t uint_least64_t;
# 213 "c:/winavr-20070525/bin/../avr/include/stdint.h" 3
typedef int8_t int_fast8_t;




typedef uint8_t uint_fast8_t;




typedef int16_t int_fast16_t;




typedef uint16_t uint_fast16_t;




typedef int32_t int_fast32_t;




typedef uint32_t uint_fast32_t;







typedef int64_t int_fast64_t;






typedef uint64_t uint_fast64_t;
# 273 "c:/winavr-20070525/bin/../avr/include/stdint.h" 3
typedef int64_t intmax_t;




typedef uint64_t uintmax_t;
# 38 "c:/winavr-20070525/bin/../avr/include/inttypes.h" 2 3
# 77 "c:/winavr-20070525/bin/../avr/include/inttypes.h" 3
typedef int32_t int_farptr_t;



typedef uint32_t uint_farptr_t;
# 32 "watchdog.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 1 3
# 87 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/avr/sfr_defs.h" 1 3
# 88 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 2 3
# 278 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/avr/iom168.h" 1 3
# 36 "c:/winavr-20070525/bin/../avr/include/avr/iom168.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/avr/iomx8.h" 1 3
# 37 "c:/winavr-20070525/bin/../avr/include/avr/iom168.h" 2 3
# 279 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 2 3
# 360 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/avr/portpins.h" 1 3
# 361 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 2 3
# 370 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 3
# 1 "c:/winavr-20070525/bin/../avr/include/avr/version.h" 1 3
# 371 "c:/winavr-20070525/bin/../avr/include/avr/io.h" 2 3
# 33 "watchdog.c" 2

# 1 "openservo.h" 1
# 49 "openservo.h"
inline static uint8_t disable_interrupts(void)
{
    uint8_t sreg;

    asm volatile (
        "in %0,__SREG__\n\t"
        "cli\n\t"
        : "=r" ((uint8_t) sreg)
        :
    );

    return sreg;
}


inline static void restore_interrupts(uint8_t sreg)
{
    asm volatile (
        "out __SREG__,%0\n\t"
        :
        : "r" ((uint8_t) sreg)
    );
}
# 35 "watchdog.c" 2
# 1 "config.h" 1
# 36 "watchdog.c" 2
# 1 "pwm.h" 1
# 30 "pwm.h"
# 1 "registers.h" 1
# 187 "registers.h"
extern uint8_t registers[(0x38 + 16)];



void registers_init(void);
void registers_defaults(void);
uint16_t registers_read_word(uint8_t address_hi, uint8_t address_lo);
void registers_write_word(uint8_t address_hi, uint8_t address_lo, uint16_t value);




inline static uint8_t registers_read_byte(uint8_t address)
{
    return registers[address];
}



inline static void registers_write_byte(uint8_t address, uint8_t value)
{
    registers[address] = value;
}


inline static void registers_write_enable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo | (1<<0x01));
}


inline static void registers_write_disable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo & ~(1<<0x01));
}


inline static uint8_t registers_is_write_enabled(void)
{
    return (registers_read_byte(0x05) & (1<<0x01)) ? 1 : 0;
}


inline static uint8_t registers_is_write_disabled(void)
{
    return (registers_read_byte(0x05) & (1<<0x01)) ? 0 : 1;
}
# 31 "pwm.h" 2

void pwm_registers_defaults(void);
void pwm_init(void);
void pwm_update(uint16_t position, int16_t pwm);
void pwm_stop(void);

inline static void pwm_enable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo | (1<<0x00));
}


inline static void pwm_disable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo & ~(1<<0x00));


    pwm_stop();
}
# 37 "watchdog.c" 2

void watchdog_init(void)

{
# 62 "watchdog.c"
    (*(volatile uint8_t *)((0x34) + 0x20)) &= ~(1<<3);


    (*(volatile uint8_t *)(0x60)) |= (1<<4) | (1<<3);


    (*(volatile uint8_t *)(0x60)) = 0x00;

}


void watchdog_hard_reset(void)

{

    pwm_disable();
# 96 "watchdog.c"
    (*(volatile uint8_t *)(0x60)) = (1<<7) |
             (0<<6) |
             (1<<3) |
             (0<<5) | (0<<2) | (0<<1) | (0<<0);



    for (;;);
}
