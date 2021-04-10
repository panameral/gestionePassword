from cryptography.fernet import Fernet
from sys import exit
from os.path import isfile

def genera_chiave_fernet():
    return Fernet.generate_key()

class Crittografia:
    def __init__(self, key):
        self.key = Fernet(key)

    def critta(self, passwords):
        lista_temp = []
        for plat in passwords.keys():           #questo ciclo serve per trasformare il dizionario in una lista "lineare", in modo da poterla poi trasformare
            lista_temp.append(plat)             #in una stringa da poter criptare e scrivere su file
            for up in passwords[plat]:
                lista_temp.append(up)

        mj = " ".join(lista_temp)
        mc = self.key.encrypt(mj.encode())      #cripta il "messaggio" contenente piattaforme, user e password usando la libreria Fernet
        try:
            with open('password', 'wb') as fw:      #trascrive il "messaggio" criptato
                fw.write(mc)
        except:
            exit("» C'è stato qualche problema con la scrittura del file delle password!")

    def decritta(self):
        mc = ''
        mf = ''
        list_temp = []
        up = ['', '']
        key = ''
        passwords = {}

        try:
            with open('password', 'rb') as fr:
                mf = fr.read()

            mc = self.key.decrypt(mf)
            messaggio = mc.decode()
            list_temp = messaggio.split(" ")         #Usando la libreria Fernet, trasforma il messaggio criptato preso dal file 'password' e lo trasforma in una lista

            for i in range(0, len(list_temp), 3):    #Trasforma la lista di prima in un dizionario su cui poter lavorare in modo più efficiente
                key = list_temp[i]
                up[0] = list_temp[i+1]
                up[1] = list_temp[i+2]
                passwords.update({key: up})

            return passwords
        except:
            exit("» C'è stato qualche problema con la lettura del file delle password!")
