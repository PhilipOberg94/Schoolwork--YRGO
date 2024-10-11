/*
 * main.c
 *
 * Created: 1/10/2024 10:18:09 AM
 *  Author: Öberg
 */ 

#include <avr/io.h>
#include <stdint.h>


void swap(uint8_t* xp, uint8_t* yp) 
{ 
    uint8_t temp = *xp; 
    *xp = *yp; 

    *yp = temp; 
} 
  
// Function to perform Selection Sort 
void selectionSort(uint8_t arr[], uint8_t n) 
{ 
    uint8_t i, j, min_idx; 
  
    // One by one move boundary of 
    // unsorted subarray 
    for (i = 0; i < n - 1; i++) { 
        // Find the minimum element in 
        // unsorted array 
        min_idx = i; 
        for (j = i + 1; j < n; j++) 
            if (arr[j] < arr[min_idx]) 
                min_idx = j; 
  
        // Swap the found minimum element 
        // with the first element 
        swap(&arr[min_idx], &arr[i]); 
    } 
} 
  
// Function to PORTD = sorted_array [i]; an array 
void writearray (uint8_t arr [], uint8_t size)
{ 
    uint8_t i; 
    for (i = 0; i < size; i++) 
    PORTD = arr[i]; 
} 
  
// Driver code 
int main() 
{ 
    DDRD = 0b11111111;
    uint8_t arr[] = {100, 40, 20, 50, 30, 60, 80, 70, 10, 90 }; 
    uint8_t n = sizeof(arr) / sizeof(arr[0]); 
    writearray(arr,n);
  
    selectionSort(arr, n); 
    writearray(arr,n);
  
    return 0; 
}