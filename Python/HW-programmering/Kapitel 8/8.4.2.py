# 8.4 Filhantering och felhantering
# Uppgift 2
# 
# Skriv in Alice-programmet på sidan 138-139 och se till att följande funktioner läggs till
# - Man skall få frågan vilken fil man vill öppna.
# - Lägg till felhantering, om man matar in något felaktig fil, exempelvis någon som inte finns. 
#   Skall ett felmeddelande visas, annars läses filen in för att undersöka vilka ord som är mest förekommande.
#
# Skapad av: Philip Öberg
# Datum: 2024-08-26
#

rakna = dict()
try:
    fil = str(input("Vilken fil vill du öppna?"))
    fil = open(fil, 'r')
except FileNotFoundError or ValueError:
    print("\nDenna fil finns inte")
else:
    innehall = fil.read()
    innehall = innehall.replace(",", " ").replace(".", " ") \
                    .replace("'", " ").lower()

    ord = innehall.split()

    for o in ord:
        if o not in rakna:
            rakna[o] = 1
        else:
            rakna[o] = rakna[o] + 1

    omvand = dict()
    for k, v in rakna.items():
        omvand[v] = k

    sorterad = sorted(omvand.items(), reverse=True)

    hogsta = 0
    for i, j in sorterad:
        print(j, "\t", i)
        hogsta = hogsta + 1
        if hogsta == 10:
            break