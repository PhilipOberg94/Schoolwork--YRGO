/*
 * HW-lektion15.c
 *
 * Created: 2024-02-15 14:23:24
 * Author : Öberg
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/delay.h>
uint8_t chararray [12] = {'H','E','L','L','O','!', ' ', 'J', 'O', 'C', 'K', 'E'};

void usart_init () {
    UCSR0B = (1<<TXEN0);
    UCSR0C = (1<<UCSZ01) | (1<<UCSZ00);
    UBRR0L = 103;
}

void usart_send (unsigned char ch) {
    while (!(UCSR0A&(1<<UDRE0)));
    UDR0 = ch;
}

int main(void)
{
    usart_init();
    while (1) {
        for (uint8_t i = 0;i < 14;i++)
        {
            usart_send(chararray [i]);
            
            if (i == 13)
            {
                _delay_ms(1000);
            }
        }
    }
}

