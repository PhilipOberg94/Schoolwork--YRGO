# 7.7 Övningar med loopar
# Uppgift 1
# 
# Skriv ett program som skriver ut alfabetet på skärmen 
# upp till angivet tal. Exempelvis om användaren anger 4
# ska programmet skriva ut "a b c d". Det är okey om 
# utskriften sker med ett tecken per rad.
# 
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#
number = int(input("Vilken siffra i alfabetet? "))
ok_number = False
if (number >= 1) and (number <= 26):
    ok_number = True
else:
    print("Denna bokstav finns inte")
if ok_number == True:
    for i in range(1,number + 1):
        ascii_tal = chr(i + 96)
        print(f"{ascii_tal}")
