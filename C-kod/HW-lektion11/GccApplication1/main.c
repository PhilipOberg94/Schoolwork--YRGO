/*
 * GccApplication1.c
 *
 * Created: 2024-01-30 14:19:51
 * Author : Öberg
 */ 

#include <avr/io.h>


int main(void)
{
    DDRD = 0b11101111;
    DDRC = 0xFF;
    DDRB = 0xFF;
    
    TCCR0A = 0;
    TCCR0B = 0x06;
    TCNT0 = 0x00;
    
    while (1) {
        
        do {
            PORTD = TCNT0&0b11101111;
        } 
        while ((TIFR0&(0x1<<TOV0))==0);
        
        TIFR0 = 1<<TOV0;
        PORTB ++;
    }
}
