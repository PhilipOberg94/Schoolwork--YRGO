/*
 * HW-lektion16.c
 *
 * Created: 2024-02-28 10:45:21
 * Author : Öberg
 */ 

#include <avr/io.h>

#define MOSI 3
#define SCK 5
#define SS 2

void execute (unsigned char cmd, unsigned char data) {
    PORTB &= ~(1<<SS);
    
    SPDR = cmd;
    while (!(SPSR & (1<<SPIF)));
    
    SPDR = data;
    while (!(SPSR & (1<<SPIF)));
    
    PORTB |= (1<<SS);
}


int main(void)
{
    DDRB = (1<<MOSI) | (1<<SCK) | (1<<SS);
    SPCR = (1<<SPE) | (1<<MSTR) | (1<<SPR0);
    
    execute(0x09, 0b11111111);
    
    execute(0x0B, 0x05);
    execute(0x0C, 0x01);
    execute(0x01, 0x08);
    execute(0x02, 0x00);
    execute(0x03, 0x00);
    execute(0x04, 0x08);
    execute(0x05, 0x05);
    
    while (1) 
    {
    }
}

