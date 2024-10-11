/*
* 4pinserialcomm.c
*
* Created: 2024-01-28 22:32:31
* Author : Öberg
*/
#define F_CPU 16000000UL

#include <avr/io.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#include <util/delay.h>

#define LCD_PORT PORTD
#define LCD_DDR DDRD

#define LCD_RS 0
#define LCD_RW 1
#define LCD_EN 2

void lcd_command (unsigned char cmd) {
    LCD_PORT = (LCD_PORT & 0x0F) | (cmd & 0xF0);
    LCD_PORT &= ~ (1<<LCD_RS);
    LCD_PORT &= ~ (1<<LCD_RW);
    LCD_PORT |= (1<<LCD_EN);
    _delay_us(10);
    LCD_PORT &= ~ (1<<LCD_EN);
    _delay_us(3000);
    
    LCD_PORT = (LCD_PORT & 0x0F) | (cmd<<4);
    LCD_PORT |= (1<<LCD_EN);
    _delay_us(10);
    LCD_PORT &= ~ (1<<LCD_EN);
    _delay_us(3000);
}

void lcd_data (unsigned char data) {
    LCD_PORT = (LCD_PORT & 0x0F) | (data & 0xF0);
    LCD_PORT |= (1<<LCD_RS);
    LCD_PORT &= ~ (1<<LCD_RW);
    LCD_PORT |= (1<<LCD_EN);
    
    _delay_us(10);
    LCD_PORT |= (1<<LCD_EN);
    LCD_PORT = (LCD_PORT & 0x0F) | (data<<4);
    LCD_PORT |= (1<<LCD_EN);
    
    _delay_us(10);
    LCD_PORT &= ~ (1<<LCD_EN);
    _delay_us(3000);
}

void lcd_init () {
    LCD_DDR = 0xFF;
    LCD_PORT &= ~ (1<<LCD_EN);
    
    lcd_command(0x33);
    lcd_command(0x32);
    lcd_command(0x28);
    lcd_command(0x0E);
    lcd_command(0x01);
    
    _delay_us(2000);
}

void lcd_gotoxy (unsigned char x, unsigned char y) {
    unsigned char firstcharadr [] = {0x80, 0xC0, 0x94, 0xD4};
    lcd_command(firstcharadr [y-1] + x-1);
    _delay_ms(1);
}

void lcd_print (char * str) {
    unsigned char i = 0;
    while (str [i] != 0) {
        lcd_data(str [i]);
        i++;
    }
}

int main(void)
{
    lcd_init();
    
    while (1) {
        lcd_gotoxy(1,2);
        lcd_print("The world is but");
        lcd_gotoxy(1,2);
        lcd_print("one country      ");
        _delay_ms(3000);
        lcd_gotoxy(1,1);
        lcd_print("and mankind its ");
        lcd_gotoxy(1,2);
        lcd_print("citizens     ");
        _delay_ms(3000);
    }
    return 0;
}

