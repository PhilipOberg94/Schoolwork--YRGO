/*
* LiquidCrystalI2CDevice.c
*
* Created: 12/9/2018 11:35:38 AM
*  Author: Barrett
*/

#include "i2c_master.h"
#include "liquid_crystal_i2c.h"

#include <avr/io.h>
#include <util/delay.h>

LiquidCrystalDevice_t lq_init(uint16_t address, uint8_t columns, uint8_t rows, uint8_t dotSize)
{
    LiquidCrystalDevice_t device;

    device.Address = address;
    device.Columns = columns;
    device.Rows = rows;
    device.Backlight = LCD_NOBACKLIGHT;
    device.DisplayFunction = LCD_4BITMODE | LCD_1LINE | dotSize;
    device.DisplayControl = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF;

    // Initialize to default text direction (for roman languages)
    device.DisplayMode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT;

    if (rows > 1) {
        device.DisplayFunction |= LCD_2LINE;
    }

    // for some 1 line displays you can select a 10 pixel high font
    if ((dotSize != 0) && (rows == 1)) {
        device.DisplayFunction |= LCD_5x10DOTS;
    }

    // SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
    // according to datasheet, we need at least 40ms after power rises above 2.7V
    // before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
    _delay_ms(100);
    
    // Now we pull both RS and R/W low to begin commands
    lq_transmitI2C(&device, LCD_NOBACKLIGHT);	// reset expanderand turn backlight off (Bit 8 =1)
    _delay_ms(1000);

    //put the LCD into 4 bit mode
    // this is according to the hitachi HD44780 datasheet
    // figure 24, pg 46
    
    // we start in 8bit mode, try to set 4 bit mode
    lq_transmitI2C(&device, 0x03 << 4);
    _delay_us(4500); // wait min 4.1ms
    
    // second try
    lq_writeDevice4Bits(&device, 0x03 << 4);
    _delay_us(4500); // wait min 4.1ms
    
    // third go!
    lq_writeDevice4Bits(&device, 0x03 << 4);
    _delay_us(150); // wait min 150 mics
    
    // finally, set to 4-bit interface
    lq_writeDevice4Bits(&device, 0x02 << 4);

    // set # lines, font size, etc.
    lq_sendCommand(&device, LCD_FUNCTIONSET | device.DisplayFunction);
    
    // turn the display on with no cursor or blinking default
    lq_turnOnDisplay(&device);
    
    // clear it off
    lq_clear(&device);
    
    // set the entry mode
    lq_sendCommand(&device, LCD_ENTRYMODESET | device.DisplayMode);
    
    lq_returnHome(&device);

    return device;
};

void lq_print(struct LiquidCrystalDevice_t* device, char * value)
{
    char letter = *value;

    while(letter != 0x00)
    {
        lq_writeDeviceByte(device, letter, LCD_REGISTER_SELECT_BIT);
        letter = *(++value);
    }
};

void lq_turnOnBacklight(struct LiquidCrystalDevice_t* device)
{
    device->Backlight = LCD_BACKLIGHT;
    lq_transmitI2C(device, 0);
}

void lq_turnOffBacklight(struct LiquidCrystalDevice_t* device)
{
    device->Backlight = LCD_NOBACKLIGHT;
    lq_transmitI2C(device, 0);
}

void lq_clear(LiquidCrystalDevice_t* device)
{
    lq_sendCommand(device, LCD_CLEARDISPLAY); // clear display, set cursor position to zero
    _delay_us(2000);  // this command takes a long time!

    lq_setCursor(device, 0, 0);
}

void lq_setCursor(LiquidCrystalDevice_t* device, uint8_t row, uint8_t column)
{
    uint8_t row_offsets[] = { 0x00, 0x40, 0x14, 0x54 };

    lq_sendCommand(device, LCD_SETDDRAMADDR | (column + row_offsets[row]));
}

void lq_returnHome(LiquidCrystalDevice_t* device)
{
    lq_sendCommand(device, LCD_RETURNHOME);  // set cursor position to zero
    _delay_us(2000);  // this command takes a long time!
};

void lq_turnOnDisplay(LiquidCrystalDevice_t* device)
{
    device->DisplayControl |= LCD_DISPLAYON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
};

void lq_turnOffDisplay(LiquidCrystalDevice_t* device)
{
    device->DisplayControl &= ~LCD_DISPLAYON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
};

void lq_turnOnCursor(struct LiquidCrystalDevice_t* device)
{
    device->DisplayControl |= LCD_CURSORON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
}

void lq_turnOffCursor(struct LiquidCrystalDevice_t* device)
{
    device->DisplayControl &= ~LCD_CURSORON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
}

void lq_turnOnBlink(struct LiquidCrystalDevice_t* device)
{
    device->DisplayControl |= LCD_BLINKON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
}

void lq_turnOffBlink(struct LiquidCrystalDevice_t* device)
{
    device->DisplayControl &= ~LCD_BLINKON;
    lq_sendCommand(device, LCD_DISPLAYCONTROL | device->DisplayControl);
}

void lq_scrollDisplayLeft(struct LiquidCrystalDevice_t* device)
{
    lq_sendCommand(device, LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT);
}

void lq_scrollDisplayRight(struct LiquidCrystalDevice_t* device)
{
    lq_sendCommand(device, LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT);
}

void lq_leftToRight(struct LiquidCrystalDevice_t* device)
{
    device->DisplayMode |= LCD_ENTRYLEFT;
    lq_sendCommand(device, LCD_ENTRYMODESET | device->DisplayMode);
}

void lq_rightToLeft(struct LiquidCrystalDevice_t* device)
{
    device->DisplayMode &= ~LCD_ENTRYLEFT;
    lq_sendCommand(device, LCD_ENTRYMODESET | device->DisplayMode);
}

void lq_turnOnAutoscroll(struct LiquidCrystalDevice_t* device)
{
    device->DisplayMode |= LCD_ENTRYSHIFTINCREMENT;
    lq_sendCommand(device, LCD_ENTRYMODESET | device->DisplayMode);
}

void lq_turnOffAutoscroll(struct LiquidCrystalDevice_t* device)
{
    device->DisplayMode &= ~LCD_ENTRYSHIFTINCREMENT;
    lq_sendCommand(device, LCD_ENTRYMODESET | device->DisplayMode);
}

void lq_createChar(struct LiquidCrystalDevice_t* device, uint8_t slot, uint8_t charmap[8])
{
    uint8_t i = 0;
    slot &= 0x7; // we only have 8 locations 0-7
    lq_sendCommand(device, LCD_SETCGRAMADDR | (slot << 3));

    for (i = 0; i < 8; i++)
    {
        lq_writeDeviceByte(device, charmap[i], LCD_REGISTER_SELECT_BIT);
    }
}


void lq_sendCommand(LiquidCrystalDevice_t* device, uint8_t command)
{
    lq_writeDeviceByte(device, command, 0);
}

void lq_writeDeviceByte(LiquidCrystalDevice_t* device, uint8_t value, uint8_t mode)
{
    uint8_t highnib= value & 0xf0;
    uint8_t lownib= (value<<4) & 0xf0;

    lq_writeDevice4Bits(device, highnib | mode);
    lq_writeDevice4Bits(device, lownib | mode);
};

void lq_writeDevice4Bits(LiquidCrystalDevice_t* device, uint8_t value)
{
    lq_transmitI2C(device, value);
    lq_writeDevicePulse(device, value);
};

void lq_writeDevicePulse(LiquidCrystalDevice_t* device, uint8_t value)
{
    lq_transmitI2C(device, value | LCD_ENABLE_BIT);
    _delay_us(2);

    lq_transmitI2C(device, value & ~LCD_ENABLE_BIT);
    _delay_us(50);
};

void lq_transmitI2C(LiquidCrystalDevice_t* device, uint8_t value)
{
    i2c_master_sendByte(device->Address, value | device->Backlight);
};

void rtc_init (void) {
    i2c_master_start(0x68,I2C_WRITE);
    i2c_master_write (0x07);
    i2c_master_write(0x00);
    i2c_master_stop();
}
void rtc_setTime (unsigned char h, unsigned char m, unsigned char s) {
    i2c_master_start(0x68,I2C_WRITE);
    i2c_master_write(0);
    i2c_master_write(s);
    i2c_master_write(m);
    i2c_master_write(h);
    i2c_master_stop();
}


void rtc_getTime  (unsigned char *h, unsigned char *m, unsigned char *s) {
    i2c_master_start(0x68,I2C_WRITE);
    i2c_master_write(0x00);
    i2c_master_stop();
    
    i2c_master_start(0x68, I2C_READ);
    *s = i2c_master_readAck();
    *m = i2c_master_readAck();
    *h = i2c_master_readNack();
    i2c_master_stop();
}


/************************************************************************/
/* uint16_t read_analogue_input(uint8_t input_number)                   */
/*                                                                      */
/* Argument:                                                            */
/* uint8_t input_number                                                 */
/* Reprecenterar den ingång (0 - 5) som skall läsas av                  */
/*                                                                      */
/* Return:                                                              */
/* Det returnerande värdet är ett 16-bitars uint-tal mellan 0 - 1023    */
/************************************************************************/

uint16_t read_analogue_input(uint8_t input_number)
 {
    ADMUX = ((1 << REFS0) | input_number);
    ADCSRA = ((1 << ADEN) | (1 << ADSC) | (1 << ADPS0) | (1 << ADPS1) | (1 << ADPS2));
    while ((ADCSRA & (1 << ADIF)) == 0) ;
    ADCSRA = (1 << ADIF);
    return ADC;
}

void lq_print_rtc_value (LiquidCrystalDevice_t* device,unsigned char data) {
    uint8_t decimal = (data>>4);
    uint8_t singular_unit = (data & 0x0F);
    
    uint8_t data_array [2] = {decimal, singular_unit};
    
    i2c_master_start(0x27, I2C_WRITE);
    lq_writeDeviceByte(device,data_array[0]+48,LCD_REGISTER_SELECT_BIT);
    lq_writeDeviceByte(device,data_array[1]+48, LCD_REGISTER_SELECT_BIT);
    i2c_master_stop();
}

/*
void lq_display_decimal_value (LiquidCrystalDevice_t* device ,uint8_t data_hour,uint8_t data_min) {
    
    
    uint8_t decimal_hour = (data_hour/10);
    uint8_t singular_hour = (data_hour&10);
    uint8_t decimal_min = (data_min/10);
    uint8_t singular_min = (data_min%10);
    
    if (data_hour < 10) {
        decimal_hour = 0;
    }
    if (data_min < 10) {
        decimal_min = 0;
    }
    
    
    i2c_master_start(0x27, I2C_WRITE);
    lq_writeDeviceByte(device,decimal_hour+48,LCD_REGISTER_SELECT_BIT);
    lq_writeDeviceByte(device,singular_hour+48, LCD_REGISTER_SELECT_BIT);
    lq_print(device, ":");
    lq_writeDeviceByte(device, decimal_min+48, LCD_REGISTER_SELECT_BIT);
    lq_writeDeviceByte(device, singular_min+48, LCD_REGISTER_SELECT_BIT);
    i2c_master_stop();
}*/
