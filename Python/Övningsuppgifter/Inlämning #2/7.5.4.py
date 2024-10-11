# 7.5 Övningar med villkor & jämförelser
# Uppgift 4
# Skriv ett program som läser in två flyttal med input() och multiplicerar 
# de två talen. Om produkten blir mindre än 50 ska texten "Ett litet tal" 
# skrivas ut. Om produkten är större än 100 ska texten "Ett medelstort tal" 
# skrivas ut. Om produkten är större än 200 men mindre än 500 skall texten
# "Ett stort tal" skrivas ut. Om talet är utanför dessa gränser skall texten
# "Ett gigantiskt tal" skrivas ut.
#
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#
flyttal1 = input("Första talet: ")
flyttal2 = input("Andra talet: ")

produkt = float(flyttal1) * float(flyttal2)

if (produkt < 50):
    print("Ett litet tal")
elif (produkt > 100) and (produkt < 200):
    print ("Ett medelstort tal")
elif (produkt > 200) and (produkt < 500):
    print("Ett stort tal")
else:
    print("Felaktigt tal")