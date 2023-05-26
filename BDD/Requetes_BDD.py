import pandas as pd #Import des librairies nécessaires
#import mariadb
import sys


USERNAME = "yguiberteau"
PASSWORD = "Ya&2l&Mito"


def liste_mal():
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = """SELECT Disease from Annotation;"""
        cur.execute(command)
        rows = cur.fetchall()
        maladies = []
        if (not rows):
            cur.close()
            conn.close()
            exit("Il n'y a pas de maladie renseignée dans la table Annotation de la base de données.")
        print("Voici la liste des maladies :") 
        for r in rows:
            print(r[0])
            maladies.append(r[0])
        cur.close()
        conn.close()
        print("Veuillez choisir une maladie : ")
        mal = input() 
        while mal not in maladies: #Gestion d'erreur sur le numéro de région passé en entrée
            print("Cette maladie n'est pas disponible.")
            print("Veuillez choisir une maladie parmi :",*maladies,"\n")
            mal = input()
        return mal        
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def liste_gen():
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = """SELECT Symbol from Annotation;"""
        cur.execute(command)
        rows = cur.fetchall()
        genes = []
        if (not rows):
            cur.close()
            conn.close()
            exit("Il n'y a pas de gène renseigné dans la table Annotation de la base de données.")
        print("Voici la liste des gènes :") 
        for r in rows:
            print(r[0])
            genes.append(r[0])
        cur.close()
        conn.close()
        print("Veuillez choisir un gène: ")
        gen = input() 
        while gen not in genes: #Gestion d'erreur sur le numéro de région passé en entrée
            print("Ce gène n'est pas disponible.")
            print("Veuillez choisir un gène parmi :",*genes,"\n")
            gen = input()
        return gen        
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def ech_pos_mut(pos):
    print('Trying to connect to the database')
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = '''SELECT Variants.Pos,Echantillons.NumEchantillon 
        FROM Echantillons JOIN Variants ON Echantillons.Variant = Variants.Variant 
        WHERE Echantillons.Variant IN (SELECT Variant FROM Variants WHERE Pos = {});'''.format(*pos) #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows = cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les numéros d'échantillons correspondant à la requête :")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print("Position :",r[0],"\tNuméro d'échantillon :",r[1])
        df=pd.DataFrame(columns=['Position','Numéro d\'échantillon']) #Création d'une dataframe contenant les résultats de la requête
        i = 0
        for r in rows:
            df.loc[i]=[r[0],r[1]]
            i += 1
        writer = pd.ExcelWriter('Num_Echantillons.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Num_Ech') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Num_Echantillons.xlsx à l'onglet Num_Ech\n")
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def var_ech(ech):
    print('Trying to connect to the database')
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = '''SELECT NumEchantillon,Variant 
        FROM Echantillons WHERE NumEchantillon = {});'''.format(*ech) #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows = cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les variants correspondant à la requête :")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print("Numéro d'échantillon :",r[0],"\tVariant :",r[1])
        df=pd.DataFrame(columns=['Numéro d\'échantillon','Variant']) #Création d'une dataframe contenant les résultats de la requête
        i = 0
        for r in rows:
            df.loc[i]=[r[0],r[1]]
            i += 1
        writer = pd.ExcelWriter('Variants_Echant.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Var_Ech') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Variants_Echant.xlsx à l'onglet Var_Ech\n")
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def var_maladie(mal):
    print('Trying to connect to the database')
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = '''SELECT Annotation.Disease,Variants.Variant 
        FROM Variants JOIN Annotation
        ON Variants.Pos = Annotation.Pos
        AND Variants.Ref = Annotation.Ref
        AND Variants.Alt = Annotation.Alt
        WHERE Annotation.Disease LIKE %{}%);'''.format(*mal) #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows = cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les variants correspondant à la requête :")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print("Maladie :",r[0],"\tVariant :",r[1])
        df=pd.DataFrame(columns=['Maladie','Variant']) #Création d'une dataframe contenant les résultats de la requête
        i = 0
        for r in rows:
            df.loc[i]=[r[0],r[1]]
            i += 1
        writer = pd.ExcelWriter('Var_Maladies.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Var_Mal') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Var_Maladies.xlsx à l'onglet Var_Mal\n")
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def var_gene(gen):
    print('Trying to connect to the database')
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = '''SELECT Symbol.Annotation,Variants.Variant, 
        FROM Variants JOIN Annotation
        ON Variants.Pos = Annotation.Pos
        AND Variants.Ref = Annotation.Ref
        AND Variants.Alt = Annotation.Alt
        WHERE Symbol.Annotation LIKE %{}%);'''.format(*gen) #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows = cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici les variants correspondant à la requête :")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print("Gène :",r[0],"\tVariant :",r[1])
        df=pd.DataFrame(columns=['Gène','Variant']) #Création d'une dataframe contenant les résultats de la requête
        i = 0
        for r in rows:
            df.loc[i]=[r[0],r[1]]
            i += 1
        writer = pd.ExcelWriter('Var_Genes.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Var_Gen') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Var_Genes.xlsx à l'onglet Var_Gen\n")
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def occ_variant(var):
    print('Trying to connect to the database')
    try:
        conn = mariadb.connect(user=USERNAME,password=PASSWORD,host="192.0.2.1",port=3306,database=USERNAME)
        print('Connected to the database')
        cur = conn.cursor()
    except Exception as e:
        exit("Can not connect to database: "+str(e))
    try:
        command = '''SELECT count(*) FROM Echantillons WHERE Variant = {};'''.format(*var) #Requête SQL
        print("Trying to execute command: ",command)
        cur.execute(command)
        print("Execute OK")
        rows = cur.fetchall()
        if (not rows):
            exit("Il n'y a pas d'éléments correspondant à cette requête.")
        print("Voici le nombre d'occurences du variant demandé :")
        for r in rows: #Affichage des résultats de la requête dans le terminal
            print(r[0])
        df=pd.DataFrame(columns=['Nombre d\'occurences']) #Création d'une dataframe contenant les résultats de la requête
        i = 0
        for r in rows:
            df.loc[i]=[r[0]]
            i += 1
        writer = pd.ExcelWriter('Occ_Variant.xlsx',engine="xlsxwriter") #Sauvegarde de la dataframe dans un fichier Excel
        df.to_excel(writer,sheet_name='Occ_Var') 
        writer.save()
        writer.close()
        print("Cette requête a été sauvegardée dans le fichier Occ_Variant.xlsx à l'onglet Occ_Var\n")
        cur.close()
        conn.close()
        print("La connexion MariaDB est fermée")
    except Exception as e:
        exit("Error when running command: "+command+" : "+str(e))


def requetes(): 
    '''Menu permettant d'accèder aux résultats des requêtes SQL'''
    rep = 1
    while rep != 0:
        #Affichage du menu
        print("Veuillez choisir ce que vous souhaitez connaître parmi les possibilités suivantes :")
        print("1 - Liste de tous les échantillons ayant une position donnée mutée.")
        print("2 - Liste de tous les variants d’un échantillon.")
        print("3 - Liste de tous les variants associés à une maladie.")
        print("4 - Liste de tous les variants liés à un gène.")
        print("5 - Nombre d’occurences d’un variant.")
        print("0 - Quitter le programme.")
        rep = int(input()) #Choix de l'utilisateur soumis en entrée
        if rep == 1:
            pos = int(input("Pour quelle position souhaitez-vous avoir la liste des échantillons ?\n"))
            ech_pos_mut(pos)
        elif rep==2:
            ech = int(input("Pour quel numéro d'échantillon souhaitez-vous avoir la liste des variants ?\n"))
            var_ech(ech)
        elif rep==3:
            print("Pour quelle maladie souhaitez-vous avoir la liste des variants ?\n")
            mal = liste_mal() 
            var_maladie(mal) 
        elif rep==4:
            print("Pour quel gène souhaitez-vous avoir la liste des variants ?\n")
            gen = liste_gen() 
            var_gene(gen)
        elif rep==5:
            var = input("De quel variant souhaitez-vous avoir le nombre d'occurences ?\n")
            occ_variant(var)
        elif rep==0: #Quitter le programme
            print("Au revoir !")
            sys.exit()
        else:
            print("Choix incorrect. Veuillez recommencer.") #Gestion d'erreur de l'entrée par l'utilisateur
            


        

