/*
* _4pinlcd.c
*
* Created: 2024-04-08 10:49:14
*  Author: Öberg
*/

#include "RTC_LCD.h"
#include <stdlib.h>

void lcdCOmmand(unsigned char cmnd) {
    PORTD = cmnd & 0xF0;
    PORTB &= ~ (1<<LCD_RS);
    PORTB &= ~ (1<<LCD_RW);
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~(1<<LCD_EN);
    _delay_us(3000);
    
    PORTD = cmnd<<4;
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~ (1<<LCD_EN);
    _delay_us(3000);
}

void lcdData(unsigned char data) {
    PORTD = data & 0xF0;
    PORTB |= (1<<LCD_RS);
    //PORTB &= ~ (1<<LCD_RW);
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~ (1<<LCD_EN);
    PORTD = data<<4;
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~ (1<<LCD_EN);
    _delay_us(1000);
}
void lcddigit (uint8_t data) {
    PORTD = data & 0xF0;
    PORTB |= (1<<LCD_RS);
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~ (1<<LCD_EN);
    PORTD = data<<4;
    PORTB |= (1<<LCD_EN);
    _delay_us(10);
    PORTB &= ~ (1<<LCD_EN);
    _delay_us(1000);
}

void lcd_init() {
    DDRD = 0xFF;
    DDRB = 0xFF;
    PORTB &=~(1<<LCD_EN);
    lcdCOmmand(0x33);
    lcdCOmmand(0x32);
    lcdCOmmand(0x28);
    lcdCOmmand(0x0e);
    lcdCOmmand(0x01);
    _delay_us(2000);
    lcdCOmmand(0x06);
}

void lcd_setcursor (unsigned char x, unsigned char y) {
    unsigned char firstCharAdr[] = {0x80,0xC0,0x94,0xD4};
    lcdCOmmand(firstCharAdr[y-1]+x-1);
    _delay_ms(1);
}

void lcd_print(char * str) {
    unsigned char i = 0;
    
    while(str[i] != 0) {
        lcdData(str[i]);
        i++;
    }
}

void printhex_to_ascii (uint8_t data) {       //This extract High nibble and Low nibble and seperate them to display it on LCD screen
    
    uint8_t high_nibble = (data>>4);          // Extract high nibble
    uint8_t low_nibble = (data & 0x0F);       // Extract low nibble
    uint8_t deciint = (high_nibble+=0x30);
    uint8_t singularint = (low_nibble+=0x30);
    if (singularint < 48)
    {
        singularint= 57;
        deciint--;
    }
    if (singularint > 57) {
        singularint = 48;
        deciint++;
    }    
        lcddigit(deciint);                    //Print high ASCII nibbble
        lcddigit(singularint);                //Print low ASCII nibbble
}

void lcdclear () {
    lcd_setcursor(0,0);
    lcd_print("                ");
    lcd_setcursor(1,0);
    lcd_print("                ");
}

void i2c_stop (){
    TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO);
}

void i2c_write (unsigned char data) {
    TWDR = data;
    TWCR = (1<<TWINT) | (1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
}

unsigned char i2c_read (unsigned char ackVal) {
TWCR = (1<<TWINT) | (1<<TWEN) | (ackVal<<TWEA);
while (!(TWCR & (1<<TWINT)));
return TWDR;
}
void i2c_start () {
    TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
}
void i2c_init() {
    TWSR = 0x00;
    TWBR = 152;
    TWCR = 0x04;
}
void rtc_init (void) {      //This is taken from Chat GPTi2c_init();
i2c_start();i2c_write(0xDE);
i2c_write(0x00); // Address of RTCC register
i2c_write(0x00); // Seconds
i2c_write(0x00); // Minutes
i2c_write(0x00); // Hours: 24-hour format, set to 00
i2c_write(0x01); // Day of the week: Not used, set to 01
i2c_write(0x01); // Date: Not used, set to 01
i2c_write(0x01); // Month: Not used, set to 01
i2c_write(0x00); // Year: Not used, set to 00
i2c_write(0x40); // Control register: SQWE = 0, OUT = 0, 24-hour formati2c_stop();
}
void rtc_setTime (unsigned char h, unsigned char m, unsigned char s) {
i2c_start();i2c_write(0xDE);i2c_write(s);i2c_write(m);i2c_write(h);i2c_stop();}
void rtc_getTime  (unsigned char *h, unsigned char *m, unsigned char *s) {i2c_start();i2c_write(0xDE);i2c_write(0);i2c_stop();i2c_start();i2c_write(0xDF);*s = i2c_read(1);*m = i2c_read(1);*h = i2c_read(0);i2c_stop();}
/// ************************************************************************ /
/// * uint16_t read_analogue_input(uint8_t input_number)                   * /
/// *                                                                      * /
/// * Argument:                                                            * /
/// * uint8_t input_number                                                 * /
/// * Reprecenterar den ingång (0 - 5) som skall läsas av                  * /
/// *                                                                      * /
/// * Return:                                                              * /
/// * Det returnerande värdet är ett 16-bitars uint-tal mellan 0 - 1023    * /
/// ************************************************************************ /
uint16_t read_analogue_input(uint8_t input_number)
{
    ADMUX = ((1 << REFS0) | input_number);
    ADCSRA = ((1 << ADEN) | (1 << ADSC) | (1 << ADPS0) | (1 << ADPS1) | (1 << ADPS2));
    while ((ADCSRA & (1 << ADIF)) == 0) ;
    ADCSRA = (1 << ADIF);
    return ADC;
}

