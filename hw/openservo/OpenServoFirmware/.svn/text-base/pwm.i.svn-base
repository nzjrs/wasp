# 1 "pwm.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "pwm.c"
# 34 "pwm.c"
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
# 35 "pwm.c" 2
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
# 36 "pwm.c" 2


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
# 39 "pwm.c" 2
# 1 "config.h" 1
# 40 "pwm.c" 2
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
# 41 "pwm.c" 2
# 65 "pwm.c"
static uint8_t pwm_a;
static uint8_t pwm_b;


static uint16_t pwm_div;
# 79 "pwm.c"
inline static void delay_loop(int n)
{
    uint8_t i;
    for(i=0; i<n; i++)
    {
        asm("nop");
    }
}




static void pwm_dir_a(uint8_t pwm_duty)


{

    uint16_t duty_cycle = (uint16_t) (((uint32_t) pwm_duty * (((uint32_t) pwm_div << 4) - 1)) / 255);


    __asm__ __volatile__ ("cli" ::);


    if (!pwm_a || pwm_b)
    {



        (*(volatile uint8_t *)(0x80)) &= ~((1<<7) | (1<<5));

        (*(volatile uint16_t *)(0x88)) = duty_cycle;


        (*(volatile uint8_t *)((0x05) + 0x20)) &= ~((1<<1) | (1<<2));




        delay_loop(8);


        (*(volatile uint8_t *)(0x80)) |= (1<<7);


        pwm_b = 0;
    }


    pwm_a = pwm_duty;


    (*(volatile uint16_t *)(0x88)) = duty_cycle;
    (*(volatile uint16_t *)(0x8A)) = 0;


    __asm__ __volatile__ ("sei" ::);


    registers_write_byte(0x0E, pwm_a);
    registers_write_byte(0x0F, pwm_b);
}


static void pwm_dir_b(uint8_t pwm_duty)


{

    uint16_t duty_cycle = (uint16_t) (((uint32_t) pwm_duty * (((uint32_t) pwm_div << 4) - 1)) / 255);


    __asm__ __volatile__ ("cli" ::);


    if (!pwm_b || pwm_a)
    {



       (*(volatile uint8_t *)(0x80)) &= ~((1<<7) | (1<<5));

       (*(volatile uint16_t *)(0x8A)) = duty_cycle;


        (*(volatile uint8_t *)((0x05) + 0x20)) &= ~((1<<1) | (1<<2));




        delay_loop(8);


        (*(volatile uint8_t *)(0x80)) = (1<<5);


        pwm_a = 0;
    }


    pwm_b = pwm_duty;


    (*(volatile uint16_t *)(0x88)) = 0;
    (*(volatile uint16_t *)(0x8A)) = duty_cycle;


    __asm__ __volatile__ ("sei" ::);


    registers_write_byte(0x0E, pwm_a);
    registers_write_byte(0x0F, pwm_b);
}


void pwm_registers_defaults(void)


{






    registers_write_word(0x28, 0x29, 0x0010);
}


void pwm_init(void)

{

    pwm_div = registers_read_word(0x28, 0x29);

    (*(volatile uint8_t *)(0x80)) = 0;
        asm("nop");
        asm("nop");
        asm("nop");


    (*(volatile uint8_t *)((0x05) + 0x20)) &= ~((1<<1) | (1<<2));


    (*(volatile uint8_t *)((0x04) + 0x20)) |= ((1<<1) | (1<<2));


    (*(volatile uint16_t *)(0x84)) = 0;
    (*(volatile uint8_t *)(0x80)) = 0;
    (*(volatile uint8_t *)(0x81)) = 0;
    (*(volatile uint8_t *)(0x82)) = 0;
    (*(volatile uint8_t *)(0x6F)) = 0;


    (*(volatile uint16_t *)(0x86)) = ((uint16_t) pwm_div << 4) - 1;;


    (*(volatile uint16_t *)(0x88)) = 0;
    (*(volatile uint16_t *)(0x8A)) = 0;


    (*(volatile uint8_t *)(0x80)) = (0<<7) | (0<<6) |
             (0<<5) | (0<<4) |
             (0<<1) | (0<<0);
    (*(volatile uint8_t *)(0x81)) = (0<<7) | (0<<6) |
             (1<<4) | (0<<3) |
             (0<<2) | (0<<1) | (1<<0);


    registers_write_byte(0x0E, 0);
    registers_write_byte(0x0F, 0);
}


void pwm_update(uint16_t position, int16_t pwm)






{
    uint8_t pwm_width;
    uint16_t min_position;
    uint16_t max_position;






    if (registers_read_word(0x28, 0x29) != pwm_div)
    {

        (*(volatile uint8_t *)(0x80)) &= ~((1<<7) | (1<<6));
        (*(volatile uint8_t *)(0x80)) &= ~((1<<5) | (1<<4));


        (*(volatile uint8_t *)((0x05) + 0x20)) &= ~((1<<1) | (1<<2));

        delay_loop(8);


        pwm_a = 0;
        pwm_b = 0;


        pwm_div = registers_read_word(0x28, 0x29);


        (*(volatile uint16_t *)(0x86)) = ((uint16_t) pwm_div << 4) - 1;;


        (*(volatile uint16_t *)(0x84)) = 0;
        (*(volatile uint16_t *)(0x88)) = 0;
        (*(volatile uint16_t *)(0x8A)) = 0;
    }


    if (registers_read_byte(0x2E) != 0)
    {



        min_position = registers_read_word(0x2C, 0x2D);
        max_position = registers_read_word(0x2A, 0x2B);


        if (min_position > 0x3ff) min_position = 0x3ff;
        if (max_position > 0x3ff) max_position = 0x3ff;


        min_position = 0x3ff - min_position;
        max_position = 0x3ff - max_position;
    }
    else
    {



        min_position = registers_read_word(0x2A, 0x2B);
        max_position = registers_read_word(0x2C, 0x2D);


        if (min_position > 0x3ff) min_position = 0x3ff;
        if (max_position > 0x3ff) max_position = 0x3ff;
    }


    if ((position < min_position) && (pwm < 0)) pwm = 0;


    if ((position > max_position) && (pwm > 0)) pwm = 0;


    if (!(registers_read_byte(0x05) & (1<<0x00))) pwm = 0;


    if (pwm < 0)
    {



        pwm_width = (uint8_t) -pwm;





        pwm_dir_b(pwm_width);

    }
    else if (pwm > 0)
    {



        pwm_width = (uint8_t) pwm;





        pwm_dir_a(pwm_width);


    }
    else
    {

        pwm_stop();
    }
}


void pwm_stop(void)

{

    __asm__ __volatile__ ("cli" ::);


    if (pwm_a || pwm_b)
    {

        (*(volatile uint8_t *)(0x80)) &= ~((1<<7) | (1<<6));
        (*(volatile uint8_t *)(0x80)) &= ~((1<<5) | (1<<4));


        (*(volatile uint8_t *)((0x05) + 0x20)) &= ~((1<<1) | (1<<2));

        delay_loop(8);


        pwm_a = 0;
        pwm_b = 0;
    }


    (*(volatile uint16_t *)(0x88)) = 0;
    (*(volatile uint16_t *)(0x8A)) = 0;


    __asm__ __volatile__ ("sei" ::);


    registers_write_byte(0x0E, pwm_a);
    registers_write_byte(0x0F, pwm_b);
}
