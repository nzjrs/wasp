# 1 "curve.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "curve.c"
# 27 "curve.c"
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
# 28 "curve.c" 2

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
# 30 "curve.c" 2
# 1 "config.h" 1
# 31 "curve.c" 2
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
# 32 "curve.c" 2




uint16_t curve_t0;
uint16_t curve_t1;
uint16_t curve_duration;
static float curve_duration_float;


float curve_p0;
float curve_p1;
float curve_v0;
float curve_v1;


static float curve_a;
static float curve_b;
static float curve_c;
static float curve_d;

void curve_init(uint16_t t0, uint16_t t1, float p0, float p1, float v0, float v1)
{

    curve_t0 = t0;
    curve_t1 = t1;
    curve_duration = t1 - t0;
    curve_duration_float = (float) curve_duration;




    v0 *= curve_duration_float;
    v1 *= curve_duration_float;


    curve_p0 = p0;
    curve_p1 = p1;
    curve_v0 = v0;
    curve_v1 = v1;
# 86 "curve.c"
    curve_a = (2.0 * p0) - (2.0 * p1) + v0 + v1;
    curve_b = -(3.0 * p0) + (3.0 * p1) - (2.0 * v0) - v1;
    curve_c = v0;
    curve_d = p0;
}


void curve_solve(uint16_t t, float *x, float *dx)
{

    if (t <= curve_t0)
    {

        *x = curve_p0;
        *dx = t < curve_t0 ? 0.0 : curve_v0;
    }
    else if (t >= curve_t1)
    {

        *x = curve_p1;
        *dx = t > curve_t1 ? 0.0 : curve_v1;
    }
    else
    {

        float t1 = ((float) (t - curve_t0)) / curve_duration_float;
        float t2 = t1 * t1;
        float t3 = t2 * t1;



        *x = (curve_a * t3) + (curve_b * t2) + (curve_c * t1) + curve_d;



        *dx = (3.0 * curve_a * t2) + (2.0 * curve_b * t1) + curve_c;



        *dx /= curve_duration_float;
    }
}
