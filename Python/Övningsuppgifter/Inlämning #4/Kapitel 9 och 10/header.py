# 9.8 Övningar med funktioner
# Uppgift 4
#
# Skapa funktionerna:
# getU(p, r, i) #returnerar volt
# getR(p, u, i) #returnerar ohm
# getI(p, r, u) #returnerar ampare
# getP(u, r, i) #returnerar watt
#
# För att räkna ut de olika enheterna krävs två av de andra, du kan exempelvis bestämma att 
# om man använder en funktion såhär ohm = getR("",12,0.3) så skall uträkningen göras med spänning och ström.
#
# Är du osäker på ohms lag, så googla.
#
# se till att ha med funktionsbeskrivningar enligt sidorna 183 - 185.
# Skapad av: Philip Öberg
# Datum:2024-08-27
#
def getU (p,r,i):
    if p == "": #Denna if-sats gångrar resistansen med strömmen
        volt = r*i 
        return volt
    elif r == "": #Denna if-sats delar effekten med strömmen
        volt = p/i
        return volt
    elif i == "": #Denna if-sats tar roten ur effekten gånger resistansen
        volt = (r*p)**0.5
    else:
        volt = (-1)
    return volt
