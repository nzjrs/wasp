#include "std.h"
#include "config/config.h"
#include "generated/settings.h"

#include "analog.h"
#include "arm7/armVIC.h"
#include "arm7/sys_time_hw.h"
#include "arm7/led_hw.h"

#if USE_ANALOG_BARO
#include "arm7/altimeter_analog_baro_hw.h"
#endif

typedef struct {
    volatile adcRegs_t          *adc_reg;
    volatile uint8_t            selection_mask;
    AnalogChannel_t             channel;
}   AdcChannel_t;

static volatile AdcChannel_t    adc_channels[ANALOG_CHANNEL_NUM];
static volatile AnalogChannel_t adc_current_channel;
static volatile AnalogChannel_t used_channels;
static volatile uint16_t        adc_values[ANALOG_CHANNEL_NUM];

#define CONVERSION_COMPLETE(_reg)           (_reg & 0x80000000)
#define SELECT_ONLY_CHANNEL(_reg, _mask)    \
    _reg &= 0xFFFFFF00;                     \
    _reg |= _mask;

// battery on AD0.2 on P0.29
// pressure on AD1.2 on P0.10
// adc_spare on AD1.4 on P0.13

void analog_init(void)
{
    uint8_t i;

    for (i = 0; i < ANALOG_CHANNEL_NUM; i++) {
        volatile AdcChannel_t *a = &adc_channels[i];
        a->adc_reg = NULL;
        a->selection_mask = 0;
        a->channel = 0;

        adc_values[i] = 0xFFFF;
    }

    adc_current_channel = 0;
    used_channels = 0;

    /* turn off and reset ADC. It is configured and enabled
    in analog_enable_channel */
    AD0CR = 0;
    AD1CR = 0;
}

void
analog_enable_channel(AnalogChannel_t channel)
{
    volatile adcRegs_t *adc_reg;
    uint8_t selection_mask;

    switch (channel)
    {
        case ANALOG_CHANNEL_BATTERY:
            ANALOG_BATT_PINSEL |= ANALOG_BATT_PINSEL_VAL << ANALOG_BATT_PINSEL_BIT;
            /* PCLK/4 (3.75MHz) | PDN=1 (ADC Operational) */
            AD0CR |= (0x03 << 8) | (1 << 21);
            adc_reg = ADC0;
            /* select AD0.2 */
            selection_mask = (1 << 2);
            break;
        case ANALOG_CHANNEL_ADC_SPARE:
            ANALOG_SPARE_PINSEL |= ANALOG_SPARE_PINSEL_VAL << ANALOG_SPARE_PINSEL_BIT;
            /* PCLK/4 (3.75MHz) | PDN=1 (ADC Operational) */
            AD1CR |= (0x03 << 8) | (1 << 21);
            adc_reg = ADC1;
            /* select AD1.4 */
            selection_mask = (1 << 4);
            break;
#if USE_ANALOG_BARO
        case ANALOG_CHANNEL_PRESSURE:
            ANALOG_BARO_PINSEL |=  ANALOG_BARO_PINSEL_VAL << ANALOG_BARO_PINSEL_BIT;
            /* PCLK/4 (3.75MHz) | PDN=1 (ADC Operational) */
            AD1CR |= (0x03 << 8) | (1 << 21);
            adc_reg = ADC1;
            /* select AD1.2 */
            selection_mask = (1 << 2);
            break;
#endif
        default:
            return;
            break;
    }

    /* mark the channel as used */
    adc_channels[used_channels].adc_reg = adc_reg;
    adc_channels[used_channels].selection_mask = selection_mask;
    adc_channels[used_channels].channel = channel;

    /* select current channel */
    adc_current_channel = used_channels;
    used_channels += 1;

    SELECT_ONLY_CHANNEL(adc_reg->cr, selection_mask);

    /* start a conversion */
    adc_reg->cr |= (0x1 << 24);
    
}

uint16_t analog_read_channel( AnalogChannel_t channel )
{
    switch (channel)
    {
        case ANALOG_CHANNEL_BATTERY:
        case ANALOG_CHANNEL_PRESSURE:
        case ANALOG_CHANNEL_ADC_SPARE:
            return adc_values[channel];
        default:
            return 0;
    }
}

uint8_t analog_read_battery( void )
{
    uint32_t v = 0;

    /* BATTERY_SENS converts ADC bits to volts. But this function
    returns the result in decivolts, so we need to multiply by 10 more.
    Multiplication by 10 is equiv. to dividing the denominator by 10 */
    v = ((uint32_t)(adc_values[ANALOG_CHANNEL_BATTERY]) * ANALOG_BATTERY_SENS_NUM) / (ANALOG_BATTERY_SENS_DEN / 10);

    return (uint8_t)v;
}

bool_t analog_event_task( void )
{
    volatile AdcChannel_t *channel;
    uint32_t r;

    if (used_channels == 0)
        return FALSE;

    /* select current channel */
    channel = &adc_channels[adc_current_channel];

    /* data to be read on current channel */
    if ( CONVERSION_COMPLETE(channel->adc_reg->gdr) ) {
        r = channel->adc_reg->gdr;
        adc_values[channel->channel] = (r >> 6) & 0x03FF;
    }

    /* select the next channel */
    adc_current_channel = (adc_current_channel + 1) % used_channels;
    channel = &adc_channels[adc_current_channel];

    SELECT_ONLY_CHANNEL(channel->adc_reg->cr, channel->selection_mask);

    /* start the conversion */
    channel->adc_reg->cr |= (0x1 << 24);

    /* return TRUE when all relevant DONE bits are set in AD0STAT and AD1STAT */
    return TRUE;
}

void analog_periodic_task( void )
{
#if USE_ANALOG_BARO
    booz2_analog_baro_isr(adc_values[ANALOG_CHANNEL_PRESSURE]);
#endif
}

