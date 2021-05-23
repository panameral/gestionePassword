from os.path import isfile
from random import choice
from string import ascii_letters, digits
from pyperclip import copy as copia
import cryptography

from Crittografia import Crittografia, genera_chiave_fernet
from Funzioni import pulisci_schermo, esci_con_messaggio, regola, elementi_lista_non_unici, intToPlat

#generaPassword() genera una password (alfanumerica o con aggiunta di alcuni simboli,
#a seconda della scelta dell'utente) in modo casuale, per poi copiarla nella clipboard
#pronta per poter essere incollata da parte dell'utente dove ritiene utile.
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
            # sceglie in modo casuale se generare un carattere numerico o dell'alfabeto oppure un simbolo scelto tra qeusti "@#$!%*?&_"
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
        counter = 0
        #stampa a video la lista di tutte le piattaforme memorizzate (chiavi del dizionario 'passwords')
        #dando pure un contatore a ciascuna di esse in modo da poter selezionare facilmente.
        for platform in passwords.keys():           #Le piattaforme sono come nome delle chiavi del dizionario "passwords"
            counter += 1
            print(f"{counter} -> {platform}")

    def modifica(self, passwords):
        #mostra le piattaforme con i corrispettivi indici che, una volta selezionato l'indice,
        #verrà usato per prendere il nome della piattaforma interessata
        pulisci_schermo()
        self.listaPiattaforme(passwords)

        plat = ''
        try:
            plat = input("Inserisci numero relativo alla piattaforma: ")
            cerca = intToPlat(passwords.keys(), int(plat))
        except ValueError:
            plat = input("Per favore inserisci un numero che sia tra quelli mostrati relativi alle piattaforme: ")
            cerca = intToPlat(passwords.keys(), int(plat))

        if cerca in passwords:
            up = passwords[cerca]
            print(cerca)
            scelta = input("User (u) o Password (p)? ").lower()

            if scelta == "u":
                up[0] = input("Inserisci Username nuovo: ")
            elif scelta == "p":
                auto_manuale = input("La password vuoi sia generata (g) o la vuoi inserire manualmente (m)?").lower()
                pulisci_schermo()
                if auto_manuale == "g" or auto_manuale == "generata" or auto_manuale == "genera":   #nel caso l'utente inserisca 'genera' o 'generata' invece di 'g'
                    up[1] = generaPassword()
                elif auto_manuale == "m" or auto_manuale == "manuale" or auto_manuale == "manualmente":     #nel caso l'utente inserisca 'manuale' o 'manualmente' invece di 'm'
                    up[1] = input("Inserisci la tua password: ")
                pulisci_schermo()
            else:
                #Se hai sbagliato basta riselezionare la modifica dal menù principale e poi scegliere correttamente
                print("Riprendi la modifica ricordando che puoi scegliere solo User (u) o Password (p)")
            passwords.update({cerca: up})
        else:
            pulisci_schermo()
            if cerca == '':
                print(f"» {plat} non risulta nel database!")
            else:
                print(f"» {cerca} non risulta nel database!")

        return passwords

    #la funzione sottostante serve all'utente per caricare in memoria
    #una lista di password opportunamente formattata e non criptata
    def carica_da_file_in_chiaro(self):
        messaggio = ''
        list_temp = []

        keys = []
        users = []
        passess = []

        passwords = {}

        try:
            with open("password_in_chiaro", 'rt') as fr:
                messaggio = fr.read()

            list_temp = messaggio.split('\n')  #Trasforma il messaggio preso dal file 'password' e lo trasforma in una lista

            int_lista_size = (int(len(list_temp)/3))*3

            #durante lo sviluppo si è presentato il problema della dimensione errata della
            #lista "splittata" precedentemente (probabilmente a causa di una newline)
            #e la seguente funzione sistema la cosa regolando la lista secondo la giusta dimensione
            list_temp = regola(list_temp, int_lista_size, len(list_temp))

            # Fare tre liste ordinate in modo da avere piattaforma, user e password in 3 diverrse liste su cui lavorare dopo
            for i in range(0, len(list_temp), 3):
                keys.append(list_temp[i])
            for i in range(1, len(list_temp), 3):
                users.append(list_temp[i])
            for i in range(2, len(list_temp), 3):
                passess.append(list_temp[i])

            #la seguente operazione serve a darmi una lista delle piattaforme con più di un utente
            pt = elementi_lista_non_unici(keys)

            #Essendo che ogni piattaforma ha almeno un nome utente e una password
            #è ovvio che le liste 'keys', 'users' e 'passess' devono essere della stessa dimensione
            if len(keys) != len(users) and len(keys) != len(passess):
                print(f"Lista Size: {len(list_temp)}\nPiattaforme: {len(keys)}\nUtenti: {len(users)}\nPassword: {len(passess)}")
                esci_con_messaggio("» C'è stato qualche problema con il caricamento!")

            # Se per una piattaforma ci sono più account, io me li segno aggiungendo
            # alla stringa della piattaforma "multipla" il nome utente
            for i in range(len(keys)):
                if keys[i] in pt:
                    piattaforma = keys[i] + " (" + users[i] + ")"
                    nome_utente = users[i]
                    passwd = passess[i]
                    passwords.update({piattaforma: [nome_utente, passwd]})
                else:
                    piattaforma = keys[i]
                    nome_utente = users[i]
                    passwd = passess[i]
                    passwords.update({piattaforma: [nome_utente, passwd]})

            return passwords
        except FileNotFoundError:
            print("File in chiaro non trovato!")
            print("Deve essere inserito nella stessa cartella del file Main.py con il nome \"password_in_chiaro\"!")


    def leggi(self, passwords):         #Stessa impostazione del metodo "modifica"
        pulisci_schermo()
        self.listaPiattaforme(passwords)

        plat = ''
        try:
            plat = input("Inserisci numero relativo alla piattaforma: ")
            cerca = intToPlat(passwords.keys(), int(plat))
        except ValueError:
            plat = input("Per favore inserisci un numero che sia tra quelli mostrati relativi alle piattaforme: ")
            cerca = intToPlat(passwords.keys(), int(plat))

        if cerca in passwords:
            up = passwords[cerca]
            user = up[0]
            passwd = up[1]
            pulisci_schermo()
            print(cerca)
            print("L'username richiesto è: " + user)
            print("La password richiesta è: " + passwd)

            #Se all'utente serve copiare la password per incollarla poi dove
            #ritiene opportuno, le seguenti operazioni rendono semplice ciò
            scegli = input("Copia user (u), password (p)?\nSe non vuoi copiare inserisci qualunque carattere e premi Invio: ").lower()
            if scegli == "u" or scegli == "user":
                copia(user)
            elif scegli == "p" or scegli == "password":
                copia(passwd)
        else:
            pulisci_schermo()
            if cerca == '':
                print(f"» {plat} non risulta nel database!")
            else:
                print(f"» {cerca} non risulta nel database!")
    
    def aggiungi(self, passwords):                      
        plat = input("Quale piattaforma? ")
        user = input("Inserisci Username nuovo: ")
        p = ''
        auto_manuale = input("La password vuoi sia generata (g) o la vuoi inserire manualmente (m)?").lower()

        pulisci_schermo()
        #si da la possibilità all'utente di inserire manualmente una password o di generarla in modo casuale
        if auto_manuale == "g" or auto_manuale == "generata" or auto_manuale == "genera":
            p = generaPassword()
        elif auto_manuale == "m" or auto_manuale == "manuale" or auto_manuale == "manualmente":
            p = input("Inserisci la tua password: ")
        pulisci_schermo()

        # questa lista racchiude user e password che saranno impostati come valore del dizionario, la cui chiave sarà la piattaforma legata ad essi
        list_temp = [user, p]
        passwords.update({plat: list_temp})

        return passwords

    def elimina(self, passwords):
        pulisci_schermo()
        self.listaPiattaforme(passwords)

        plat = ''
        try:
            plat = input("Inserisci numero relativo alla piattaforma: ")
            cerca = intToPlat(passwords.keys(), int(plat))
        except ValueError:
            plat = input("Per favore inserisci un numero che sia tra quelli mostrati relativi alle piattaforme: ")
            cerca = intToPlat(passwords.keys(), int(plat))

        if cerca in passwords:
            passwords.pop(cerca)
            pulisci_schermo()
            print(f"» I dati di {cerca} sono stati eliminati!")
            return passwords
        else:
            pulisci_schermo()
            if cerca == '':
                print(f"» {plat} non risulta nel database!")
            else:
                print(f"» {cerca} non risulta nel database!")
            return passwords

    def carica(self):
        # Se il file delle password esiste, lo apre semplicemente e ritorna le password come lista, altrimenti crea la lista
        if isfile(self.file_name):
            try:
                return self.crypto.decritta()
            except (cryptography.fernet.InvalidToken, TypeError):   #Nel caso di password errata
                esci_con_messaggio("» Password errata!\n» Riavvia e riprova!");
        else:
            #Generazione della lista delle password (o caricandola da un file in chiaro, o costruendola passo passo)
            passwords = {}
            chiaro = input("» Non c'è memorizzata nessuna password: vuoi caricare da un file in chiaro? ").lower()

            if chiaro == "si" or chiaro == "s":
                pulisci_schermo()
                return self.carica_da_file_in_chiaro()
            else:
                plat = input("» Memorizza una password!\nPer quale piattaforma? ")
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
