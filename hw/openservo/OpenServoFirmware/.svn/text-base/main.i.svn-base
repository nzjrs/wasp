# 1 "main.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "main.c"
# 27 "main.c"
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
# 28 "main.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/avr/interrupt.h" 1 3
# 36 "c:/winavr-20070525/bin/../avr/include/avr/interrupt.h" 3
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
# 37 "c:/winavr-20070525/bin/../avr/include/avr/interrupt.h" 2 3
# 29 "main.c" 2


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
# 32 "main.c" 2
# 1 "config.h" 1
# 33 "main.c" 2
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
# 34 "main.c" 2
# 1 "eeprom.h" 1
# 37 "eeprom.h"
uint8_t eeprom_erase(void);
uint8_t eeprom_restore_registers(void);
uint8_t eeprom_save_registers(void);
# 35 "main.c" 2
# 1 "estimator.h" 1
# 32 "estimator.h"
void estimator_init(void);


void estimator_registers_defaults(void);




void estimate_velocity(int16_t position);
# 36 "main.c" 2
# 1 "ipd.h" 1
# 31 "ipd.h"
void ipd_init(void);


void ipd_registers_defaults(void);



int16_t ipd_position_to_pwm(int16_t position);
# 37 "main.c" 2
# 1 "motion.h" 1
# 32 "motion.h"
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
# 33 "motion.h" 2






extern uint8_t motion_head;
extern uint8_t motion_tail;
extern uint32_t motion_counter;
extern uint32_t motion_duration;


void motion_init(void);
void motion_reset(int16_t position);
void motion_registers_reset(void);
uint8_t motion_append(void);
void motion_next(uint16_t delta);
uint8_t motion_buffer_left(void);



inline static void motion_enable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo | (1<<0x02));
}


inline static void motion_disable(void)
{
    uint8_t flags_lo = registers_read_byte(0x05);


    registers_write_byte(0x05, flags_lo & ~(1<<0x02));
}


inline static uint32_t motion_time_left(void)

{

    return motion_duration - motion_counter;
}
# 38 "main.c" 2
# 1 "pid.h" 1
# 31 "pid.h"
void pid_init(void);


void pid_registers_defaults(void);



int16_t pid_position_to_pwm(int16_t position);
# 39 "main.c" 2
# 1 "regulator.h" 1
# 31 "regulator.h"
void regulator_init(void);


void regulator_registers_defaults(void);



int16_t regulator_position_to_pwm(int16_t position);
# 40 "main.c" 2
# 1 "power.h" 1
# 30 "power.h"
void power_init(void);
void power_update(uint16_t power);
# 41 "main.c" 2
# 1 "pwm.h" 1
# 32 "pwm.h"
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
# 42 "main.c" 2
# 1 "seek.h" 1
# 43 "main.c" 2
# 1 "pulsectl.h" 1
# 30 "pulsectl.h"
void pulse_control_init(void);
void pulse_control_update(void);
# 44 "main.c" 2
# 1 "timer.h" 1
# 32 "timer.h"
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
# 45 "main.c" 2
# 1 "twi.h" 1
# 93 "twi.h"
void twi_slave_init(uint8_t);
uint8_t twi_receive_byte(void);
uint8_t twi_data_in_receive_buffer(void);
# 46 "main.c" 2
# 1 "watchdog.h" 1
# 30 "watchdog.h"
void watchdog_init(void);
void watchdog_hard_reset(void);
# 47 "main.c" 2


static void config_pin_defaults(void)



{


    (*(volatile uint8_t *)((0x04) + 0x20)) = (0<<7) | (0<<6) | (0<<5) | (0<<4) |
           (0<<3) | (1<<2) | (1<<1) | (0<<0);
    (*(volatile uint8_t *)((0x05) + 0x20)) = (1<<7) | (1<<6) | (1<<5) | (1<<4) |
            (1<<3) | (0<<2) | (0<<1) | (1<<0);


    (*(volatile uint8_t *)((0x07) + 0x20)) = (0<<6) | (0<<5) | (0<<4) |
           (0<<3) | (0<<2) | (0<<1) | (0<<0);
    (*(volatile uint8_t *)((0x08) + 0x20)) = (1<<6) | (1<<5) | (1<<4) |
            (1<<3) | (1<<2) | (1<<1) | (1<<0);


    (*(volatile uint8_t *)((0x0A) + 0x20)) = (0<<7) | (0<<6) | (0<<5) | (0<<4) |
           (0<<3) | (0<<2) | (0<<1) | (0<<0);
    (*(volatile uint8_t *)((0x0B) + 0x20)) = (1<<7) | (1<<6) | (1<<5) | (1<<4) |
            (1<<3) | (1<<2) | (1<<1) | (1<<0);

}


static void handle_twi_command(void)
{
    uint8_t command;


    command = twi_receive_byte();

    switch (command)
    {
        case 0x80:


            watchdog_hard_reset();

            break;

        case 0x82:


            pwm_enable();

            break;

        case 0x83:


            pwm_disable();

            break;

        case 0x84:


            registers_write_enable();

            break;

        case 0x85:


            registers_write_disable();

            break;

        case 0x86:


            eeprom_save_registers();

            break;

        case 0x87:


            eeprom_restore_registers();

            break;

        case 0x88:


            registers_defaults();
            break;

        case 0x89:


            eeprom_erase();

            break;

        case 0x90:


            adc_read_voltage();

            break;


        case 0x91:


            motion_enable();

            break;

        case 0x92:


            motion_disable();

            break;

        case 0x93:


            motion_reset(adc_get_position_value());

            break;

        case 0x94:


            motion_append();

            break;


        default:


            break;
    }
}


int main (void)
{

 config_pin_defaults();


    watchdog_init();


    registers_init();


    pwm_init();


    adc_init();
# 221 "main.c"
    pid_init();
# 231 "main.c"
    motion_init();



    power_init();






    twi_slave_init(registers_read_byte(0x20));


    timer_set(0);


    __asm__ __volatile__ ("sei" ::);


    while (!adc_position_value_is_ready());



    motion_reset(adc_get_position_value());



    registers_write_word(0x10, 0x11, adc_get_position_value());
    registers_write_word(0x12, 0x13, 0);




    pwm_enable();
    registers_write_enable();



    for (;;)
    {

        if (adc_position_value_is_ready())
        {
            int16_t pwm;
            int16_t position;
# 285 "main.c"
            motion_next(10);



            position = (int16_t) adc_get_position_value();
# 298 "main.c"
            pwm = pid_position_to_pwm(position);
# 313 "main.c"
            pwm_update(position, pwm);
        }


        if (adc_power_value_is_ready())
        {

            uint16_t power = adc_get_power_value();


            power_update(power);
        }


        if (twi_data_in_receive_buffer())
        {

            handle_twi_command();
        }
# 373 "main.c"
    }

    return 0;
}
