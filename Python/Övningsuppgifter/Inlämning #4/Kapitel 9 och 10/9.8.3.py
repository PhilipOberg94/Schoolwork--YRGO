# 9.8 Övningar med funktioner
# Uppgift 3
#
# Skapa en funktion som tar in tre heltal och returnerar en lista med de tre heltalen sorterade i stigande
# ordning(minsta till största)
# Skapa ett program som använder funktionen, användaren skall mata in tre värden och sedan skall en sorterad 
# utskrift ske. Funktionen SKALL användas
# 
#
# Skapad av:Philip Öberg
# Datum:2024-08-27
#
def number_list (hel1,hel2,hel3):
    list = [hel1,hel2,hel3]
    list.sort()
    return list

print(number_list(3,2,5))

