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

int main(void)
{
    DDRD = 0b00000000;
    DDRB = 0b00000000;
    uint8_t data_variabel = 0;
    uint8_t data_array [32] = {0};
    uint8_t i = 0;
    
    while(1)
    {
        if (PORTB == 0b00000001) {
            data_variabel = PIND;
            data_array [i] = data_variabel;
            i++;
        }           
    }
}