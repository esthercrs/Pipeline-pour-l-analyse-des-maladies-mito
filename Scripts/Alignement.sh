# Auteurs : Cros Esther, Guiberteau Yaelle, Le corre Mallory, Serain Corentin et Vanney Noah

#!/bin/bash

# Vérifie si le nombre d'arguments est correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 reference_file.fastq reads_file.fastq"
    exit 1
fi

# Récupère les noms des fichiers d'entrée
reference="$1"
reads="$2"

# Enlever le > de la ref
temp_file=$(mktemp)
grep -v "^>" "$reference" | head -c 300 > "$temp_file"
cat "$reference" "$temp_file" > "${reference}_nouveau"
rm "$temp_file"

# Création du fichier fasta
echo "${reference}" > "nouveau.fasta"
cat "${reference}_nouveau" >> "nouveau.fasta"
tr -d '\n' < "nouveau.fasta" > "begin.fasta"
sed 's/\(.\{9\}\)/\1\n/' "begin.fasta" > "begin2.fasta"
sed 's/\(.\{56\}\)/\1\n/' "begin2.fasta" > "end.fasta"



# Crée l'index pour le génome de référence avec BWA
bwa index "end.fasta"

# Aligne les reads avec BWA-MEM et redirige la sortie vers un fichier SAM
bwa mem -t 4 "end.fasta" "$reads" > output.sam

# Convertit le fichier SAM en format BAM avec samtools
samtools view -Sb output.sam > output.bam

# Trie le fichier BAM
samtools sort output.bam -o sorted.bam

# Indexe le fichier BAM trié
samtools index sorted.bam
