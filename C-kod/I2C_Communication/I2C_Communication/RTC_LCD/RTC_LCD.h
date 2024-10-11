/*
 * _4pinlcd.h
 *
 * Created: 2024-04-08 10:51:12
 *  Author: Öberg
 */ 


#ifndef RTC_LCD_H_
#define RTC_LCD_H_

#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>

#define LCD_RS 0
#define LCD_RW 1
#define LCD_EN 2
#define LCD_D4 2
#define LCD_D5 3
#define LCD_D6 4
#define LCD_D7 7
#define BUTTON1 3
#define BUTTON2 4
#define BUTTON3 5

void lcdCOmmand(unsigned char cmnd);

void lcdData(unsigned char data);

void lcd_init();

void lcd_setcursor(unsigned char x, unsigned char y);

void lcd_print(char * str);

void printhex_to_ascii (uint8_t data);

void lcdclear (void);

void lcddigit (uint8_t data);

void i2c_stop (void);

void i2c_write (unsigned char data);

unsigned char i2c_read (unsigned char ackVal);

void i2c_start (void);

void i2c_init(void);

void rtc_init (void);

void rtc_setTime (unsigned char h, unsigned char m, unsigned char s);

void rtc_getTime  (unsigned char *h, unsigned char *m, unsigned char *s);

uint16_t read_analogue_input(uint8_t input_number);



#endif /* 4PINLCD_H_ */