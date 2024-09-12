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
import os
import pickle
import sys

FILE_NAME = 'top10.pkl'

try:
    if os.path.exists(FILE_NAME):
        load_choice = input("Vill du ändra något i listan? (j/n): ")
        if load_choice == 'j':
            top_list = []
            print("Ange din topplista 1 - 10.")
            for i in range(1, 11):
                item = input(f"{i}: ")
                top_list.append(item)
            with open(FILE_NAME, 'wb') as file:
                pickle.dump(top_list, file)
        elif load_choice == 'n':
            with open(FILE_NAME, 'rb') as file:
                top_list = pickle.load(file)
        else:
            sys.exit("Var god svara (j)a eller (n)ej")
    else:
        raise FileNotFoundError

except FileNotFoundError:
    print("Fil saknas. Vänligen ange din topplista 1 - 10.")
    top_list = []
    for i in range(1, 11):
        item = input(f"{i}: ")
        top_list.append(item)
    with open(FILE_NAME, 'wb') as file:
        pickle.dump(top_list, file)

# Display the list and allow modifications
while True:
    print("\nTop 10 Lista:")
    for i, item in enumerate(top_list, start=1):
        print(f"{i}\t{item}")

    choice = input("\nVälj siffra för att ändra värde (0 för att avsluta): ")

    if choice == '0':
        break
    elif choice.isdigit() and 1 <= int(choice) <= 10:
        new_value = input(f"Ange nytt värde för plats {choice}: ")
        top_list[int(choice) - 1] = new_value
        with open(FILE_NAME, 'wb') as file:
            pickle.dump(top_list, file)
    else:
        print("Ogiltigt val. Vänligen ange en siffra mellan 0 och 10.")