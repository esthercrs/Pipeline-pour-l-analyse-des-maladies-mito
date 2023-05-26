import pandas as pd #Import des librairies nécessaires
import mariadb
import sys


def creation():
    USERNAME = "yguiberteau"
    PASSWORD = "Ya&2l&Mito"

    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()

    nom_bdd = "Variants_Mitochondriaux"
    try:
        print("Création de la base de données Variants mitochondriaux")
        cur.execute("CREATE DATABASE {}".format(nom_bdd))
        print("La base de données '{}' a été créée avec succès.".format(nom_bdd))
    except Exception as e:
        exit("Impossible de créer la base de données Variants mitochondriaux"+str(e))


    #cur.execute("DROP TABLE Variants CASCADE")
    #conn.commit()

    try:
        print("Création de la table Variants") 
        cur.execute("""CREATE TABLE public.Variants(Pos int not null,
                                                Ref text not null,
                                                Alt text not null,
                                                Variant text not null,
                                                primary key (Pos,Ref,Alt)
                                                );""")
        print("Table Variants créée avec succès")
    except Exception as e:
        exit("Impossible de créer la table Variants"+str(e))
        
    #cur.execute("DROP TABLE Annotations")
    #conn.commit()

    try:
        print("Création de la table Annotations") #Voir intitulés des colonnes avec Esther et types des variables
        cur.execute("""CREATE TABLE public.Annotations(Chrom text not null,
                                                Pos int not null,
                                                Id text not null,
                                                Ref text not null,
                                                Alt text not null,
                                                Qual float not null,
                                                Type text not null,
                                                Disease text not null,
                                                DiseaseStatus text not null,
                                                Filter text not null,
                                                PubmedIDs text not null,
                                                AAchange text not null,
                                                Heteroplasmy text not null,
                                                Homoplasmy text not null,
                                                Allele text not null,
                                                Consequence text not null,
                                                Impact text not null,
                                                Symbol text not null,
                                                Gene text not null,
                                                primary key (Pos,Ref,Alt),
                                                foreign key (Pos) references Variants(Pos),
                                                foreign key (Ref) references Variants(Ref),
                                                foreign key (Alt) references Variants(Alt)
                                                );""")
        print("Table Annotations créée avec succès")
    except Exception as e:
        exit("Impossible de créer la table Annotations"+str(e))
        
    #cur.execute("DROP TABLE Annotations")
    #conn.commit()

    try:
        print("Création de la table Echantillons")
        cur.execute("""CREATE TABLE public.Echantillons(Id int not null,
                                                NumEchantillon int not null,
                                                Variant text not null,
                                                primary key (Id),
                                                foreign key (Variant) references Variants(Variant)
                                                );""")
        print("Table Echantillons créée avec succès")
    except Exception as e:
        exit("Impossible de créer la table Nomenclature"+str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()

    print("La connexion MariaDB est fermée.")
