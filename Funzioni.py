from os import system
from sys import exit

def menu():
    print("""\n*************************
    1. Lista Piattaforme
    2. Leggi User e Password
    3. Modifica 
    4. Aggiungi 
    5. Elimina 
    6. Generare una Password
    7. Carica da file in chiaro
    8. Salva e Esci""")

def pulisci_schermo():
    system("clear")

def esci_con_messaggio(messaggio):
    exit(messaggio)

def regola(lista, int_lista_size, lista_size):
    int_lista_opera = int_lista_size
    lista_temporanea = []
    test_size_lista = lista_size - int_lista_size

    if test_size_lista < 0:
        if test_size_lista > -1:
            for i in range(int_lista_opera - 1):
                lista_temporanea.append(lista[i])
        elif test_size_lista > -2:
            for i in range(int_lista_opera - 2):
                lista_temporanea.append(lista[i])
        elif test_size_lista > -3:
            for i in range(int_lista_opera - 3):
                lista_temporanea.append(lista[i])
    elif test_size_lista == 0:
        return lista
    elif test_size_lista > 0:
        for i in range(int_lista_opera):
            lista_temporanea.append(lista[i])

    return lista_temporanea

def elementi_lista_non_unici(lista):
    pt = []

    for i in lista:
        if lista.count(i) > 1 and i not in pt:
            pt.append(i)

    return pt

def intToPlat(keys, index):
    counter = index
    counter_loop = 1
    platform = ''

    for i in keys:
        if counter != counter_loop:
            counter_loop += 1
        else:
            platform = i
            break

    return platform