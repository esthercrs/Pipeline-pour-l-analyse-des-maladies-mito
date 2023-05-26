# Auteurs : CROS Esther, GUIBERTEAU Yaelle, LE CORRE Mallory, SERAIN Corentin et VANNEY Noah

import pandas as pd
import subprocess
import os

OUTPUT_FILE = '/output'
VEP_FILE = '/ensembl-vep/vep'
POINT_VEP = '/root/.vep'
REF_FASTA = '/data/REF.fasta'
VARIANT_CALL_FILE = '/output/TSVC_variants_IonXpress_011.vcf'
DISEASE_FILE = '/data/disease.vcf'
ANNO_FILE = '/output/annotation_VEP_Mitomap.csv'

#Annotation par VEP
def annotate_vcf(vcf_file):
    output_filename = 'output_vep.csv'
    output_path = os.path.join(OUTPUT_FILE,output_filename)
    print(f"Le fichier output sera cree a l'emplacement : {output_path}")
    vep_command = f'{VEP_FILE} -i {vcf_file} --cache --dir_cache {POINT_VEP} --offline --fasta {REF_FASTA} --assembly GRCh38 --format vcf --vcf --pick --force_overwrite --no_escape --everything --output_file {output_path}' 
    subprocess.call(vep_command, shell=True)
    if os.path.exists(output_path):
        print("Le fichier output a ete cree avec succes!")
    else:
        print("Erreur : le fichier output n'a pas ete cree.")
    return output_path

# Chargement des fichiers VCF et CSV
def load_vcf(file_variant):
    headers = []  # Variable pour stocker les en-tetes
    data = []  # Variable pour stocker les donnees du fichier
    with open(file_variant, 'r') as f:
        for line in f:
            if not line.startswith('#'):  # Sortir de la boucle lorsqu'on atteint la ligne non commentee
                data.append(line.strip().split('\t'))  # Ajouter les donnees a la liste
            if line.startswith('#CHROM'):  # Identifier la ligne des en-tetes
                headers = line.strip().split('\t')  # Extraire les en-tetes (a partir de la colonne 2)
    df = pd.DataFrame(data, columns=headers)
    return df

# Separation des elements contenu dans la colonne INFO
def parse_info_column(df):
    parsed_info = []  # Liste de dictionnaires pour stocker les informations analysees
    for index, row in df.iterrows():
        info = row['INFO']
        pairs = info.split(';')
        parsed_info_row = {}  # Dictionnaire pour stocker les informations de la ligne actuelle
        for pair in pairs:
            if '=' in pair:
                split_pair = pair.split('=')
                if len(split_pair) == 2:
                    key, value = split_pair
                    parsed_info_row[key] = value
        parsed_info.append(parsed_info_row)
    parsed_info_df = pd.DataFrame(parsed_info)
    merged_df = pd.concat([df.drop('INFO', axis=1), parsed_info_df], axis=1)
    return merged_df

def load_and_parse_vcf(file_path):
    vcf_data = load_vcf(file_path)
    vcf_data.rename(columns={'#CHROM': 'CHROM'}, inplace=True)
    # Permet d'homogeneise les dataframes, dans toutes les situations le chromosome sera nomme "M"
    vcf_data['CHROM'] = 'M'
    return parse_info_column(vcf_data)

# Separation des elements contenu dans la colonne CSQ
def separate_csq_column(df, column_name):
    # Creer de nouvelles colonnes CSQ
    csq_columns = [f'CSQ{i+1}' for i in range(df[column_name].str.count('\|').max() + 1)]
    df[csq_columns] = df[column_name].str.split('\|', expand=True)
    df = df.drop(column_name, axis=1)  # Supprimer la colonne CSQ d'origine
    # Renommer les nouvelles colonnes avec les noms specifiques
    # Il y a plus de colonnes que de noms de colonnes connus, les dernieres colonnes ne sont donc pas renommees, trouver l'information et adapter
    new_column_names = ['Allele', 'Consequence', 'IMPACT', 'SYMBOL', 'Gene', 'Feature_type',
                        'Feature', 'BIOTYPE', 'EXON', 'INTRON', 'HGVSc', 'HGVSp', 'cDNA_position',
                        'CDS_position', 'Protein_position', 'Amino_acids', 'Codons',
                        'Existing_variation', 'DISTANCE', 'STRAND', 'FLAGS', 'SYMBOL_SOURCE', 'HGNC_ID']
    df = df.rename(columns=dict(zip(csq_columns, new_column_names)))
    return df

# Appel a la fonction annotate_vcf, sortie : Variants annotes par VEP
output_path_vep = annotate_vcf(VARIANT_CALL_FILE)
csv_variant_VEP=load_and_parse_vcf(output_path_vep)

# Chargement et fusion des donnees Mitomap
vcf_variant_TSCV=load_and_parse_vcf(VARIANT_CALL_FILE)
vcf_variant_disease=load_and_parse_vcf(DISEASE_FILE)
merged_data_Mitomap = pd.merge(vcf_variant_TSCV, vcf_variant_disease, on=['CHROM', 'POS', 'REF', 'ALT'], how='inner')

# Sortie : Variants deja annotes dans la litterature
#output_file = '/home/escros/project_prog/demo-app/anno/annotation/output_mito.csv'
#merged_data_Mitomap.to_csv(output_file, index=False)

# Fusion des donnees Mitomap et VEP
merged_data_anno = merged_data_Mitomap.set_index(['CHROM', 'POS', 'REF', 'ALT']).combine_first(csv_variant_VEP.set_index(['CHROM', 'POS', 'REF', 'ALT'])).reset_index()

# Traitement de la colonne CSQ
merged_data_anno['CSQ'] = merged_data_anno['CSQ'].astype(str).fillna('')
merged_data_anno = separate_csq_column(merged_data_anno, 'CSQ')

# Ne pas supprimer colonnes vides, sinon cree des beugs pour l'integration du document à la base de donnee. Il faut que les colonnes soient stables.

# Reorganisation des colonnes dans l'ordre souhaite
ordering_columns = ['CHROM', 'POS', 'ID','REF', 'ALT','QUAL','TYPE','Disease','DiseaseStatus','FILTER','FORMAT']
desired_order =  ordering_columns + list(merged_data_anno.columns.drop(ordering_columns))
merged_data_anno=merged_data_anno.reindex(columns=desired_order)

# Sortie : Variants annotes par Mitomap et VEP
output_file = ANNO_FILE
merged_data_anno.to_csv(output_file, index=False)
