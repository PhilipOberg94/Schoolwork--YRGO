/*
 * main.c
 *
 * Created: 12/15/2023 10:26:10 AM
 *  Author: Öberg
 */ 

#define F_CPU 1000000UL //1 Mhz klockfrekvens
#include <avr/io.h>
#include <avr/delay.h>


int main(void)
{
    DDRB = 0b00000000;
    DDRD = 0b11111111;
    PORTB = 0b00000010;
    while(1) {
        PORTD = PINB;
        _delay_ms(1000);
    }
}