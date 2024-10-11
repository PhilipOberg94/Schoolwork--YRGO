# 7.7 Övningar med loopar
# Uppgift 2
# 
# Skriv ett liknande program som ovan, men denna gången ska
# utskriften ske baklänges. Strängen som du ger till programmet 
# ska fortfarande vara "hejsan", men programmet ska skriva ut 
# den baklänges. Ett teckan per rad så att utskriften kommer att 
# se ut såhär:
# 
# n
# a
# s
# j
# e
# h
#
# Skapad av: Philip Öberg
# Datum: 2024-08-22
#

hej = "hejsan"
for i in reversed(hej):
    print(i)
