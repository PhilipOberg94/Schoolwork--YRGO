/*
* I2C_Communication.c
*
* Created: 2024-02-26 21:51:03
* Author : Öberg
*/

#include "RTC_LCD/RTC_LCD.h"

uint16_t min_array [4] = {0x00 ,0x15 ,0x30, 0x45};
uint16_t hour_array [24] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x20, 0x21, 0x22, 0x23};
int menu_int = 1;
int min_int = 0;
int hour_int = 0;

unsigned char box1n5_array [2] = {0x00,0x00};
unsigned char box2n6_array [2] = {0x00,0x00};
unsigned char box3n7_array [2] = {0x00,0x00};
unsigned char box4n8_array [2] = {0x00,0x00};

void press_button () {              //This is to make it impossible to hold down a button to scroll in the menu 
    while (PIND & (1<<2)) {
        _delay_ms(10);
    }
}

void lcd_display_time (uint8_t time_hour, uint8_t time_min) {       //Displays current time
    
    printhex_to_ascii(time_hour);
    lcd_print(":");
    printhex_to_ascii(time_min);
}
void hold_button (uint16_t button_press) {          //Make something else happen if you hold down the button instead of pressing it
    uint16_t presstime = 1;
    if (button_press > 740) {
        presstime++;
        _delay_ms(1);
        
        if (presstime >= 300000) {
            menu_int = 0;
        }
        } else {
        // Reset pressTime if the button is not pressed
        presstime = 0;
    }
}

int main(void)
{
    DDRD = 0xFF;
    DDRB = 0xFF;
    DDRC = 0x00;
    PORTC= 0b00000001;
    unsigned char hour,min,sec;
    hour = 0x12;
    min = 0x00;
    sec = 0x00;
    lcd_init();
    lcdclear ();
    rtc_init();

    while (1) {
        
            
        if (menu_int == 0) {            //Set time on every startup, possible to select this by holding down a specific button
            lcd_setcursor(1,1);
            lcd_print("Set time:");

            if (read_analogue_input(0)< 400 && read_analogue_input(0) > 200){           //Change time with ADC from buttons
                min--;
                _delay_ms(50);
            }
            else if (read_analogue_input(0) > 740 && read_analogue_input(0) < 800) {
                min++;
                _delay_ms(50);
            }
            
            _delay_ms(100);
            rtc_setTime(hour, min, sec);
        }
        
        if (menu_int == 1) {
            
            lcd_setcursor(1,1);
            lcd_print("Box 1&5 ");
            lcd_setcursor(1,2);
            printhex_to_ascii(hour_array[hour_int]);            //Displays the time for opening the boxes
            lcd_print(":");
            printhex_to_ascii(min_array[min_int]);
            box1n5_array [0] = (hour_array [hour_int]);         //Stores the set time for opening two of the boxes
            box1n5_array [1] = (min_array [min_int]);
            
            if (read_analogue_input(0)< 400 && read_analogue_input(0) > 200) {
                min_int--;
                _delay_ms(100);
            }
            else if (read_analogue_input(0) > 740 && read_analogue_input(0) < 800) {
                min_int++;
                _delay_ms(100);
            }
        }
        
        if (menu_int == 2) {
        
            lcd_setcursor(1,1);
            lcd_print("Box 2&6 ");
            lcd_setcursor(1,2);
            printhex_to_ascii(hour_array[hour_int]);            //Displays the time for opening the boxes
            lcd_print(":");
            printhex_to_ascii(min_array[min_int]);
            box2n6_array [0] = (hour_array [hour_int]);         //Stores the set time for opening two of the boxes
            box2n6_array [1] = (min_array [min_int]);
        
            if (read_analogue_input(0)< 400 && read_analogue_input(0) > 200) {
                min_int--;
                _delay_ms(100);
            }
            else if (read_analogue_input(0) > 740 && read_analogue_input(0) < 800) {
                min_int++;
                _delay_ms(100);
            }
        }
        if (menu_int == 3) {
        
           lcd_setcursor(1,1);
           lcd_print("Box 3&7 ");
           lcd_setcursor(1,2);
           printhex_to_ascii(hour_array[hour_int]);            //Displays the time for opening the boxes
           lcd_print(":");
           printhex_to_ascii(min_array[min_int]);
           box3n7_array [0] = (hour_array [hour_int]);         //Stores the set time for opening two of the boxes
           box3n7_array [1] = (min_array [min_int]);
       
           if (read_analogue_input(0)< 400 && read_analogue_input(0) > 200) {
               min_int--;
               _delay_ms(100);
           }
           else if (read_analogue_input(0) > 740 && read_analogue_input(0) < 800) {
               min_int++;
               _delay_ms(100);
           }
        }
        if (menu_int == 4) {
            lcd_setcursor(1,1);
            lcd_print("Box 4&8 ");
            lcd_setcursor(1,2);
            printhex_to_ascii(hour_array[hour_int]);            //Displays the time for opening the boxes
            lcd_print(":");
            printhex_to_ascii(min_array[min_int]);
            box4n8_array [0] = (hour_array [hour_int]);         //Stores the set time for opening two of the boxes
            box4n8_array [1] = (min_array [min_int]);
            
            if (read_analogue_input(0)< 400 && read_analogue_input(0) > 200) {
                min_int--;
                _delay_ms(100);
            }
            else if (read_analogue_input(0) > 740 && read_analogue_input(0) < 800) {
                min_int++;
                _delay_ms(100);
            }
        else if ((read_analogue_input(0) > 600) && (read_analogue_input(0) < 800)) {
            min_int--;
        }
        
        }
        if ((read_analogue_input(0) > 750) && (read_analogue_input(0) < 950)) {
            menu_int++;
        }
        
        if (menu_int > 4) {             //Menu resets
            menu_int = 0;
        }
        if (menu_int < 1) {
            menu_int = 4;
        }
        if (min_int > 3) {
            min_int = 0;
            hour_int++;
        }
        if (min_int < 0) {
            min_int = 3;
            hour_int--;
        }
        if (hour_int < 0) {
            hour_int = 23;
        }
        if (hour_int > 23) {
            hour_int = 0;
        }
        if (min < 0x01) {
            min = 0x59;
            hour--;
        }
        if (min > 0x59) {
            min = 0x00;
            hour++;
        }
        if (hour < 0x00) {
            hour = 0x23;
        }
        if (hour > 0x23) {
            hour = 0x00;
        }
        rtc_getTime(&hour, &min, &sec);         //Gets time value from RTC
        _delay_ms(100);
        lcd_setcursor(12,1);
        lcd_display_time(hour,min);
    }
}

