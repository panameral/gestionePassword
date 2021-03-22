from Crittografia import Crittografia

class ListaPass:
    def __init__(self, key):
        self.cry = Crittografia(key)

    def scriviPassword(self, messaggio):
        self.cry.critta(messaggio)
        
    def leggiPassword(self):
        return self.cry.decritta()