import numpy as np
import cmath

def fourier_transform_triangle_wave(numbers_array, file):
    with open(file, 'w') as f: 
        f.write("__________Triangle wave__________\n")
        f.write("_________________________________\n")
        f.write("Value of n   | Value of Bn\n")
        f.write("--------------------------\n")
        print("__________Triangle wave__________")
        print("_________________________________")
        print("Value of n   | Value of Bn")
        print("--------------------------")
        for n in numbers_array:
            if n % 2 == 0:
                Bn = 0
            else:
                Bn = ((8 * 2.5) / ((np.pi ** 2) * (n ** 2))) * (-1 ** ((n - 1) / 2))
            f.write(f"{n:<12} | {Bn:.3f} db\n")
            print(f"{n:<12} | {Bn:.3f} db")


def fourier_transform_sawtooth_wave(numbers_array, file):
    with open(file, 'a') as f: 
        f.write("\n__________Sawtooth wave__________\n")
        f.write("_________________________________\n")
        f.write("Value of n   | Value of Bn\n")
        f.write("--------------------------\n")
        print("\n__________Sawtooth wave__________")
        print("_________________________________")
        print("Value of n   | Value of Bn")
        print("--------------------------")
        for n in numbers_array:
            Bn = ((2 * 2.5) / (np.pi * n)) * ((-1) ** (n - 1))
            f.write(f"{n:<12} | {Bn:.3f} db\n")
            print(f"{n:<12} | {Bn:.3f} db")

def transfer_function_low_pass_filter(numbers_array, frequency, R, C, file):
    with open(file, 'a') as f:
        f.write("\n_______________Low-pass filter_______\n")
        f.write("_______________________________________\n")
        f.write("Value of H(jω) | Value of H(jω) in VRMS\n")
        f.write("--------------------------------------\n")
        print("\n___________________Low-pass filter____\n")
        print("________________________________________")
        print("Value of H(jω) | Value of H(jω) in VRMS")
        print("---------------------------------------")
        for i in range(len(numbers_array)):
            omega = 2 * np.pi * frequency * numbers_array[i]
            magnitude = 1 / np.sqrt(1 + (omega * R * C) ** 2)
            dbVRMS = 20 * np.log10(magnitude / np.sqrt(2))
            print(f"{magnitude:<14.3f} | {dbVRMS:.3f} VRMS")
            f.write(f"{magnitude:<14.3f} | {dbVRMS:.3f} VRMS\n")


numbers_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
frequency = 1000  # 1 kHz
R = 8200  # 1 kOhm
C = 10 * 10 ** -9  # 10 nF

output_file = './Labration - Frekvensanalys.txt'
fourier_transform_triangle_wave(numbers_array, output_file)
print("")
fourier_transform_sawtooth_wave(numbers_array, output_file)
print("")
transfer_function_low_pass_filter(numbers_array,frequency, R, C, output_file)