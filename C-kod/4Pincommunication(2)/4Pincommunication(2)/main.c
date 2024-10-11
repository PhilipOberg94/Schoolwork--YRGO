/*
* 4Pincommunication(2).c
*
* Created: 2024-01-29 00:14:47
* Author : Öberg
*/

#define F_CPU 16000000UL

#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#define LCD_RS 0
#define LCD_RW 1
#define LCD_EN 2
#define BUTTON1 3
#define BUTTON2 4
#define BUTTON3 5
#define CS      PINB2
#define MOSI    PINB3
#define MISO    PINB4
#define SCK     PINB5
#define SS      1


char buffer [8];
unsigned char ascii;

#include <avr/io.h>


uint8_t SPI_data [8];
uint8_t data = 0;

void SPI_init()
{
    // set CS, MOSI and SCK to output
    PORTB |= (1 << CS) | (1 << MOSI) | (1 << SCK);

    // enable SPI, set as master, and clock to fosc/128
    SPCR = (1 << SPE) | (1 << MSTR) | (1 << SPR1) | (1 << SPR0);
}
void SPI_masterTransmitByte(uint8_t data)
{
    // load data into register
    SPDR = data;

    // Wait for transmission complete
    while(!(SPSR & (1 << SPIF)));
}
void SPI_master_transmitdata (uint8_t data) {
    PORTD |= ~(1<<SS);
    SPI_masterTransmitByte(data);
    PORTD |= ~(1<<SS);
}
uint8_t SPI_master_recievedata() {
    SPDR = 0xFF;
    while(!(SPSR & (1 << SPIF)));
    return SPDR;
}

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
    _delay_us(3000);
}

bool sw1 (){
    if (PINB & (1<<BUTTON1)) {
        return false;
    }
    else return true;
}
bool sw2 (){
    if (PINB & (1<<BUTTON2)) {
        return false;
    }
    else return true;
}
bool sw3 (){
    if (PINB & (1<<BUTTON3)) {
        return false;
    }
    else return true;
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

void lcd_gotoxy(unsigned char x, unsigned char y) {
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
void lcdclear () {
    lcd_gotoxy(1,1);
    lcd_print("                ");
    lcd_gotoxy(2,1);
    lcd_print("                ");
}
char* int_to_ascii (uint16_t data) {
    char* datavalue = itoa(data,buffer,10);
    return datavalue;
}



int main(void)
{
    SPI_init();
    lcd_init();
    
    
    while (1){
        //PORTB &= ~(1<<3);
        //SPDR = 'G';
        //while (!(SPSR & (1<<SPIF)));
        //PORTB |= (1<<3);
        //_delay_ms(100);
        //itoa (SPDR,str, 10);
        //lcd_gotoxy(1,1);
        //lcd_print(str);
        //_delay_ms(100);
        
        lcd_gotoxy(1,1);
        lcd_print("Hello");
        _delay_ms(10);
        
        
    }
}