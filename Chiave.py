from cryptography.fernet import Fernet
from sys import exit

def apri_chiave():
    try:
        with open('key', 'rb') as fileK:
            return fileK.read()
    except:
         exit("» C'è stato qualche problema con la lettura della chiave")

def genera_chiave():
    try:
        with open('key', 'wb') as fileK:
            fileK.write(Fernet.generate_key())
    except:
        exit("» C'è stato qualche problema con la generazione della chiave")