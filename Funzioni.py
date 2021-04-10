from os import system
from sys import exit

def menu():
    print("""\n*************************
    1. Lista Piattaforme
    2. Leggi User o Password
    3. Modifica Password
    4. Aggiungi Password
    5. Elimina Password
    6. Generare una Password
    7. Salva e Esci""")

def pulisci_schermo():
    system("clear")

def esci_con_messaggio(messaggio):
    exit(messaggio)



