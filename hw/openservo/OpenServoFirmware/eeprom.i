# 1 "eeprom.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "eeprom.c"
# 27 "eeprom.c"
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
# 28 "eeprom.c" 2
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
# 29 "eeprom.c" 2
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
# 30 "eeprom.c" 2
# 1 "c:/winavr-20070525/bin/../avr/include/avr/eeprom.h" 1 3
# 49 "c:/winavr-20070525/bin/../avr/include/avr/eeprom.h" 3
# 1 "c:\\winavr-20070525\\bin\\../lib/gcc/avr/4.1.2/include/stddef.h" 1 3 4
# 50 "c:/winavr-20070525/bin/../avr/include/avr/eeprom.h" 2 3
# 128 "c:/winavr-20070525/bin/../avr/include/avr/eeprom.h" 3
static inline uint8_t __attribute__ ((always_inline))
eeprom_read_byte (const uint8_t *addr);

static inline uint16_t __attribute__ ((always_inline))
eeprom_read_word (const uint16_t *addr);

static inline void __attribute__ ((always_inline))
eeprom_read_block (void *pointer_ram,
                   const void *pointer_eeprom,
                   size_t size);

static inline void __attribute__ ((always_inline))
eeprom_write_byte (uint8_t *addr,uint8_t value);

static inline void __attribute__ ((always_inline))
eeprom_write_word (uint16_t *addr,uint16_t value);

static inline void __attribute__ ((always_inline))
eeprom_write_block (const void *pointer_ram,
                    void *pointer_eeprom,
                    size_t size);
# 189 "c:/winavr-20070525/bin/../avr/include/avr/eeprom.h" 3
uint8_t
eeprom_read_byte (const uint8_t *addr)
{
  uint8_t result;
  __asm__ __volatile__
      ( "call" " __eeprom_read_byte_" "1F2021" "\n\t"
        "mov %1,__tmp_reg__"
       : "+x" (addr),
         "=r" (result)
       : );
  return result;
}



uint16_t
eeprom_read_word (const uint16_t *addr)
{
  uint16_t result;

  __asm__ __volatile__ (
        "call" " __eeprom_read_word_" "1F2021" "\n\t"
       : "+x" (addr),
         "=z" (result)
       : );
  return result;
}







void
eeprom_read_block (void *pointer_ram,
                   const void *pointer_eeprom,
                   size_t n)
{
  if (!__builtin_constant_p (n)
      || n > 256)
    {

      uint16_t size = n;

      __asm__ __volatile__ (
            ".%=_start:" "\n\t"
            "sbiw %2,1" "\n\t"
            "brlt .%=_finished" "\n\t"
             "call" " __eeprom_read_byte_" "1F2021" "\n\t"
            "st z+,__tmp_reg__" "\n\t"
            "rjmp .%=_start" "\n\t"
            ".%=_finished:"
          : "=x" (pointer_eeprom),
            "=z" (pointer_ram),
            "+w" (size)
           : "x" (pointer_eeprom),
             "z" (pointer_ram)
           : "memory");
    }
  else
    {
      if (n != 0)
        {
          if (n == 256)
            {
              __asm__ __volatile__ (
                  "call" " __eeprom_read_block_" "1F2021"
                : "+x" (pointer_eeprom),
                  "=z" (pointer_ram)
                : "z" (pointer_ram)
                : "memory");
            }
          else
            {

              uint8_t len;
              len = (uint8_t) n;

              __asm__ __volatile__ (
                  "mov __zero_reg__,%2" "\n\t"
                   "call" " __eeprom_read_block_" "1F2021"
                : "+x" (pointer_eeprom),
                  "=z" (pointer_ram)
                : "r" (len),
                  "z" (pointer_ram)
                : "memory");
            }
        }
    }
}




void
eeprom_write_byte (uint8_t *addr,uint8_t value)
{
  __asm__ __volatile__ (
         "mov __tmp_reg__,%1" "\n\t"
         "call" " __eeprom_write_byte_" "1F2021"
       : "+x" (addr)
       : "r" (value)
       : "memory"
      );
}




void
eeprom_write_word (uint16_t *addr,uint16_t value)
{
  __asm__ __volatile__ (

         "movw __tmp_reg__,%A1" "\n\t"




          "call" " __eeprom_write_word_" "1F2021" "\n\t"
       : "+x" (addr)
       : "r" (value)
       : "memory"
      );
}





void
eeprom_write_block (const void *pointer_ram,
                    void *pointer_eeprom,
                    size_t n)
{
  if (!__builtin_constant_p (n)
      || n > 256)
    {

      uint16_t size = n;

      __asm__ __volatile__ (
            ".%=_start:" "\n\t"
            "sbiw %2,1" "\n\t"
            "brlt .%=_finished" "\n\t"
            "ld __tmp_reg__,z+" "\n\t"
             "call" " __eeprom_write_byte_" "1F2021" "\n\t"
            "rjmp .%=_start" "\n\t"
            ".%=_finished:"
          : "=x" (pointer_eeprom),
            "=z" (pointer_ram),
            "+w" (size)
           : "x" (pointer_eeprom),
             "z" (pointer_ram)
           : "memory");
    }
  else
    {

      if (n != 0)
        {
          if (n == 256)
            {
              __asm__ __volatile__ (
                 "call" " __eeprom_write_block_" "1F2021"
               : "+x" (pointer_eeprom),
                 "=z" (pointer_ram)
               : "z" (pointer_ram)
               : "memory" );
            }
          else
            {
              uint8_t len;
              len = (uint8_t) n;

              __asm__ __volatile__ (
                 "mov __zero_reg__,%2" "\n\t"
                 "call" " __eeprom_write_block_" "1F2021"
               : "+x" (pointer_eeprom),
                 "=z" (pointer_ram)
               : "r" (len),
                 "z" (pointer_ram)
               : "memory" );
            }

        }
    }
}
# 31 "eeprom.c" 2

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
# 33 "eeprom.c" 2
# 1 "config.h" 1
# 34 "eeprom.c" 2
# 1 "eeprom.h" 1
# 37 "eeprom.h"
uint8_t eeprom_erase(void);
uint8_t eeprom_restore_registers(void);
uint8_t eeprom_save_registers(void);
# 35 "eeprom.c" 2
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
# 36 "eeprom.c" 2

static uint8_t eeprom_checksum(const uint8_t *buffer, size_t size, uint8_t sum)

{

    while (size)
    {

        sum += *buffer;


        ++buffer;
        --size;
    }


    return sum;
}


uint8_t eeprom_erase(void)

{
    uint16_t i;
    uint8_t buffer[16];




    memset(buffer, 0xFF, sizeof(buffer));


    for (i = 0; i < 0x1FF; i += sizeof(buffer))
    {

        eeprom_write_block(buffer, (void *) i, sizeof(buffer));
    }




    return 1;
}


uint8_t eeprom_restore_registers(void)


{
    uint8_t header[2];




    eeprom_read_block(&header[0], (void *) 0, 2);


    if (header[0] != 0x03) return 0;


    eeprom_read_block(&registers[0x20], (void *) 2, (0x37 - 0x20 + 1) + (0x6F - 0x60 + 1));


    if (header[1] != eeprom_checksum(&registers[0x20], (0x37 - 0x20 + 1) + (0x6F - 0x60 + 1), 0x03)) return 0;




    return 1;
}


uint8_t eeprom_save_registers(void)

{
    uint8_t header[2];




    header[0] = 0x03;
    header[1] = eeprom_checksum(&registers[0x20], (0x37 - 0x20 + 1) + (0x6F - 0x60 + 1), 0x03);


    eeprom_write_block(&header[0], (void *) 0, 2);


    eeprom_write_block(&registers[0x20], (void *) 2, (0x37 - 0x20 + 1) + (0x6F - 0x60 + 1));




    return 1;
}
