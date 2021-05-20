
from base64 import urlsafe_b64encode
from Funzioni import regola, esci_con_messaggio
from cryptography.fernet import Fernet


def genera_chiave_fernet(passphrase):
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
        for plat in passwords.keys():           #questo ciclo serve per trasformare il dizionario in una lista "lineare", in modo da poterla poi trasformare
            lista_temp.append(plat)             #in una stringa da poter criptare e scrivere su file
            for up in passwords[plat]:
                lista_temp.append(up)

        mj = "\n".join(lista_temp)
        mc = self.key.encrypt(mj.encode())      #cripta il "messaggio" contenente piattaforme, user e password usando la libreria Fernet

        with open(self.file_name, 'wb') as fw:      #trascrive il "messaggio" criptato
            fw.write(mc)

    def decritta(self):
        mc = ''
        mf = ''
        list_temp = []
        pt = []
        up = ['', '']
        key = ''

        keys = []
        users = []
        passess = []

        passwords = {}

        with open(self.file_name, 'rb') as fr:
            mf = fr.read()
        mc = self.key.decrypt(mf)
        messaggio = mc.decode()

        list_temp = messaggio.split("\n")         #Usando la libreria Fernet, trasforma il messaggio criptato preso dal file 'password' e lo trasforma in una lista

        int_lista_size = (int(len(list_temp)/3))*3
        list_temp = regola(list_temp, int_lista_size, len(list_temp))

        for i in range(0, len(list_temp), 3):  # Fare tre liste ordinate in modo da avere piattaforma, user e password in 3 diverrse liste su cui lavorare dopo
            keys.append(list_temp[i].lower())
        for i in range(1, len(list_temp), 3):
            users.append(list_temp[i])
        for i in range(2, len(list_temp), 3):
            passess.append(list_temp[i])

        if len(keys) != len(users) and len(keys) != len(passess):
            print(f"Piattaforme: {len(keys)}\nUtenti: {len(users)}\nPassword: {len(passess)}")
            esci_con_messaggio("» C'è stato qualche problema con il caricamento!")

        for i in keys:
            if keys.count(i) > 1 and i not in pt:
                    pt.append(i)

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
