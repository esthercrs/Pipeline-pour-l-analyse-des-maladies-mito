import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# Lire le fichier haplogroup.txt dans un DataFrame Pandas
df_haplogroup = pd.read_csv('haplogrouptest.txt', sep='\t', header=None)
df_haplogroup.columns = ['SampleID', 'Haplogroup', 'Rank', 'Quality', 'Range']
df_haplogroup = df_haplogroup.iloc[1:]  # Supprimer la première ligne

# Lire le fichier haplogroup.qc.txt dans un DataFrame Pandas
df_haplogroupqc = pd.read_csv('haplogrouptest.qc.txt', sep='\t', header=None)
df_haplogroupqc = df_haplogroupqc.drop(columns=[1])  # Exclure la colonne "Haplogroup"
df_haplogroupqc.columns = ['SampleID', 'Type', 'Message', 'Missing Mutations', 'Global Private Mutations']

# Fusionner les DataFrames sur la colonne "SampleID"
df_merged = pd.merge(df_haplogroup, df_haplogroupqc, on='SampleID', how='left', suffixes=('_haplogroup', '_haplogroupqc'))

# Exporter les données fusionnées dans un fichier Excel
excel_writer = pd.ExcelWriter('haplogroup_merged.xlsx', engine='openpyxl')
df_merged.to_excel(excel_writer, index=False, sheet_name='Sheet1')

# Appliquer le style à la colonne "Global Private Mutations"
workbook = excel_writer.book
worksheet = workbook['Sheet1']
red_font = Font(color='FF0000')
worksheet.column_dimensions['J'].width = 20  # Ajuster la largeur de la colonne si nécessaire
for cell in worksheet['J']:
    cell.font = red_font

# Enregistrer le fichier Excel
workbook.save('haplogroup_merged.xlsx')
excel_writer.close()
