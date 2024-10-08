# 8.4 Filhantering och felhantering
# Uppgift 5
#
# Kopiera programmet för uppgift 3, lägg till felhantering för filöppning samt inmatning.
#
# Skapad av:Philip Öberg
# Datum:2024-08-27
#
import pickle
import sys

try:
    ladda = input("Vill du ladda tidigare kurs? (j/n): ")
    if ladda == "j":
        kurs = pickle.load(open('./kurs.p', 'rb'))
        print(f"Din aktuella kurs är : {kurs}")
    elif (ladda == "n"):
        kurs = float(input("Ange ny USD-kurs: "))
        pickle.dump(kurs, open('./kurs.p', 'wb'))
    else:
        sys.exit("Var god svara (j)a eller (n)ej")

    usd = float(input("Ange summa i USD: "))
    print ("%.2f USD motsvarar %.2f SEK" \
        %(usd,usd*kurs))
except FileExistsError:
    print("Filen du försöker öppna finns inte")
except Exception as i:
    print(f"Ett oväntat fel inträffade: {i}")
except ValueError:
    print("Inmatningsvärde felaktigt")
