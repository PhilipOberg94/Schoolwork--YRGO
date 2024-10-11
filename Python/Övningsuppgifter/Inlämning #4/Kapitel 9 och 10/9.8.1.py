# 9.8 Övningar med funktioner
# Uppgift 1
#
# Skriv in programmet "ränta på ränta" på sidan 173
# Testa att köra det och försök förstå hur det är uppbyggt och hur det fungerar.
# 
# Skapad av: Philip Öberg
# Datum:2024-08-27
#
#!/usr/bin/env python3

def ranta(kr, ranta, ar):
    ranta = (ranta / 100) + 1
    svar = kr * ranta ** ar
    return svar

pengar = float(input("Ange hur mycket pengar du har på kontot: "))
procentRanta = float(input("Ange ränta i procent: "))
antalAr = float(input("Hur många år ska pengarna stå på kontot? "))

# Spara till variabel och använd i print
tot = ranta(ar=antalAr, ranta=procentRanta, kr=pengar)
print("Jag har", tot, "kr på kontot efter", antalAr, "år")

# Samma funktion, fast med andra värden
print("Med 30000 kr med 3% ränta har du", ranta(30000, 3, 8), "kr efter 8 år")

# Använd i en ny beräkning
print("Dubbelt upp blir", (ranta(pengar, procentRanta, antalAr) * 2))
