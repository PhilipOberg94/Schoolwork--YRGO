import numpy as np

def fourier_transform_triangle_wave(numbers_array, file):
    with open(file, 'w') as f: 
        f.write("__________Triangle wave____________\n")        # Print function to write the text to the file  #
        f.write("_________________________________\n")          #                                               #
        f.write("Value of n   | Value of Bn\n")                 #                                               #
        f.write("---------------------------------\n")          #                                               #
        print("__________Triangle wave__________")              #                                               #
        print("_________________________________")              #                                               #
        print("Value of n   | Value of Bn")                     #                                               #
        print("---------------------------------")              #-----------------------------------------------#
        for n in numbers_array:
            if n % 2 == 0:
                dbVRMS = 0
            else:
                Bn = ((8 * 2.5) / ((np.pi ** 2) * (n ** 2))) * (-1 ** ((n - 1) / 2)) # Equation to calculate the value of Bn for a triangle wave
                dbVRMS = 20 * np.log10(abs(Bn) / np.sqrt(2))        # Equation to calculate the value of Bn in decibel
            f.write(f"{n:<12} | {dbVRMS:<3.3f} dbVRMS\n")
            print(f"{n:<12} | {dbVRMS:<3.3f} dbVRMS")

def fourier_transform_sawtooth_wave(numbers_array, file):
    Bn_values = {}
    with open(file, 'a') as f: 
        f.write("\n__________Sawtooth wave____________\n")          # Print function to write the text to the file  #
        f.write("__________________________________\n")             #                                               #
        f.write("Value of n   | Value of Bn\n")                     #                                               #  
        f.write("----------------------------------\n")             #                                               #
        print("\n__________Sawtooth wave__________")                #                                               #       
        print("___________________________________")                #                                               #
        print("Value of n   | Value of Bn")                         #                                               #
        print("-----------------------------------")                #-----------------------------------------------#
        for n in numbers_array:
            Bn = abs(((2 * 2.5) / (np.pi * n)) * ((-1) ** (n - 1))) # Equation to calculate Bn on a sawtooth wave
            dbVRMS = 20 * np.log10(Bn / np.sqrt(2))                 # Equation to calculate the value of Bn in decibel
            f.write(f"{n:<12} | {dbVRMS:<3.3f} dbVRMS\n")
            print(f"{n:<12} | {dbVRMS:<3.3f} dbVRMS")
            Bn_values[n] = Bn
    return Bn_values

def transfer_function_low_pass_filter(numbers_array, frequency, R, C, file):
    B_values = fourier_transform_sawtooth_wave(numbers_array, file)
    with open(file, 'a') as f:
        f.write("\n__________Low Pass Filter__________\n")        # Print function to write the text to the file  #
        f.write("___________________________________\n")          #                                               #
        f.write("Value of n   | Magnitude\n")                     #                                               #
        f.write("-----------------------------------\n")          #                                               #
        print("\n__________Low Pass Filter______________")        #                                               #
        print("_______________________________________")          #                                               #
        print("Value of n   |  Value of H  | Magnitude")          #                                               #
        print("---------------------------------------")          #-----------------------------------------------#
        for n in numbers_array:
            omega = 2 * np.pi * frequency * n
            H = abs(1 / np.sqrt(1 + (omega * R * C) ** 2))          # Equation to calculate the magnitude of the transfer function
            H *= B_values[n]
            dbVRMS = 20 * np.log10(H / np.sqrt(2))                 # Equation to calculate the magnitude in decibel
            f.write(f"{n:<12} | {H:<12.3f} | {dbVRMS:<3.3f} dbVRMS\n")
            print(f"{n:<12} | {H:<12.3f} | {dbVRMS:<3.3f} dbVRMS")

def cutoff_frequency_low_pass_filter(R, C, file):
    cutoff_frequency = 1 / (2 * np.pi * R * C)                      # Equation to calculate the cutoff frequency
    with open(file, 'a') as f:
        f.write("\n__________Cutoff frequency__________\n")         # Print function to write the text to the file  #
        f.write("___________________________________\n")            #                                               #
        f.write(f"Cutoff frequency: {cutoff_frequency:.3f} Hz\n")   #                                               #
        print("\n__________Cutoff frequency__________")             #                                               #
        print("_____________________________________")              #                                               #
        print(f"Cutoff frequency: {cutoff_frequency:<3.3f} Hz")     #-----------------------------------------------#
        
numbers_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
frequency = 1000  # 1 kHz
R = 8200  # 8,2 kOhm
C = 10 * 10 ** -9  # 10 nF

output_file = './Frekvensanalys_output.txt'
fourier_transform_triangle_wave(numbers_array, output_file)
print("")
fourier_transform_sawtooth_wave(numbers_array, output_file)
print("")
transfer_function_low_pass_filter(numbers_array, frequency, R, C, output_file)
print("")
cutoff_frequency_low_pass_filter(R, C, output_file)