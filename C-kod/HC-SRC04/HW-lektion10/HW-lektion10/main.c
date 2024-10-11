/*
* main.c
*
* Created: 1/16/2024 9:16:25 AM
*  Author: JPJ-Engineering
*/
#define F_CPU 1000000UL

#include <avr/io.h>
#include <stdio.h>
#include <util/delay.h>
#include <stdbool.h>
#include <avr/interrupt.h>

#define LCD_DPRT PORTD
#define LCD_DDRD DDRD
#define LCD_DPIN PIND
#define LCD_CPRT PORTB
#define LCD_CDDR DDRB
#define LCD_CPIN PINB
#define LCD_RS 0
#define LCD_RW 1
#define LCD_EN 2
#define BUTTON1 3
#define BUTTON2 4
#define BUTTON3 5

void lcdCOmmand(unsigned char cmnd) {
    LCD_DPRT = cmnd;
    LCD_CPRT &= ~ (1<<LCD_RS);
    LCD_CPRT &= ~ (1<<LCD_RW);
    LCD_CPRT |= (1<<LCD_EN);
    _delay_us(10);
    LCD_CPRT &= ~(1<<LCD_EN);
    _delay_us(3000);
}

void lcdData(unsigned char data) {
    LCD_DPRT = data;
    LCD_CPRT |= (1<<LCD_RS);
    LCD_CPRT &= ~ (1<<LCD_RW);
    LCD_CPRT |= (1<<LCD_EN);
    _delay_us(10);
    LCD_CPRT &= ~ (1<<LCD_EN);
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
    LCD_DDRD = 0xFF;
    LCD_CDDR = 0b00000111;
    PORTB = 0b00111000;
    
    LCD_CPRT &=~(1<<LCD_EN);
    _delay_us(2000);
    lcdCOmmand(0x38);
    lcdCOmmand(0x0E);
    lcdCOmmand(0x01);
    _delay_us(2000);
    lcdCOmmand(0x06);
    
    DDRC = 0xFF;							// Port C all output. PC0: RW		PC1: RS		PC2: E
    DDRC &= ~(1<<DDC5);						// Set Pin C5 as input to read Echo
    PORTC |= (1<<PORTC5);					// Enable pull up on C5
    PORTC &= ~(1<<PC4);						// Init C4 as low (trigger)

    PRR &= ~(1<<PRTIM1);					// To activate timer1 module
    TCNT1 = 0;								// Initial timer value
    TCCR1B |= (1<<CS10);					// Timer without prescaller. Since default clock for atmega328p is 1Mhz period is 1uS
    TCCR1B |= (1<<ICES1);					// First capture on rising edge

    PCICR = (1<<PCIE1);						// Enable PCINT[14:8] we use pin C5 which is PCINT13
    PCMSK1 = (1<<PCINT13);					// Enable C5 interrupt
    sei();
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
int main(void)
{
    lcd_init();
    
    
    while(1){
        
        
        _delay_ms(60); 							// To allow sufficient time between queries (60ms min)

        PORTC |= (1<<PC4);						// Set trigger high
        _delay_us(10);							// for 10uS
        PORTC &= ~(1<<PC4);						// to trigger the ultrasonic module
    }
}
/*******************************************INTURRUPT PCINT1 FOR PIN C5*******************************************/
char result [6];

ISR(PCINT1_vect) {
    if (bit_is_set(PINC,PC5)) {					// Checks if echo is high
        TCNT1 = 0;								// Reset Timer
        PORTC |= (1<<PC3);
        } else {
        uint32_t numuS = TCNT1;					// Save Timer value
        uint16_t oldSREG = SREG;
       
        char temp [6];
        sprintf(temp, "%d",(int) roundf (numuS/58));
        
        for (int i = 0; i < sizeof(temp);i++) {
            if (result[i] != temp[i]) {
                
        lcdCOmmand(1);
            }
            result [i] = temp [i];
        }
        
         lcd_gotoxy(1,1);
        lcd_print("CM: ");
         lcd_gotoxy(5,1);
        lcd_print(result);
        _delay_us(250);
        SREG = oldSREG;
						// Enable interrupts
    }
}