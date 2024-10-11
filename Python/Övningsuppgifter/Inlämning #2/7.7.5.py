# 7.7 Övningar med loopar
# Uppgift 5
# 
# Skriv ett program som skriver ut en tabell över alla värden 
# för volymen hos kuber vars sidor är mellan en och femton meter. 
# Exempelvis en kub med en metersida får volymen 1**3 = 1m3. 
# Volymen hos en kub vars ena sida är 3 meter blir 3**3 = 27m3. 
# Exempel på tabellens utseende:
# 1 meter sida = 1 kubikmeter
# 2 meter sida = 8 kubikmeter
# 3 meter sida = 27 kubikmeter
# osv....
# 
# Skapad av:Philip Öberg
# Datum: 2024-08-22
#
for i in range(1,15):
    tal = (i**3)
    print(str(i) + "meter sida = " + str(tal) + "kubikmeter")