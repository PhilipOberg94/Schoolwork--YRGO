# 9.8 Övningar med funktioner
# Uppgift 2
#
# Gör om uppgift 1 och se till att utskriften enbart sker med 2 decimaler.
#
# Skapad av: Philip Öberg
# Datum:2024-08-27
#
def ranta(kr, ranta, ar):
    ranta = (ranta / 100) + 1
    svar = kr * ranta ** ar
    return round(svar,3)

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