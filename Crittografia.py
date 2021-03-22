from cryptography.fernet import Fernet
from sys import exit

class Crittografia():
    def __init__(self, key):
        self.key = Fernet(key)

    def critta(self, messaggio):
        mj = " ".join(messaggio)
        mc = self.key.encrypt(mj.encode())
        try:
            with open('password', 'wb') as fw:
                fw.write(mc)
        except:
            exit("» C'è stato qualche problema con la scrittura del file delle password!")

    def decritta(self):
        mc = ''
        mf = ''
        try:
            with open('password', 'rb') as fr:
                mf = fr.read()
            mc = self.key.decrypt(mf)
            messaggio = mc.decode()
            return messaggio.split(" ")
        except:
            exit("» C'è stato qualche problema con la lettura del file delle password!")