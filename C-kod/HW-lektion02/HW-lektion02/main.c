/*
 * main.c
 *
 * Created: 12/8/2023 11:23:05 AM
 *  Author: Öberg
 */ 

#include <avr/io.h>
#include <stdint.h>

int main(void)
{
    DDRD = 0b11111111;
    uint8_t counter = 0;

    while(1) {
        for (uint8_t i = 0;i < 10; i++) {
        printf(i , "gånger");
        }        
        
        
        //TODO:: Please write your application code 
    }
}