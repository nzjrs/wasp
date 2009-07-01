#ifndef _BOOZ_IMU_BABY_H_
#define _BOOZ_IMU_BABY_H_

/* SSPCR0 settings */
//#define SSP_DDS  0x07 << 0  /* data size         : 8 bits        */
#define SSP_DDS  0x0F << 0  /* data size         : 16 bits        */
#define SSP_FRF  0x00 << 4  /* frame format      : SPI           */
#define SSP_CPOL 0x00 << 6  /* clock polarity    : data captured on first clock transition */  
#define SSP_CPHA 0x00 << 7  /* clock phase       : SCK idles low */
#define SSP_SCR  0x0F << 8  /* serial clock rate : divide by 16  */

/* SSPCR1 settings */
#define SSP_LBM  0x00 << 0  /* loopback mode     : disabled                  */
#define SSP_SSE  0x00 << 1  /* SSP enable        : disabled                  */
#define SSP_MS   0x00 << 2  /* master slave mode : master                    */
#define SSP_SOD  0x00 << 3  /* slave output disable : don't care when master */

#define SSPCR0_VAL (SSP_DDS |  SSP_FRF | SSP_CPOL | SSP_CPHA | SSP_SCR )
#define SSPCR1_VAL (SSP_LBM |  SSP_SSE | SSP_MS | SSP_SOD )

#define SSP_PINSEL1_SCK  (2<<2)
#define SSP_PINSEL1_MISO (2<<4)
#define SSP_PINSEL1_MOSI (2<<6)

#define Booz2ImuSetSpi8bits() { \
  SSPCR0 &= (~(0xF << 0)); \
  SSPCR0 |= (0x07 << 0); /* data size : 8 bits */ \
}

#define Booz2ImuSetSpi16bits() { \
  SSPCR0 &= (~(0xF << 0)); \
  SSPCR0 |= (0x0F << 0); /* data size : 16 bits */ \
}

#endif /* _BOOZ_IMU_BABY_H_ */
