# 7.7 Övningar med loopar
# Uppgift 4
# 
# Skriv ett program som skriver ut en tabell över alla primtalen 
# upp till angivet tal. Till exempel alla primtal som finns upp 
# till 100.
# 
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#
tal = int(input("Vilket tal? "))
nytt_tal = (tal - 1)

for ii in range(2,tal):
    is_prime = True
    for i in range(2, ii-1):
        prime_check = (ii%i)
        if (prime_check == 0):
            is_prime = False
            break
    if (is_prime == True):
        print(ii)
