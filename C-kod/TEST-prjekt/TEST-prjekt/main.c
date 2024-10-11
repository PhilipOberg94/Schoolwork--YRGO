#include <avr/io.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include <string.h>


#define LCD_RS 0
#define LCD_RW 3
#define LCD_EN 1

void lcdCommand(unsigned char cmnd) {
    PORTD = cmnd & 0xF0; // Rewrite this
    PORTB &= ~(1<<LCD_RS);
    PORTD |= (1<<LCD_EN);
    _delay_us(1);
    PORTD &= ~(1<<LCD_EN);
    _delay_us(100);
    
    PORTD = cmnd<<1;
    PORTD |= (1<<LCD_EN);
    _delay_us(1);
    PORTD &= ~(1<<LCD_EN);
    _delay_us(100);
}

void lcdData(unsigned char data) {
    PORTD = data & 0xF0;
    PORTB |= (1<<LCD_RS);
    PORTD |= (1<<LCD_EN);
    _delay_us(1);
    PORTD &= ~(1<<LCD_EN);
    PORTD = data<<1;
    PORTD |= (1<<LCD_EN);
    _delay_us(1);
    PORTD &= ~(1<<LCD_EN);
    _delay_us(100);
}

void lcd_init() {
    DDRD = 0xFF;
    DDRB = 0xFF;
    PORTD &= ~(1<<LCD_EN);
    lcdCommand(0x33);
    lcdCommand(0x32);
    lcdCommand(0x28);
    lcdCommand(0x0e);
    lcdCommand(0x01);
    _delay_us(2000);
    lcdCommand(0x06);
}

void lcd_set_position(unsigned char x, unsigned char y) {
    unsigned char firstCharAdr[] = {0x80,0xC0,0x94,0xD4};
    lcdCommand(firstCharAdr[y-1] + x - 1);
    _delay_us(100);
}

void lcd_print(char * str) {
    unsigned char i = 0;
    
    while(str[i] != 0) {
        lcdData(str[i]);
        i++;
    }
}

void lcd_clear() {
    lcd_set_position(1,1);
    lcd_print("                ");
    lcd_set_position(1,2);
    lcd_print("                ");
    lcdCommand(0);
}


void lcd_write(char *str) {
    lcd_clear(); // Clear the screen screen
    
    // Length of string
    unsigned char len = strlen(str);
    
    // Limit string to only 32 characters long
    len = (len > 32) ? 32 : len;
    
    // Display on first line!
    lcd_set_position(1, 1);
    for (unsigned char i = 0; i < len && i < 16; ++i) {
        lcdData(str[i]);
    }
    
    // Display on the second line!
    if (len > 16) {
        lcd_set_position(1, 2);
        for (unsigned char i = 16; i < len; ++i) {
            lcdData(str[i]);
        }
    }
}

int main (void) {
    lcd_init();
    lcd_write("Hello!");
    
    while (1) {
        PORTD |= ~(1<<0);
        _delay_ms(1000);
    }
}