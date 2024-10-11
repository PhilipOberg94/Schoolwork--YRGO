# 7.7 Övningar med loopar
# Uppgift 3
# 
# Skriv ett program som talar om ifall ett angivet tal är ett 
# primtal eller inte. Det enklaste sättet att få reda på ifall 
# ett tal är ett primtal är att dela talet med alla tal mellan 
# två och sig själv minus 1. Om vi ska ta reda på om talet sju 
# är ett primtal delar vi talet sju med alla tal från två till 
# sex. Om något av dessa får svaret 0 i rest är talet inte ett 
# primtal. Om däremot inget svar får noll i rest är 
# talet ett primtal.
#
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#
tal = int(input("Vilket tal? "))
nytt_tal = (tal - 1)

if (tal < 2):
    print("Detta är inte ett primtal")
elif (tal == 3) or (tal == 2):
    print("Detta är ett primtal")
else:
    for i in range(2, nytt_tal):
        primtal = (tal%i)
        if (primtal == 0):
            break
    if (primtal == 0):
        print("Detta är inte ett primtal")
    else:
        print("Detta är ett primtal")