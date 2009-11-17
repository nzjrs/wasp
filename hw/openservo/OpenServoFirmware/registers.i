# 1 "registers.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "registers.c"
# 27 "registers.c"
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
# 28 "registers.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/string.h" 1 3
# 45 "c:/winavr-20070525/bin/../avr/include/string.h" 3
# 1 "c:\\winavr-20070525\\bin\\../lib/gcc/avr/4.1.2/include/stddef.h" 1 3 4
# 214 "c:\\winavr-20070525\\bin\\../lib/gcc/avr/4.1.2/include/stddef.h" 3 4
typedef unsigned int size_t;
# 46 "c:/winavr-20070525/bin/../avr/include/string.h" 2 3
# 106 "c:/winavr-20070525/bin/../avr/include/string.h" 3
extern int ffs (int) __attribute__((const));
extern int ffsl (long) __attribute__((const));
extern int ffsll (long long) __attribute__((const));
extern void *memccpy(void *, const void *, int, size_t);
extern void *memchr(const void *, int, size_t) __attribute__((__pure__));
extern int memcmp(const void *, const void *, size_t) __attribute__((__pure__));
extern void *memcpy(void *, const void *, size_t);
extern void *memmem(const void *, size_t, const void *, size_t) __attribute__((__pure__));
extern void *memmove(void *, const void *, size_t);
extern void *memrchr(const void *, int, size_t) __attribute__((__pure__));
extern void *memset(void *, int, size_t);
extern char *strcat(char *, const char *);
extern char *strchr(const char *, int) __attribute__((__pure__));
extern char *strchrnul(const char *, int) __attribute__((__pure__));
extern int strcmp(const char *, const char *) __attribute__((__pure__));
extern char *strcpy(char *, const char *);
extern int strcasecmp(const char *, const char *) __attribute__((__pure__));
extern char *strcasestr(const char *, const char *) __attribute__((__pure__));
extern size_t strcspn(const char *s, const char *reject) __attribute__((__pure__));
extern size_t strlcat(char *, const char *, size_t);
extern size_t strlcpy(char *, const char *, size_t);
extern size_t strlen(const char *) __attribute__((__pure__));
extern char *strlwr(char *);
extern char *strncat(char *, const char *, size_t);
extern int strncmp(const char *, const char *, size_t) __attribute__((__pure__));
extern char *strncpy(char *, const char *, size_t);
extern int strncasecmp(const char *, const char *, size_t) __attribute__((__pure__));
extern size_t strnlen(const char *, size_t) __attribute__((__pure__));
extern char *strpbrk(const char *s, const char *accept) __attribute__((__pure__));
extern char *strrchr(const char *, int) __attribute__((__pure__));
extern char *strrev(char *);
extern char *strsep(char **, const char *);
extern size_t strspn(const char *s, const char *accept) __attribute__((__pure__));
extern char *strstr(const char *, const char *) __attribute__((__pure__));
extern char *strtok_r(char *, const char *, char **);
extern char *strupr(char *);
# 29 "registers.c" 2

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
# 31 "registers.c" 2
# 1 "config.h" 1
# 32 "registers.c" 2
# 1 "eeprom.h" 1
# 37 "eeprom.h"
uint8_t eeprom_erase(void);
uint8_t eeprom_restore_registers(void);
uint8_t eeprom_save_registers(void);
# 33 "registers.c" 2
# 1 "estimator.h" 1
# 32 "estimator.h"
void estimator_init(void);


void estimator_registers_defaults(void);




void estimate_velocity(int16_t position);
# 34 "registers.c" 2
# 1 "ipd.h" 1
# 31 "ipd.h"
void ipd_init(void);


void ipd_registers_defaults(void);



int16_t ipd_position_to_pwm(int16_t position);
# 35 "registers.c" 2
# 1 "pid.h" 1
# 31 "pid.h"
void pid_init(void);


void pid_registers_defaults(void);



int16_t pid_position_to_pwm(int16_t position);
# 36 "registers.c" 2
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
# 37 "registers.c" 2
# 1 "regulator.h" 1
# 31 "regulator.h"
void regulator_init(void);


void regulator_registers_defaults(void);



int16_t regulator_position_to_pwm(int16_t position);
# 38 "registers.c" 2



uint8_t registers[(0x38 + 16)];

void registers_init(void)

{

    memset(&registers[0], 0, (0x38 + 16));


    registers_write_byte(0x00, 1);
    registers_write_byte(0x01, 1);
    registers_write_byte(0x02, 0);
    registers_write_byte(0x03, 2);




    if (!eeprom_restore_registers())
    {

        memset(&registers[0x20], (0x37 - 0x20 + 1) + (0x6F - 0x60 + 1), (0x38 + 16));


        registers_defaults();
    }
}


void registers_defaults(void)

{



    registers_write_byte(0x20, 0x10);


    pwm_registers_defaults();
# 94 "registers.c"
    pid_registers_defaults();






}


uint16_t registers_read_word(uint8_t address_hi, uint8_t address_lo)


{
    uint8_t sreg;
    uint16_t value;



    asm volatile ("in %0,__SREG__\n\tcli\n\t" : "=&r" (sreg));


    value = (registers[address_hi] << 8) | registers[address_lo];


    asm volatile ("out __SREG__,%0\n\t" : : "r" (sreg));

    return value;
}


void registers_write_word(uint8_t address_hi, uint8_t address_lo, uint16_t value)


{
    uint8_t sreg;


    asm volatile ("in %0,__SREG__\n\tcli\n\t" : "=&r" (sreg));


    registers[address_hi] = value >> 8;
    registers[address_lo] = value;


    asm volatile ("out __SREG__,%0\n\t" : : "r" (sreg));
}
