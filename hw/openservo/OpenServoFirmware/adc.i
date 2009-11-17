# 1 "adc.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "adc.c"
# 27 "adc.c"
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
# 28 "adc.c" 2
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
# 29 "adc.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/avr/interrupt.h" 1 3
# 30 "adc.c" 2

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
# 32 "adc.c" 2
# 1 "config.h" 1
# 33 "adc.c" 2
# 1 "adc.h" 1
# 31 "adc.h"
void adc_init(void);


extern volatile uint8_t adc_power_ready;
extern volatile uint16_t adc_power_value;
extern volatile uint8_t adc_position_ready;
extern volatile uint16_t adc_position_value;
extern volatile uint8_t adc_voltage_needed;




inline static uint16_t adc_get_power_value(void)

{

    adc_power_ready = 0;


    return adc_power_value;
}

inline static uint8_t adc_power_value_is_ready(void)

{

    return adc_power_ready;
}

inline static void adc_power_value_clear_ready(void)

{
    adc_power_ready = 0;
}



inline static uint16_t adc_get_position_value(void)

{

    adc_position_ready = 0;


    return adc_position_value;
}

inline static uint8_t adc_position_value_is_ready(void)

{

    return adc_position_ready;
}

inline static void adc_position_value_clear_ready(void)

{
    adc_position_ready = 0;
}

inline static void adc_read_voltage(void)

{
    adc_voltage_needed = 1;
}
# 34 "adc.c" 2
# 1 "timer.h" 1
# 30 "timer.h"
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
# 31 "timer.h" 2

static inline void timer_set(uint16_t value)
{

    registers_write_word(0x06, 0x07, value);
}

static inline uint16_t timer_get(void)
{

    return registers_read_word(0x06, 0x07);
}

static inline uint16_t timer_delta(uint16_t time_stamp)
{
    uint16_t delta_time;


    uint16_t current_time = registers_read_word(0x06, 0x07);


    if (current_time > time_stamp)
        delta_time = current_time - time_stamp;
    else
        delta_time = 0xffff - (time_stamp - current_time) + 1;

    return delta_time;
}

static inline void timer_increment(void)
{
    uint16_t value;


    value = registers_read_word(0x06, 0x07);


    ++value;


    registers_write_word(0x06, 0x07, value);
}
# 35 "adc.c" 2
# 95 "adc.c"
volatile uint8_t adc_channel;
volatile uint8_t adc_power_ready;
volatile uint16_t adc_power_value;
volatile uint8_t adc_position_ready;
volatile uint16_t adc_position_value;
volatile uint8_t adc_voltage_needed;


void adc_init(void)

{

    adc_channel = 1;


    adc_power_ready = 0;
    adc_power_value = 0;
    adc_position_ready = 0;
    adc_position_value = 0;
    adc_voltage_needed = 1;
# 169 "adc.c"
    (*(volatile uint8_t *)((0x08) + 0x20)) &= ~((1<<0) | (1<<1) | (1<<2));


    (*(volatile uint8_t *)(0x7E)) |= (1<<2) | (1<<1) |(1<<0);


    (*(volatile uint8_t *)(0x7C)) = (0<<7) | (1<<6) |
            (0<<3) | (0<<2) | (1<<1) | (0<<0) |
            (0<<5);


    (*(volatile uint8_t *)(0x7B)) = (0<<2) | (1<<1) | (1<<0);


    (*(volatile uint8_t *)(0x7A)) = (1<<7) |
             (0<<6) |
             (1<<5) |
             (1<<3) |
             ((1<<2) | (1<<1) | (0<<0));
# 223 "adc.c"
    (*(volatile uint8_t *)((0x24) + 0x20)) = (0<<7) | (0<<6) |
             (0<<5) | (0<<4) |
             (1<<1) | (0<<0);


    (*(volatile uint8_t *)((0x25) + 0x20)) = (0<<7) | (0<<6) |
             (0<<3) |
             ((1<<2) | (0<<1) | (1<<0));


    (*(volatile uint8_t *)(0x6E)) = (1<<1) |
             (0<<2) |
             (0<<0);


    (*(volatile uint8_t *)((0x27) + 0x20)) = 78;

}




void __vector_14 (void) __attribute__ ((signal,used, externally_visible)); void __vector_14 (void)

{

    if (adc_channel == 1) timer_increment();
}
# 278 "adc.c"
void __vector_21 (void) __attribute__ ((signal,used, externally_visible)); void __vector_21 (void)

{

    uint16_t new_value = (*(volatile uint16_t *)(0x78));


    switch (adc_channel)
    {

        case 1:


            adc_position_value = new_value;


            adc_position_ready = 1;


            adc_channel = 0;
# 311 "adc.c"
            (*(volatile uint8_t *)(0x7C)) = (0<<7) | (1<<6) |
                    (0<<3) | (0<<2) | (0<<1) | (0<<0) |
                    (0<<5);


            (*(volatile uint8_t *)(0x7A)) |= (1<<6);


            break;


        case 0:


            adc_power_value = new_value;


            adc_power_ready = 1;
# 346 "adc.c"
            if (adc_voltage_needed)
            {

                adc_channel = 2;


                (*(volatile uint8_t *)(0x7C)) = (0<<7) | (1<<6) |
                        (0<<3) | (0<<2) | (0<<1) | (1<<0) |
                        (0<<5);


                (*(volatile uint8_t *)(0x7A)) |= (1<<6);
            }
            else
            {

                adc_channel = 1;


                (*(volatile uint8_t *)(0x7C)) = (0<<7) | (1<<6) |
                        (0<<3) | (0<<2) | (1<<1) | (0<<0) |
                        (0<<5);
            }

            break;


        case 2:


            adc_voltage_needed = 0;


            registers_write_word(0x14, 0x15, new_value);


            adc_channel = 1;


            (*(volatile uint8_t *)(0x7C)) = (0<<7) | (1<<6) |
                    (0<<3) | (0<<2) | (1<<1) | (0<<0) |
                    (0<<5);
            break;



    }
}
