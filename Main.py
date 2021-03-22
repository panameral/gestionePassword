from GestisciPassword import GestisciPassword
from os.path import isfile
import Chiave
from sys import exit
from os import system

if isfile("./key"):
    key = Chiave.apri_chiave()
else:
    Chiave.genera_chiave()
    key = Chiave.apri_chiave()

gestisci = GestisciPassword(key)
passwords = ''
scelta = ''

if isfile("./password"):
    passwords = gestisci.listaPasswords()
else:
    passwords = gestisci.crea()

while scelta != "7":
    print("\n*************************")
    print("1. Lista Piattaforme")
    print("2. Leggi User o Password")
    print("3. Modifica Password")
    print("4. Aggiungi Password")
    print("5. Elimina Password")
    print("6. Generare una Password")
    print("7. Esci")
    scelta = input().lower()
    system("clear")
    if scelta == "1":
        gestisci.listaPiattaforme(passwords)
    elif scelta == "2":
        gestisci.leggi(passwords)
    elif scelta == "3":
        gestisci.modifica(passwords)
    elif scelta == "4":
        gestisci.aggiungi(passwords)
    elif scelta == "5":
        gestisci.elimina(passwords)
    elif scelta == "6":
        gestisci.generaPassword()
    elif scelta == "7":
        exit("» Grazie per aver utilizzato il programma!")
    else:
        print("Le opzioni sono i numeri da 1 a 7!")