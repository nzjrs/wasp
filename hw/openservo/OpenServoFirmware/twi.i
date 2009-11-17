# 1 "twi.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "twi.c"
# 27 "twi.c"
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
# 28 "twi.c" 2
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
# 29 "twi.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/avr/interrupt.h" 1 3
# 30 "twi.c" 2

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
# 32 "twi.c" 2
# 1 "config.h" 1
# 33 "twi.c" 2
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
# 34 "twi.c" 2
# 1 "twi.h" 1
# 93 "twi.h"
void twi_slave_init(uint8_t);
uint8_t twi_receive_byte(void);
uint8_t twi_data_in_receive_buffer(void);
# 35 "twi.c" 2
# 97 "twi.c"
static volatile uint8_t twi_address;
static volatile uint8_t twi_data_state;
static volatile uint8_t twi_overflow_state;

static volatile uint8_t twi_rxhead;
static volatile uint8_t twi_rxtail;
static uint8_t twi_rxbuf[(4)];


static uint8_t twi_chk_count;
static uint8_t twi_chk_count_target;
static uint8_t twi_chk_sum;
static uint8_t twi_chk_write_buffer[(16)];


static uint8_t twi_registers_read(uint8_t address)



{

    address &= 0x7F;


    if (address <= 0x37)
    {

        return registers_read_byte(address);
    }


    if (address <= 0x5F)
    {

        return 0;
    }


    if (address <= 0x6F)
    {

        return registers_read_byte(address - (0x60 - 0x38));
    }


    if (address <= 0x7F)
    {

        address = 0x60 + (address - 0x70);


        address = registers_read_byte(address - (0x60 - 0x38));


        if (address <= 0x6F)
        {

            return twi_registers_read(address);
        }
    }


    return 0;
}


static void twi_registers_write(uint8_t address, uint8_t data)



{

    address &= 0x7F;


    if (address <= 0x0F)
    {

        return;
    }


    if (address <= 0x1F)
    {

        registers_write_byte(address, data);

        return;
    }


    if (registers_is_write_disabled())
    {

        return;
    }


    if (address <= 0x37)
    {

        registers_write_byte(address, data);

        return;
    }


    if (address <= 0x5F)
    {

        return;
    }



    if (address <= 0x6F)
    {

        registers_write_byte(address - (0x60 - 0x38), data);

        return;
    }


    if (address <= 0x7F)
    {

        address = 0x60 + (address - 0x70);


        address = registers_read_byte(address - (0x70 - 0x38));


        if (address <= 0x6F)
        {

            twi_registers_write(address, data);

            return;
        }
    }


    return;
}



static void twi_write_buffer(void)

{

    for (twi_chk_count = 0; twi_chk_count < twi_chk_count_target; twi_chk_count++)
    {

        twi_registers_write(twi_address, twi_chk_write_buffer[twi_chk_count & ((16) - 1)]);


        ++twi_address;
    }
}



static uint8_t twi_read_data()

{

    uint8_t data = twi_registers_read(twi_address);



    if (twi_data_state == (0x04))
    {

        if (twi_chk_count < twi_chk_count_target)
        {

            twi_chk_sum += data;


            ++twi_chk_count;


            ++twi_address;
        }
        else
        {

            data = twi_chk_sum;
        }
    }
    else
    {

        ++twi_address;
    }





    return data;
}


static uint8_t twi_write_data(uint8_t data)

{

    uint8_t ack = (0x00);


    switch (twi_data_state)
    {
        case (0x00):


            if (data < 0x80)
            {

                twi_address = data;


                twi_data_state = (0x01);
            }

            else if (data == 0x81)
            {

                twi_data_state = (0x02);
            }

            else
            {

                twi_rxhead = (twi_rxhead + 1) & ((4) - 1);
                twi_rxbuf[twi_rxhead] = data;
            }

            break;

        case (0x01):


            twi_registers_write(twi_address, data);


            ++twi_address;

            break;


        case (0x02):



            twi_chk_sum = twi_chk_count_target = data & ((16) - 1);


            twi_chk_count = 0;


            twi_data_state = (0x03);

            break;

        case (0x03):


            twi_chk_sum += twi_address = data;


            twi_data_state = (0x04);

            break;

        case (0x04):


            if (twi_chk_count < twi_chk_count_target)
            {

                twi_chk_write_buffer[twi_chk_count & ((16) - 1)] = data;


                twi_chk_sum += data;


                ++twi_chk_count;
            }
            else
            {

                if (data == twi_chk_sum)
                {

                    twi_write_buffer();
                }
                else
                {

                    ack = (0x01);
                }
            }

            break;

    }

    return ack;
}


void
twi_slave_init(uint8_t slave_address)

{

    twi_rxtail = 0;
    twi_rxhead = 0;
# 450 "twi.c"
    (*(volatile uint8_t *)(0xBA)) = slave_address << 1;


    (*(volatile uint8_t *)(0xBB)) = 0xFF;


    (*(volatile uint8_t *)(0xBC)) = (1<<2) |
           (1<<0) |
           (0<<5) |
           (0<<4) |
           (1<<7) |
           (1<<6) |
           (0<<3);

}


uint8_t twi_receive_byte(void)

{

    while (twi_rxhead == twi_rxtail);


    twi_rxtail = (twi_rxtail + 1 ) & ((4) - 1);


    return twi_rxbuf[twi_rxtail];
}


uint8_t twi_data_in_receive_buffer(void)

{

    return (twi_rxhead != twi_rxtail);
}
# 667 "twi.c"
void __vector_24 (void) __attribute__ ((signal,used, externally_visible)); void __vector_24 (void)

{
    switch ((*(volatile uint8_t *)(0xB9)))
    {

        case 0xA8:

        case 0xB8:


            (*(volatile uint8_t *)(0xBB)) = twi_read_data();


            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (0<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);
            break;


        case 0xC0:

        case 0xC8:


            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (0<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);
            break;


        case 0x60:


            twi_data_state = (0x00);


            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (0<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);

            break;


        case 0x80:


            twi_write_data((*(volatile uint8_t *)(0xBB)));


            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (0<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);

            break;


        case 0x88:

        case 0xA0:


             (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                    (1<<0) |
                    (0<<5) |
                    (0<<4) |
                    (1<<7) |
                    (1<<6) |
                    (0<<3);

            break;


        case 0x00:



            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (1<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);
            break;


        case 0xF8:


            break;

        default:


            (*(volatile uint8_t *)(0xBC)) = (1<<2) |
                   (1<<0) |
                   (0<<5) |
                   (0<<4) |
                   (1<<7) |
                   (1<<6) |
                   (0<<3);
            break;
    }
}
