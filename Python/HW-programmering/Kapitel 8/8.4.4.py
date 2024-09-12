# 8.4 Filhantering och felhantering
# Uppgift 4
# 
# Skapa ett program för att spara en 10-toplista över vad du vill. När man startar programmet visas en lista 1 - 10 på alla
# värden. Exempel nedan
#
# Världens största länder
# 1	Russia
# 2	Canada
# 3	China
# 4	United States
# 5	Brazil
# 6	Australia
# 7	India
# 8	Argentina
# 9	Kazakhstan
# 10	Algeria
# 
# Välj siffra för att ändra värde (0 för att avsluta)
#
# Om man ändrar ett värde skall samtliga värden sparas i en fil, dessa värden läses in direkt vid uppstart av programmet.
# Om filen som värden finns i saknas, be då användaren att skriva in sin fulla lista 1 - 10.
#
#
# Skapad av: Philip Öberg
# Datum: 2024-08-24
#
import pickle
import sys

ladda = input("Vill du ladda tidigare lista? (j/n): ")
if ladda == "j":
    kurs = pickle.load(open('country.p', 'rb'))
elif (ladda == "n"):
    
    for i in range(1,11):
        print("Ange land här: \n")
        lista = input(str(i) + " ")
        pickle.dump(lista, open('country.p', 'wb'))
else:
    sys.exit("Var god svara (j)a eller (n)ej")


# print ("%.2f USD motsvarar %.2f SEK" \
#        %(usd,usd*kurs))