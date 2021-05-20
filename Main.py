import sys

from GestisciPassword import GestisciPassword, generaPassword
from Funzioni import esci_con_messaggio, menu, pulisci_schermo
from getpass import getpass

passphrase = getpass(prompt="Inserisci Password: ")
gestisci = GestisciPassword(passphrase)
passwords = gestisci.carica()
pulisci_schermo()

while True:
    menu()
    scelta = input()

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
        print(generaPassword())
    elif scelta == "7":
        passwords = gestisci.carica_da_file_in_chiaro()
    elif scelta == "8":
        gestisci.salva(passwords)
        esci_con_messaggio("» Grazie per aver utilizzato il programma!")    
    else:
        print("Le opzioni sono i numeri da 1 a 8")
