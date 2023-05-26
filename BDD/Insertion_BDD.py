import pandas as pd #Import des librairies nécessaires
import mariadb
import sys


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&Mito"


def liste_var():
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = """SELECT Variant from Variants;"""
        cur.execute(command)
        rows = cur.fetchall()
        Variants = []
        if (not rows):
            cur.close()
            conn.close()
            exit("Il n'y a pas de variant renseigné dans la table Variants de la base de données.")
        for r in rows:
            Variants.append(r[0])
        cur.close()
        conn.close()
        return Variants        
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def longueur_ech():
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = """SELECT count(*) from Echantillons;"""
        cur.execute(command)
        rows = cur.fetchall()
        if (not rows):
            cur.close()
            conn.close()
            exit("Il n'y a pas d'échantillon renseigné dans la table Echantillons de la base de données.")
        for r in rows:
            longueur = r[0]
        cur.close()
        conn.close()
        return longueur    
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def remise_en_forme_variants(df):

    liste_variants = liste_var()

    Positions = []
    Refs = []
    Alts = []
    Variants = []

    for i in range (0,df.shape[1],2):
        for j in range (0,df.shape[0]):
            var = df.iloc[j,i] 
            if var != "NaN" and var not in Variants:
                Variants.append(var)

    Variants_uniq = [var for var in Variants if var not in liste_variants]

    for var in Variants_uniq:
        pos = ""
        ref = ""
        alt = ""
        if var[0] == "-":
            ref = "-"
            for char in var[1:]:
                if char.isdigit():
                    pos += char
                else:
                    alt += char
        elif var[-1] == "-":
            alt = "-"
            for char in var[:-1]:
                if char.isdigit():
                    pos += char
                else:
                    ref += char
        else:
            for i in range(len(var)):
                if var[i].isdigit():
                    pos += var[i]
                    i_pos = i
            ref = var[:i_pos+1-len(pos)]
            alt = var[i_pos+1:]
        Positions.append(pos)
        Refs.append(ref)
        Alts.append(alt)
            
    df_variants = pd.DataFrame({"Pos":Positions,
                    "Ref":Refs,
                    "Alt":Alts,
                    "Variant":Variants_uniq})

    return df_variants


def insert_Excel_variants(path_excel):
    df_chargement = pd.read_excel(path_excel) #Insertion des données issues des fichiers .xlsx dans des dataframes pandas
    df_chargement.fillna(value="NaN",inplace=True) #Remplacement des cases vides de la dataframe par la valeur 'NaN'
    df_variants = remise_en_forme_variants(df_chargement)

    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()

    print("Insertion des données dans la table Variants") 
    try:
        for i in range (1,df_variants.shape[0]):
            value=list(df_variants.iloc[i])
            command="INSERT INTO Variants VALUES ({},'{}','{}','{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            print(command)
            cur.execute(command)
        print("Importation des données dans la table Variants réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion MariaDB est fermée.\n")


def remise_en_forme_echantillons(df):

    deb_ids = longueur_ech()

    Identifiants = []
    Echantillons = []
    Variants = []

    for i in range (0,df.shape[1],2):
        for j in range (0,df.shape[0]):
            ech = df.columns[i]
            var = df.loc[j,ech] 
            if var != "NaN":
                Variants.append(var)
                Echantillons.append(int(ech[8:]))
                deb_ids += 1
                Identifiants.append(deb_ids)
            
    df_echantillons = pd.DataFrame({"Identifiant":Identifiants,
                    "NumEchantillon":Echantillons,
                    "Variant":Variants})

    return df_echantillons


def insert_Excel_echantillons(path_excel):
    df_chargement = pd.read_excel(path_excel) #Insertion des données issues des fichiers .xlsx dans des dataframes pandas
    df_chargement.fillna(value="NaN",inplace=True) #Remplacement des cases vides de la dataframe par la valeur 'NaN'
    df_echantillons = remise_en_forme_echantillons(df_chargement)

    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()

    print("Insertion des données dans la table Variants") 
    try:
        for i in range (1,df_echantillons.shape[0]):
            value=list(df_echantillons.iloc[i])
            command="INSERT INTO Echantillons VALUES ({},{},'{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            print(command)
            cur.execute(command)
        print("Importation des données dans la table Variants réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion MariaDB est fermée.\n")


def insert_manuel_variants(var):

    liste_variants = liste_var()

    if var not in liste_variants:
        pos = ""
        ref = ""
        alt = ""
        if var[0] == "-":
            ref = "-"
            for char in var[1:]:
                if char.isdigit():
                    pos += char
                else:
                    alt += char
        elif var[-1] == "-":
            alt = "-"
            for char in var[:-1]:
                if char.isdigit():
                    pos += char
                else:
                    ref += char
        else:
            for i in range(len(var)):
                if var[i].isdigit():
                    pos += var[i]
                    i_pos = i
            ref = var[:i_pos+1-len(pos)]
            alt = var[i_pos+1:]
        
        try:
            print("Connexion à la base de données...") #Connexion à la base de données
            conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        except mariadb.Error as e :
            exit("Connexion impossible à la base de données: " + str(e))
        print("Connecté à la base de données")

        cur = conn.cursor()

        print("Insertion des données dans la table Variants") 
        try:
            value=[pos,ref,alt,var]
            command="INSERT INTO Variants VALUES ({},'{}','{}','{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            print(command)
            cur.execute(command)
            print("Importation des données dans la table Variants réussie.")
        except Exception as e:
            cur.close()
            conn.close()
            exit("Error when running: ",command," : ",str(e))

        conn.commit() #Fermeture de la connexion à la base de données
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée.\n")

    else:
        print("Ce variant est déjà présent dans la table Variants")


def insert_manuel_echantillons(ech,var):
    
    id = longueur_ech()

    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()

    print("Insertion des données dans la table Variants") 
    try:
        value=[id,ech,var]
        command="INSERT INTO Echantillons VALUES ({},{},'{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
        print(command)
        cur.execute(command)
        print("Importation des données dans la table Variants réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée.\n")


def insert_csv_annotations(path_csv):
    df_annotations = pd.read_csv(path_csv,sep=",") #sep à voir avec le fichier de sortie d'Esther

    try:
        print("Connexion à la base de données...") #Connexion à la base de données
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
    except mariadb.Error as e :
        exit("Connexion impossible à la base de données: " + str(e))
    print("Connecté à la base de données")

    cur = conn.cursor()

    print("Insertion des données dans la table Annotation")
    try:
        for i in range (df_annotations.shape[0]):
            value=list(df_annotations.iloc[i])
            command="INSERT INTO Annotation VALUES ('{}',{},'{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(*value) #Formatage des chaînes grâce aux accolades et à la fonction format
            cur.execute(command)
        print("Importation des données dans la table Annotation réussie.")
    except Exception as e:
        cur.close()
        conn.close()
        exit("Error when running: ",command," : ",str(e))   

    conn.commit() #Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion MariaDB est fermée.\n")


def insertion():
    rep1 = 1
    while rep1 != 0:
        print("Dans quelle table souhaitez-vous insérer des données ?")
        print("1 - Table Variants")
        print("2 - Table Echantillons")
        print("3 - Table Annotation")
        print("0 - Quitter le programme")
        rep1 = int(input())
        if rep1 == 1:
            rep2 = 1
            while rep2 != 0:
                print("Comment souhaitez-vous insérer des données dans la table Variants ?")
                print("1 - À partir d'un fichier Excel")
                print("2 - Manuellement")
                rep2 = int(input())
                if rep2 == 1:
                    path_excel = input("Quel est le path de votre fichier Excel ?\n")
                    insert_Excel_variants(path_excel)
                    break
                elif rep2 == 2:
                    var = input("Veuillez entrer votre variant : ")
                    insert_manuel_variants(var)
                    break
                else:
                    print("Choix incorrect. Veuillez recommencer")
        elif rep1 == 2:
            rep3 = 1
            while rep3 != 0:
                print("Comment souhaitez-vous insérer des données dans la table Variants ?")
                print("1 - À partir d'un fichier Excel")
                print("2 - Manuellement")
                rep3 = int(input())
                if rep3 == 1:
                    path_excel = input("Quel est le path de votre fichier Excel ?\n")
                    insert_Excel_echantillons(path_excel)
                    break
                elif rep3 == 2:
                    ech = int(input("Veuillez entrer votre numéro d'échantillon : "))
                    var = input("Veuillez entrer votre variant : ")
                    insert_manuel_echantillons(ech,var)
                    break
                else:
                    print("Choix incorrect. Veuillez recommencer")
        elif rep1 == 3:
            path_csv = input("Quel est le path de votre fichier d'annotation .csv ?\n")
            insert_csv_annotations(path_csv)
        elif rep1 == 0:
            print("Au revoir !")
            sys.exit()
        else:
            print("Choix incorrect. Veuillez recommencer")
