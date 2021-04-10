from Funzioni import pulisci_schermo
from Crittografia import Crittografia, genera_chiave_fernet
from os.path import isfile
from string import ascii_letters, digits, punctuation
from random import choice


def generaPassword():
    caratteri = ascii_letters + digits          #Insieme di tutte le lettere e tutti i numeri (alfabeto inglese)
    simboli = caratteri + punctuation           #Qui oltre alle lettere e ai numeri di prima, si aggiungono una serie di simboli da poter scegliere per 
                                                    #la generazione casuale della password

    scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
    numero = input("Inserire numero caratteri: ")
    
    p = ''
    if scelta == "1":             
        for i in range(int(numero)+1):
            p += choice(caratteri)
    elif scelta == "2":      
        for i in range(int(numero)+1):
            p += choice(simboli)
    
    return p

def carica_chiave():
    if isfile("./key"):                 #Se il file della chiave esiste, lo apre semplicemente e lo ritorna come istanza, altrimenti prima genera il file e
        try:                            #poi lo ritorna comunque come istanza
            with open('key', 'rb') as fileK:
                return fileK.read()
        except:
            exit("» C'è stato qualche problema con la lettura della chiave")
    else:       
        #Generazione del file della chiave
        try:
            with open('key', 'wb') as fileK:
                chiave_fernet = genera_chiave_fernet()
                fileK.write(chiave_fernet)
        except:
            exit("» C'è stato qualche problema con la generazione della chiave")
                
        #Apertura del file della chiave
        try:
            with open('key', 'rb') as fileK:
                return fileK.read()
        except:
            exit("» C'è stato qualche problema con la lettura della chiave")
        
class GestisciPassword:
    def __init__(self):
        self.crypto = Crittografia(carica_chiave())

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
                up[1] = generaPassword()
            passwords.update({cerca: up})
        else:
            pulisci_schermo()
            print(f"» {plat} non risulta nel database!")
        return passwords

    def leggi(self, passwords):                                 #Stessa impostazione del metodo "modifica"
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            up = passwords[cerca]
            print("L'username richiesto è: " + up[0])
            print("La password richiesta è: " + up[1])
        else:
            pulisci_schermo()
            print(f"» {plat} non risulta nel database!")
    
    def aggiungi(self, passwords):                      
        plat = input("Quale piattaforma? ").lower()
        user = input("Inserisci Username nuovo: ")

        pulisci_schermo()
        p = generaPassword()
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
        if isfile("./password"):                 #Se il file delle password esiste, lo apre semplicemente e ritorna le password come lista
            return self.crypto.decritta()       #altrimenti crea la lista
        else:
            #Generazione della lista delle password
            passwords = {}
            plat = input("» Non c'è memorizzata nessuna password! Memorizzane una!\nQuale piattaforma? ").lower()
            user = input("Inserisci Username nuovo: ")

            pulisci_schermo()

            print("La password verrà generata automaticamente, scegli però alcune opzioni")
            #Processo di generazione automatico della password
            p = generaPassword()

            list_temp = [user, p]
            passwords.update({plat: list_temp})

            return passwords
    
    def salva(self, passwords):
        self.crypto.critta(passwords)
