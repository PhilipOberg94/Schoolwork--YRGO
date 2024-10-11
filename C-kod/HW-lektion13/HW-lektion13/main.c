/*
 * HW-lektion13.c
 *
 * Created: 2024-02-01 14:25:07
 * Author : Öberg
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>  /*Needed for interrupts*/
#include <avr/delay.h>

int main(void)
{
    DDRD =  0b11111111;
    PORTD = 0b00000100;
    EIMSK = (1<<INT0);       /*Enable interrupt INT0*, see page 336*/
    EICRA = (1<<ISC01);      /*Enable falling edge interrupt, see page 337*/
    sei();                   /*Enable interrupts*/
    while (1) 
    {
        PORTD ^= (1<<0);     /*Toggle bit0*/
        _delay_ms(200);
    }
}

ISR(INT0_vect) {
    PORTD ^=(1<<1);          /*toggle bit1*/
}

