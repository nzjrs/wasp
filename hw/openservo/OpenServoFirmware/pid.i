# 1 "pid.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "pid.c"
# 27 "pid.c"
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
# 28 "pid.c" 2

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
# 30 "pid.c" 2
# 1 "config.h" 1
# 31 "pid.c" 2
# 1 "pid.h" 1
# 31 "pid.h"
void pid_init(void);


void pid_registers_defaults(void);



int16_t pid_position_to_pwm(int16_t position);
# 32 "pid.c" 2
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
# 33 "pid.c" 2
# 43 "pid.c"
static int16_t previous_seek;
static int16_t previous_position;
# 65 "pid.c"
static int32_t filter_reg = 0;

static int16_t filter_update(int16_t input)
{

    filter_reg = filter_reg - (filter_reg >> 1) + input;


    return (int16_t) (filter_reg >> 1);
}

void pid_init(void)

{

    previous_seek = 0;
    previous_position = 0;
}


void pid_registers_defaults(void)


{

    registers_write_byte(0x21, 0x00);


    registers_write_word(0x22, 0x23, 0x0000);
    registers_write_word(0x24, 0x25, 0x0000);
    registers_write_word(0x26, 0x27, 0x0000);


    registers_write_word(0x2A, 0x2B, 0x0060);
    registers_write_word(0x2C, 0x2D, 0x03A0);


    registers_write_byte(0x2E, 0x00);
}


int16_t pid_position_to_pwm(int16_t current_position)



{

    static int16_t deadband;
    static int16_t p_component;
    static int16_t d_component;
    static int16_t seek_position;
    static int16_t seek_velocity;
    static int16_t minimum_position;
    static int16_t maximum_position;
    static int16_t current_velocity;
    static int16_t filtered_position;
    static int32_t pwm_output;
    static uint16_t d_gain;
    static uint16_t p_gain;


    filtered_position = filter_update(current_position);


    current_velocity = filtered_position - previous_position;
    previous_position = filtered_position;


    seek_position = (int16_t) registers_read_word(0x10, 0x11);
    seek_velocity = (int16_t) registers_read_word(0x12, 0x13);


    minimum_position = (int16_t) registers_read_word(0x2A, 0x2B);
    maximum_position = (int16_t) registers_read_word(0x2C, 0x2D);


    if (registers_read_byte(0x2E) != 0)
    {

        registers_write_word(0x08, 0x09, (uint16_t) ((1023) - current_position));
        registers_write_word(0x0A, 0x0B, (uint16_t) -current_velocity);


        seek_position = (1023) - seek_position;
        minimum_position = (1023) - minimum_position;
        maximum_position = (1023) - maximum_position;
    }
    else
    {

        registers_write_word(0x08, 0x09, (uint16_t) current_position);
        registers_write_word(0x0A, 0x0B, (uint16_t) current_velocity);
    }


    deadband = (int16_t) registers_read_byte(0x21);


    if (seek_position == previous_seek) current_position = filtered_position;
    previous_seek = seek_position;


    if (seek_position < minimum_position) seek_position = minimum_position;
    if (seek_position > maximum_position) seek_position = maximum_position;


    p_component = seek_position - current_position;


    d_component = seek_velocity - current_velocity;


    p_gain = registers_read_word(0x22, 0x23);
    d_gain = registers_read_word(0x24, 0x25);


    pwm_output = 0;


    if ((p_component > deadband) || (p_component < -deadband))
    {

        pwm_output += (int32_t) p_component * (int32_t) p_gain;
    }


    pwm_output += (int32_t) d_component * (int32_t) d_gain;


    pwm_output >>= 8;


    if (pwm_output > (255))
    {

        pwm_output = (255);
    }
    else if (pwm_output < (-(255)))
    {

        pwm_output = (-(255));
    }


    return (int16_t) pwm_output;
}
