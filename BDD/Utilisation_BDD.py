# Auteurs : Cros Esther, Guiberteau Yaelle, Le corre Mallory, Serain Corentin et Vanney Noah

import pandas as pd #Import des librairies nécessaires
import mariadb
import sys
from Creation_BDD import *
from Insertion_BDD import *
from Requetes_BDD import *


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&Mito"


def exist_BDD():
    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()
    cur.execute("SHOW DATABASES LIKE 'Variants_Mitochondriaux'")
    result = cur.fetchone()

    if not result:
        creation()

    cur.close()
    conn.close()


def menu():
    exist_BDD()
    print("Bienvenue sur la base de données de variants mitochondriaux.")
    choix = 1
    while choix == 1 or choix == 2:
        print("""Que souhaitez-vous faire ?
        1 - Insérer des données dans la base de données
        2 - Soumettre une requête sur les données
        0 - Quitter""")
        choix = int(input())
        if choix == 1:
            insertion()
            print("on va insérer")
        elif choix == 2:
            requetes()
            print("requeeeeeeetes")
        elif choix == 0: #Quitter le programme
            print("Au revoir !")
            sys.exit()
        else:
            print("Choix incorrect. Veuillez recommencer.")

menu()

