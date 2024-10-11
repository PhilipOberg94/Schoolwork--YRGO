import husdjur

from husdjur import *

hund1 = Hund('Kalle',farg='svart', ras ='varg' )
hund2 = Hund('Knatte',farg='blå', ras ='cockerspaniell' )
hund3 = Hund('Fnatte',farg='gul', ras ='husky' )
hund4 = Hund('Tjatte',farg='rosa', ras ='labrador' )
hund5 = Hund('VonAnka',farg='lila', ras ='schäfer' )
hund6 = Hund('Musse-pigg',farg='svart', ras ='pudel' )

hundar = {hund1,hund2,hund3,hund4,hund5,hund6}

for i in hundar:
    print(i.vilkenRas())