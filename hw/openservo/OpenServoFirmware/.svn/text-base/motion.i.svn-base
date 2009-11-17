# 1 "motion.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "motion.c"
# 27 "motion.c"
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
# 28 "motion.c" 2

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
# 30 "motion.c" 2
# 1 "config.h" 1
# 31 "motion.c" 2
# 1 "curve.h" 1
# 33 "curve.h"
extern uint16_t curve_t0;
extern uint16_t curve_t1;
extern uint16_t curve_duration;


extern float curve_p0;
extern float curve_p1;
extern float curve_v0;
extern float curve_v1;


void curve_init(uint16_t t0, uint16_t t1, float p0, float p1, float v0, float v1);
void curve_solve(uint16_t t, float *x, float *dx);


inline static uint16_t curve_get_t0(void) { return curve_t0; }
inline static uint16_t curve_get_t1(void) { return curve_t1; }
inline static uint16_t curve_get_duration(void) { return curve_duration; }
inline static float curve_get_p0(void) { return curve_p0; }
inline static float curve_get_p1(void) { return curve_p1; }
inline static float curve_get_v0(void) { return curve_v0; }
inline static float curve_get_v1(void) { return curve_v1; }
# 32 "motion.c" 2
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
# 33 "motion.c" 2





typedef struct motion_key
{
    uint16_t delta;
    float position;
    float in_velocity;
    float out_velocity;
} motion_key;



uint8_t motion_head;
uint8_t motion_tail;
uint32_t motion_counter;
uint32_t motion_duration;


static motion_key keys[8];

static float int_to_float(int16_t a)

{
    return (float) a;
}


static int16_t float_to_int(float a)

{
    return (int16_t) (a + 0.5);
}


static float fixed_to_float(int16_t a)

{
    return ((float) a) / 1024.0;
}
# 86 "motion.c"
void motion_init(void)

{

    motion_counter = 0;


    motion_duration = 0;


    motion_head = 0;
    motion_tail = 0;


    keys[0].delta = 0;
    keys[0].position = 512.0;
    keys[0].in_velocity = 0.0;
    keys[0].out_velocity = 0.0;


    curve_init(0, 0, 512.0, 512.0, 0.0, 0.0);


    motion_registers_reset();
}


void motion_reset(int16_t position)

{

    motion_counter = 0;


    motion_duration = 0;


    motion_head = 0;
    motion_tail = 0;


    keys[0].delta = 0;
    keys[0].position = int_to_float(position);
    keys[0].in_velocity = 0.0;
    keys[0].out_velocity = 0.0;



    curve_init(0, 0, keys[0].position, keys[0].position, 0.0, 0.0);


    motion_registers_reset();
}


void motion_registers_reset(void)

{

    registers_write_word(0x1A, 0x1B, 0);
    registers_write_word(0x1C, 0x1D, 0);
    registers_write_word(0x1E, 0x1F, 0);
    registers_write_word(0x18, 0x19, 0);


    registers_write_byte(0x16, 0);
    registers_write_byte(0x17, motion_buffer_left());
}


uint8_t motion_append(void)




{
    int16_t position;
    int16_t in_velocity;
    int16_t out_velocity;
    uint8_t next;
    uint16_t delta;


    next = (motion_head + 1) & (8 - 1);


    if (next == motion_tail) return 0;


    position = (int16_t) registers_read_word(0x1A, 0x1B);
    in_velocity = (int16_t) registers_read_word(0x1C, 0x1D);
    out_velocity = (int16_t) registers_read_word(0x1E, 0x1F);
    delta = (uint16_t) registers_read_word(0x18, 0x19);


    if (delta < 1) return 0;


    keys[next].delta = delta;
    keys[next].position = int_to_float(position);
    keys[next].in_velocity = fixed_to_float(in_velocity);
    keys[next].out_velocity = fixed_to_float(out_velocity);


    if (motion_tail == motion_head)
    {


        curve_init(0, delta, curve_get_p1(), keys[next].position, 0.0, 0.0);
    }


    motion_duration += delta;


    motion_head = next;


    motion_registers_reset();

    return 1;
}


void motion_next(uint16_t delta)



{
    float fposition;
    float fvelocity;


    if (!(registers_read_byte(0x05) & (1<<0x02))) return;


    if (motion_tail == motion_head)
    {

        motion_counter = 0;
        motion_duration = 0;
    }
    else
    {

        motion_counter += delta;


        while (motion_counter > curve_get_duration())
        {

            motion_counter -= curve_get_duration();


            motion_duration -= curve_get_duration();


            motion_tail = (motion_tail + 1) & (8 - 1);


            if (motion_tail == motion_head)
            {


                curve_init(0, 0, keys[motion_head].position, keys[motion_head].position, 0.0, 0.0);


                motion_counter = 0;
                motion_duration = 0;
            }
            else
            {
                uint8_t curr_point;
                uint8_t next_point;


                curr_point = motion_tail;
                next_point = (curr_point + 1) & (8 - 1);


                curve_init(0, keys[next_point].delta,
                           keys[curr_point].position, keys[next_point].position,
                           keys[curr_point].out_velocity, keys[next_point].in_velocity);
            }


            registers_write_byte(0x17, motion_buffer_left());
        }
    }


    curve_solve(motion_counter, &fposition, &fvelocity);




    fvelocity *= 10.0;


    registers_write_word(0x10, 0x11, float_to_int(fposition));


    registers_write_word(0x12, 0x13, float_to_int(fvelocity));
}


uint8_t motion_buffer_left(void)


{
    uint8_t space_left;


    if (motion_head < motion_tail)
    {
        space_left = (8 - 1) - (8 + motion_head - motion_tail);
    }
    else
    {
        space_left = (8 - 1) - (motion_head - motion_tail);
    }

    return space_left;
}
