/*
 * HW-lektion20.c
 *
 * Created: 2024-03-05 09:48:03
 * Author : Öberg
 */ 

#include <avr/io.h>
#include <stdint.h>


void i2c_write (unsigned char data) {
    TWDR = data;
    TWCR = (1<<TWINT) | (1<<TWEN);
    while ((TWCR & (TWCR<<TWINT)) == 0);
}

void i2c_start () {
    TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);
    while ((TWCR & (1<<TWINT)) == 0);
}
void i2c_stop () {
    TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO);
}
void i2c_init () {
    TWSR=0x00;
    TWBR=152;
    TWCR=0x04;
}

int main(void)
{
    DDRD = 0b11111111;
    i2c_init();
    while (1) {
        i2c_start();
        i2c_write(0b11010000); //Write to SLAVE
        i2c_write(0b11110000); // Bytes sent
        i2c_stop();
    }
}

