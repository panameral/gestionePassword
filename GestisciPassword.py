from string import ascii_letters
from string import digits
from string import punctuation
from random import choice
from ListaPass import ListaPass
from os import system

class GestisciPassword:
    def __init__(self, key):
        self.lp = ListaPass(key)

    def listaPiattaforme(self, passwords):
        print("Le piattaforme sono:")
        for i in range(len(passwords)):
            if i%3 == 0 or i == 0:
                print(f"-> {passwords[i]}")
    
    def generaPassword(self):
        caratteri = ascii_letters + digits
        simboli = caratteri + punctuation
        scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
        numero = input("Inserire numero caratteri: ")
        system("clear")
        print("La password da te richiesta è:")
        if scelta == "1":             
            for i in range(int(numero)):
                print(choice(caratteri), end='') 
        elif scelta == "2":      
            for i in range(int(numero)):
                print(choice(simboli), end='')

    def modifica(self, passwords):
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            indice = passwords.index(cerca)
            cerca = input("User (u) o Password (p)? ").lower()
            if cerca == "u":
                passwords[indice+1] = input("Inserisci Username nuovo: ")
            elif cerca == "p":
                caratteri = ascii_letters + digits
                simboli = caratteri + punctuation
                scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
                numero = input("Inserire numero caratteri: ")
                if scelta == "1":             
                    for i in range(int(numero)):
                        p += choice(caratteri)
                elif scelta == "2":      
                    for i in range(int(numero)):
                        p += choice(simboli)
                passwords[indice+2] = p
                self.lp.scriviPassword(passwords)
        else:
            system("clear")
            print(f"» {plat} non risulta nel database!")
        return passwords

    def leggi(self, passwords):
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            indice = passwords.index(cerca)
            cerca = input("User (u) o Password (p)? ")
            system("clear")
            if cerca == "u":
                print("L'username richiesto è:")
                print(passwords[indice+1])
            elif cerca == "p":
                print("La password richiesta è:")
                print(passwords[indice+2])
        else:
            system("clear")
            print(f"» {plat} non risulta nel database!")

    def crea(self):
        passwords = ['', '', '']
        plat = input("» Non c'è memorizzata nessuna password! Memorizzane una!\nQuale piattaforma? ")
        passwords[0] = plat.lower()
        passwords[1] = input("Inserisci Username nuovo: ")
        caratteri = ascii_letters + digits
        simboli = caratteri + punctuation
        system("clear")
        print("La password verrà generata automaticamente, scegli però alcune opzioni")
        scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
        numero = input("Inserire numero caratteri: ")
        password = ''
        if scelta == "1":             
            for i in range(int(numero)):
                password += choice(caratteri)
        elif scelta == "2":      
            for i in range(int(numero)):
                password += choice(simboli)
        passwords[2] = password
        self.lp.scriviPassword(passwords)
        system("clear")
        return passwords
    
    def aggiungi(self, passwords):
        plat = input("Quale piattaforma? ")
        piattaforma = plat.lower()
        passwords.append(piattaforma)
        user = input("Inserisci Username nuovo: ")
        passwords.append(user)
        caratteri = ascii_letters + digits
        simboli = caratteri + punctuation
        system("clear")
        scelta = input("1. Password alfanumerica\n2. Password alfanumerica con simboli\nInserire scelta: ")
        numero = input("Inserire numero caratteri: ")
        password = ''
        if scelta == "1":             
            for i in range(int(numero)):
                password += choice(caratteri)
        elif scelta == "2":      
            for i in range(int(numero)):
                password += choice(simboli)
        passwords.append(password)
        self.lp.scriviPassword(passwords)
        system("clear")
        return passwords

    def elimina(self, passwords):
        plat = input("Quale piattaforma? ")
        cerca = plat.lower()
        if cerca in passwords:
            indice = passwords.index(cerca)
            passwords.pop(indice)
            passwords.pop(indice)
            passwords.pop(indice)
            system("clear")
            print(f"» I dati di {plat} sono stati eliminati!")
            self.lp.scriviPassword(passwords)
            return passwords
        else:
            system("clear")
            print(f"» {plat} non risulta nel database!")
            return passwords

    def listaPasswords(self):
        return self.lp.leggiPassword()