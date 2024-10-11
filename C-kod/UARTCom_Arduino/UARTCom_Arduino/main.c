/*
* UARTCom_Arduino.c
*
* Created: 2024-02-27 13:26:43
* Author : Öberg
*/

#define F_CPU 16000000UL // Assuming 16 MHz clock
#include <avr/io.h>
#include <util/delay.h>

void USART_init(unsigned int ubrr) {
    UBRR0H = (unsigned char)(ubrr>>8);
    UBRR0L = (unsigned char)ubrr;
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);
    UCSR0C = (1<<UCSZ01)|(1<<UCSZ00); // 8 data bits, 1 stop bit
    DDRD = 0b00000100;
}

unsigned char USART_receive(void) {
    while (!(UCSR0A & (1<<RXC0)));
    return UDR0;
}

int main(void) {
    USART_init(103); // 9600 Baud rate at 16MHz
    uint16_t receivedData [4] = {0,0,0,0};

    while(1) {
        while (USART_receive() != 'S');
            for (uint8_t i = 0; i<4; i++) {
                receivedData [i] = USART_receive();
            }
        // Process receivedData
    }
}

