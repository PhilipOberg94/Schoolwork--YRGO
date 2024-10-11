/*
 * main.c
 *
 * Created: 1/16/2024 10:45:45 AM
 *  Author: Öberg
 */ 
/*
 * main.c
 *
 * Created: 1/16/2024 9:16:39 AM
 *  Author: Öberg
 */ 

#define F_CPU 1000000UL
#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>
#include <stdbool.h>

int main(void)
{
    DDRD = 0b00000000;
    DDRB = 0b00000000;
    uint8_t data_variabel = 0;
    uint8_t data_array [12];
    uint8_t i = 0;
    bool pin_state = 0;
    
    while(i < 12)
    {
        pin_state = (PINB & 0b00000001);
        if ((PINB & 0b00000001) && (!pin_state)) {
            data_array[i] = PIND & 0b11111111;
            i++;
        }
         _delay_ms(1);
    }
    data_array;
}