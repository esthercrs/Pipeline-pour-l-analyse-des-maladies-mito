# Auteurs : Cros Esther, Guiberteau Yaelle, Le corre Mallory, Serain Corentin et Vanney Noah

#!/usr/bin/env python3
export PATH="/net/cremi/mallecorre/pp/gatk-4.4.0.0/:$PATH"

fastaReference = /data/REF.fasta
sortedbam = /output/sorted.bam
output = /output/Variantcall.vcf

gatk Mutect2 \
-R fastaReference \
-L chrM 1 \
--mitochondria-mode \
-I sortedbam\
-O output \
