/*
 * HW-lektion17.c
 *
 * Created: 2024-03-13 11:16:51
 * Author : Öberg
 */ 

#include <avr/io.h>


int main(void)
{
    DDRD = 0x00;
    DDRB = 0x00;
    /* Replace with your application code */
    while (1) 
    {
        PORTD = 0x00;
        PORTB = 0x00;
    }
}

