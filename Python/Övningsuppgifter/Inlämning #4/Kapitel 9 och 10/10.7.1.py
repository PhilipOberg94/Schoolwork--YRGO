# 10.7 Övningar med funktioner
# Uppgift 1
#
# Kopiera programmet som läser in filen alice.txt. Gör om programmet så att det hämtar filen direkt från internet 
# tag hjälp av boken på sidan 206.
#
# Skapad av: Philip Öberg
# Datum:2024-08-27
#
#!/usr/bin/env python3
import urllib.request

rakna = dict()
try:
        # Vi börjar med att skapa ett objekt
    url = urllib.request.urlopen("https://gaia.cs.umass.edu/wireshark-labs/alice.txt")

    # Nu läser vi in HTML-dokumentet
    html = url.read()

    # Därefter måste vi omkoda byten till en sträng för att
    # t.ex. radbrytningar ska fungera korrekt
    htmlUtf = html.decode("utf-8")

except FileNotFoundError or ValueError:
    print("\nDenna fil finns inte")
else:
    innehall = htmlUtf
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
