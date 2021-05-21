
from base64 import urlsafe_b64encode
from Funzioni import regola, esci_con_messaggio, elementi_lista_non_unici
from cryptography.fernet import Fernet


def genera_chiave_fernet(passphrase):
    #questa funzione genera una chiave nel modo richiesto dalla libreria Fernet
    #cioè una chiave in byte con base64 e 32 caratteri. Qui si opera in modo che
    #da una stringa precedentemente scelta come passphrase si impone la struttura
    #richiesta dalla libreria Fernet.

    char = 'GK5n4SbqDOzB160q2pm3X5lRu5L1cAzy'

    if len(passphrase) < 32:
        for count in range(len(char) - len(passphrase)):
            passphrase += char[count]
    elif len(passphrase) > 32:
        temp = passphrase
        passphrase = temp[:32]

    return urlsafe_b64encode(passphrase.encode())

class Crittografia:
    file_name = "./passwords"

    def __init__(self, key, fileName):
        self.key = Fernet(key)
        self.file_name = fileName

    def critta(self, passwords):
        lista_temp = []

        #questo ciclo serve per trasformare il dizionario in una lista formata da piattaforma, user e password
        #in modo sequenziale, per poter poi trasformare la lista in una stringa da poter criptare e scrivere su file
        for plat in passwords.keys():
            lista_temp.append(plat)
            for up in passwords[plat]:
                lista_temp.append(up)

        #trasformo la lista in una stringa, scegliendo come "separatore" il carattere new-line
        mj = "\n".join(lista_temp)
        mc = self.key.encrypt(mj.encode())      #cripta il "messaggio" contenente piattaforme, user e password usando la libreria Fernet

        with open(self.file_name, 'wb') as fw:      #trascrive il "messaggio" criptato
            fw.write(mc)

    def decritta(self):
        messaggio = ''
        list_temp = []
        up = ['', '']
        key = ''

        keys = []
        users = []
        passess = []

        passwords = {}

        #prende il contetuto del file, lo decripta, lo decodifica e lo assegna
        #alla stringa 'messaggio' in modo da poter operare dopo
        with open(self.file_name, 'rb') as fr:
            messaggio = self.key.decrypt(fr.read()).decode()

        #Usando la libreria Fernet, trasforma il messaggio criptato preso dal file 'password' e lo trasforma in una lista
        list_temp = messaggio.split("\n")

        int_lista_size = (int(len(list_temp)/3))*3

        # durante lo sviluppo si è presentato il problema della dimensione errata della
        # lista "splittata" precedentemente (probabilmente a causa di una newline)
        # e la seguente funzione sistema la cosa regolando la lista secondo la giusta dimensione
        list_temp = regola(list_temp, int_lista_size, len(list_temp))

        # Fare tre liste ordinate in modo da avere piattaforma, user e password in 3 diverrse liste su cui lavorare dopo
        for i in range(0, len(list_temp), 3):
            keys.append(list_temp[i].lower())
        for i in range(1, len(list_temp), 3):
            users.append(list_temp[i])
        for i in range(2, len(list_temp), 3):
            passess.append(list_temp[i])

        # Essendo che ogni piattaforma ha almeno un nome utente e una password
        # è ovvio che le liste 'keys', 'users' e 'passess' devono essere della stessa dimensione
        if len(keys) != len(users) and len(keys) != len(passess):
            print(f"Piattaforme: {len(keys)}\nUtenti: {len(users)}\nPassword: {len(passess)}")
            esci_con_messaggio("» C'è stato qualche problema con il caricamento!")

        #la seguente operazione serve a darmi una lista delle piattaforme con più di un utente
        pt = elementi_lista_non_unici(list_temp)

        #Per l'inserimento delle piattaforme nel dizionario 'passwords', parto con quelle con più utenti e poi procedo con gli altri
        for i in pt:
            dp = 0
            for j in range(len(keys)):
                if i == keys[j]:
                    ++dp
                    piattaforma = keys[j]+str(dp)
                    nome_utente = users[j]
                    passwd = passess[j]
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
