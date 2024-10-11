# 7.5 Övningar med villkor & jämförelser
# Uppgift 1
#
# Gör om övningen från kapitlet om datayper med Celsius Fahrenheit-omvandlingen
# till att nu ochså innehålla villkorlig kod. Om temperaturen blir högre än 80
# grader ska programmet skriva ut "Det är varmt". Om temperaturen i Fahrenheit 
# istället blir under 40 grader ska programmet skriva ut "Det är kallt". Tänk på
# att du nu måste spara gradtalet i Fahrenheit i en ny variabel. Använd gärna
# också input().
#
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#
c = 40
f = c * 1.8 + 32
print(f)
if (f > 80):
    print("Det är varmt")
elif (f < 40):
    print("Det är kallt")
