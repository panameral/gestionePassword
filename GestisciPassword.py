from os.path import isfile
from random import choice
from string import ascii_letters, digits
from pyperclip import copy as copia
import cryptography

from Crittografia import Crittografia, genera_chiave_fernet
from Funzioni import pulisci_schermo, esci_con_messaggio, regola, elementi_lista_non_unici


def generaPassword():
    scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
    numero = input("Inserire numero caratteri: ")
    
    p = ''
    if scelta == "1":             
        for i in range(int(numero)+1):
            l = choice(range(2))
            if l == 0:
                p += choice(ascii_letters)
            elif l == 1:
                p += choice(digits)
    elif scelta == "2":      
        for i in range(int(numero)+1):
            l = choice(range(3))
            if l == 0:
                p += choice(ascii_letters)
            elif l == 1:
                p += choice(digits)
            elif l == 2:
                p += choice("@#$!%*?&_")

    copia(p)
    print("Password generata e copiata pronta per poterla incollare!")
    return p
        
class GestisciPassword:
    file_name = "./password"

    def __init__(self, passphrase):
        self.crypto = Crittografia(genera_chiave_fernet(passphrase), self.file_name)

    def listaPiattaforme(self, passwords):
        print("Le piattaforme sono:")
        for platform in passwords.keys():           #Le piattaforme sono come nome delle chiavi del dizionario "passwords"
            print(f"-> {platform}")

    def modifica(self, passwords):
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            up = passwords[cerca]                                   #Essendo che la piattaforma è la chiave l'user e la password sono una lista di due elementi 
            scelta = input("User (u) o Password (p)? ").lower()         #impostati come valore del dizionario, allora prendo il valore della chiave e lavoro su di esso
            if scelta == "u":
                up[0] = input("Inserisci Username nuovo: ")
            elif scelta == "p":
                auto_manuale = input("La password vuoi sia generata (g) o la vuoi inserire manualmente (m)?")
                pulisci_schermo()
                if auto_manuale == "g" or auto_manuale == "generata" or auto_manuale == "genera":
                    up[1] = generaPassword()
                elif auto_manuale == "m" or auto_manuale == "manuale" or auto_manuale == "manualmente":
                    up[1] = input("Inserisci la tua password: ")
                pulisci_schermo()
            else:
                print("Riprendi la modifica ricordando che puoi scegliere solo User (u) o Password (p)")
            passwords.update({cerca: up})
        else:
            pulisci_schermo()
            print(f"» {plat} non risulta nel database!")
        return passwords

    def carica_da_file_in_chiaro(self):
        messaggio = ''
        list_temp = []

        keys = []
        users = []
        passess = []

        passwords = {}

        with open("./password_in_chiaro", 'rt') as fr:
            messaggio = fr.read()

        list_temp = messaggio.split('\n')  #Trasforma il messaggio preso dal file 'password' e lo trasforma in una lista
        int_lista_size = (int(len(list_temp)/3))*3
        list_temp = regola(list_temp, int_lista_size, len(list_temp))

        for i in range(0, len(list_temp), 3):  # Fare tre liste ordinate in modo da avere piattaforma, user e password in 3 diverrse liste su cui lavorare dopo
            keys.append(list_temp[i].lower())
        for i in range(1, len(list_temp), 3):
            users.append(list_temp[i])
        for i in range(2, len(list_temp), 3):
            passess.append(list_temp[i])

        pt = elementi_lista_non_unici(keys)

        if len(keys) != len(users) and len(keys) != len(passess):
            print(f"Lista Size: {len(list_temp)}\nPiattaforme: {len(keys)}\nUtenti: {len(users)}\nPassword: {len(passess)}")
            esci_con_messaggio("» C'è stato qualche problema con il caricamento!")

        for i in pt:
            dp = 0
            for j in range(len(keys)):
                if i == keys[j]:
                    dp += 1
                    nome_utente = users[j]
                    passwd = passess[j]
                    piattaforma = keys[j] + str(dp)
                    passwords.update({piattaforma: [nome_utente, passwd]})

        for i in range(len(keys)):
            if keys[i] in pt:
                continue
            else:
                piattaforma = keys[i]
                nome_utente = users[i]
                passwd = passess[i]
                passwords.update({piattaforma: [nome_utente, passwd]})

        return passwords

    def leggi(self, passwords):         #Stessa impostazione del metodo "modifica"
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()

        if cerca in passwords:
            up = passwords[cerca]
            user = up[0]
            passwd = up[1]
            print("L'username richiesto è: " + user)
            print("La password richiesta è: " + passwd)

            scegli = input("Vuoi copiare l'informazione per poterlo incollare poi? ")
            if scegli == "s" or scegli == "si":
                cosa = input("Cosa vuoi copiare user (u) o password (p)? ")
                if cosa == "u" or cosa == "user":
                    copia(user)
                elif cosa == "p" or cosa == "password":
                    copia(passwd)
        else:
            pulisci_schermo()
            print(f"» {plat} non risulta nel database!")
    
    def aggiungi(self, passwords):                      
        plat = input("Quale piattaforma? ").lower()
        user = input("Inserisci Username nuovo: ")
        p = ''
        auto_manuale = input("La password vuoi sia generata (g) o la vuoi inserire manualmente (m)?")
        pulisci_schermo()
        if auto_manuale == "g" or auto_manuale == "generata" or auto_manuale == "genera":
            p = generaPassword()
        elif auto_manuale == "m" or auto_manuale == "manuale" or auto_manuale == "manualmente":
            p = input("Inserisci la tua password: ")
        pulisci_schermo()
        list_temp = [user, p]                   #questa lista racchiude user e password che saranno impostati come valore del dizionario,
        passwords.update({plat: list_temp})     #la cui chiave sarà la piattaforma legata ad essi

        return passwords

    def elimina(self, passwords):
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            passwords.pop(cerca)
            pulisci_schermo()
            print(f"» I dati di {plat} sono stati eliminati!")
            return passwords
        else:
            pulisci_schermo()
            print(f"» {plat} non risulta nel database!")
            return passwords

    def carica(self):
        if isfile(self.file_name):                 #Se il file delle password esiste, lo apre semplicemente e ritorna le password come lista
            try:
                return self.crypto.decritta()       #altrimenti crea la lista
            except (cryptography.fernet.InvalidToken, TypeError):
                esci_con_messaggio("» Password errata!\n» Riavvia e riprova!");
        else:
            #Generazione della lista delle password
            passwords = {}
            chiaro = input("» Non c'è memorizzata nessuna password: vuoi caricare da un file in chiaro? ").lower()

            if chiaro == "si" or chiaro == "s":
                pulisci_schermo()
                return self.carica_da_file_in_chiaro()
            else:
                plat = input("» Memorizza una password!\nPer quale piattaforma? ").lower()
                user = input("Inserisci Username nuovo: ")

                pulisci_schermo()

                print("La password verrà generata automaticamente, scegli però alcune opzioni")
                #Processo di generazione automatico della password
                p = generaPassword()

                list_temp = [user, p]
                passwords.update({plat: list_temp})

                pulisci_schermo()

                return passwords
    
    def salva(self, passwords):
        pulisci_schermo()
        self.crypto.critta(passwords)
