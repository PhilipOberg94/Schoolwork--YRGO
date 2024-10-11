/*
* main.c
*
* Created: 12/12/2023 1:53:10 PM
*  Author: Öberg
*/

#include <avr/io.h>

int main(void)
{
    unsigned char z;
    DDRC = 0;
    DDRD = 0xFF;

    while(1) {
        z = PINC;
        z = z & 0b00000011;
        
        if (z == 0) {
            PORTD = 0;
        }
        if (z == 1) {
            PORTD = "1";
        }
        if (z == 2) {
            PORTD = "2";
        }
        if (z == 3) {
            PORTD = "3";
        }
    }
}