/*
 * main.c
 *
 * Created: 1/9/2024 11:17:05 AM
 *  Author: Öberg
 */ 

#include <avr/io.h>
#include <stdint.h>

int main(void)
{
    DDRD = 0b11111111;
    uint8_t test_array [10] = {89,82,71,79,95,69,76,65,50,51};
    while(1)
    {
        
        for (uint8_t r = 0;r < 10;r++)
        {
            PORTD = test_array [r];
        }
    }
}