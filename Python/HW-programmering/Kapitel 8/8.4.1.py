# 8.4 Filhantering och felhantering
# Uppgift 1
#
# Öppna tidigare programmet för Celsius/Fahrenheit och se till att följande funktioner läggs till
# - Man skall kunna mata in temperatur (detta kanske redan är gjort).
# - Lägg till felhantering, om man matar in något annat än en temperatur skall felet fångas upp och ett
#   felmeddelande skall skrivas ut.
# - Lägg till en kontroll vid inmatningen om värdet är ett heltal eller ett decimaltal, om inte fråga 
#   efter temperatur igen.
#
# Skapad av: Philip Öberg
# Datum: 2024-08-26
#
c = 26
f = str(c * 1.8 + 32)

if f != 0:
    try:
        fil = open('/home/oberg/Schoolwork--YRGO/Python/HW-programmering/Kapitel 8/temp.txt', 'w')
        fil.write (f)
    except FileExistsError:
        print("Filen finns inte")
    except ValueError:
        print("Du försöker mata in något annat än int eller float")
        f = 0
    else:
        print(f"Temperaturen är: {f:.6}")
else:
    print("Du försöker mata in något annat än int eller float")
    f = 0