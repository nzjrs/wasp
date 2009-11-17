# 1 "math.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "math.c"
# 27 "math.c"
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
# 28 "math.c" 2

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
# 30 "math.c" 2
# 1 "config.h" 1
# 31 "math.c" 2
# 1 "math.h" 1
# 30 "math.h"
static inline int16_t shift_right16(int16_t val, uint8_t cnt)

{
    asm volatile (
        "L_asr1%=:" "\n\t"
        "cp %1,__zero_reg__" "\n\t"
        "breq L_asr2%=" "\n\t"
        "dec %1" "\n\t"
        "asr %B0" "\n\t"
        "ror %A0" "\n\t"
        "rjmp L_asr1%=" "\n\t"
        "L_asr2%=:" "\n\t"
        : "=&r" (val)
        : "r" (cnt), "0" (val)
        );

    return val;
}

static inline int32_t shift_right32(int32_t val, uint8_t cnt)

{
    asm volatile (
        "L_asr1%=:" "\n\t"
        "cp %1,__zero_reg__" "\n\t"
        "breq L_asr2%=" "\n\t"
        "dec %1" "\n\t"
        "asr %D0" "\n\t"
        "ror %C0" "\n\t"
        "ror %B0" "\n\t"
        "ror %A0" "\n\t"
        "rjmp L_asr1%=" "\n\t"
        "L_asr2%=:" "\n\t"
        : "=&r" (val)
        : "r" (cnt), "0" (val)
        );

    return val;
}
# 32 "math.c" 2
