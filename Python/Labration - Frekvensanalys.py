import numpy as np

# Function to calculate Fourier transform for triangle wave
def fourier_transform_triangle_wave(numbers_array):
    for i in range(len(numbers_array)):
        n = numbers_array[i]
        if n % 2 == 0:
            Bn = 0
        else:
            Bn = ((8 * 2.5) / ((np.pi ** 2) * (n ** 2))) * (-1 ** ((n - 1) / 2))
        print(f"Triangle wave - Bn of n: {n} {Bn:.3f}")

# Function to calculate Fourier transform for sawtooth wave
def fourier_transform_sawtooth_wave(numbers_array):
    for i in range(len(numbers_array)):
        n = numbers_array[i]
        Bn = (2 * 2.5) / (np.pi * n) * (-1) ** (n - 1)
        print(f"Sawtooth wave - Bn of n: {n} {Bn:.3f}")

    
def transfer_function_low_pass_filter(frequency, i, R, C):
    numbers_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    omega = (2 * np.pi) * (frequency * numbers_array[i])
    j_omega_RC = 1j * omega * R * C
    H_j_omega = (1 / np.sqrt(j_omega_RC + 1) ** 2)
    magnitude = abs(H_j_omega)
    decibel = 20 * np.log10(magnitude)
    
    print(f"Omega: {omega:.3f}")
    print(f"H(jω) = {magnitude:.3f}")
    print(f"Decibel: {decibel:.3f}")

# Example usage
numbers_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
frequency = 1000  # 1 kHz
R = 8200  # 1 kOhm
C = 10 * 10 ** -9  # 10 nF
i = 0

fourier_transform_triangle_wave(numbers_array)
print("")
fourier_transform_sawtooth_wave(numbers_array)
print("")
for i in range(len(numbers_array)):
    print(f"\nn: {numbers_array[i]}")
    transfer_function_low_pass_filter(frequency, i, R, C)