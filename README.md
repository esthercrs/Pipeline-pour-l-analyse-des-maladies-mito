# Pipeline-pour-l-analyse-des-maladies-mito

Ce pipeline a pour objectif de fournir le maximum d'informations à partir d'une séquence d'ADN mitochondrial d'un patient dans le but de permettre au biologiste de réaliser le meilleur diagnostic possible.

#Prérequis
Afin de pouvoir exécuter le pipeline sur votre poste, vous devez d'abord installer les logiciels suivants :

* python 2.7
* Java
* BWA
* samtools
* picard tools
* gatk
* VEP
* haplogrep
* eKlipse


#Installation on Ubuntu
Note : Avant les installations par apt-get install, pensez à réaliser un apt-get update pour mettre à jour le système.

### PYTHON 2.7
$ sudo apt install python2

### JAVA

$ sudo apt-get install -y default-jre default-jdk

##BWA

$ sudo apt-get -y install bwa

### SAMTOOLS

$ sudo apt-get install -y libncurses-dev libbz2-dev liblzma-dev #telecharger les librairies necessaires à linstallation de samtools

$ cd Downloads/ #Mettez vous dans le repertoir ou vous souhaitez télécharger samtools

$ wget https://github.com/samtools/samtools/releases/download/1.12/samtools-1.12.tar.bz2 #telecharger le logiciel

$ tar xvjf samtools-1.12.tar.bz2 #extraire l'archive telechargé

$ cd samtools-1.12/ #placez vous dans le repertoire du logiciel extrait.

$ ./configure

$ make

$ sudo make install

$ export PATH="$PATH:/home/user/Downloads/samtools-1.12" #EXPORTER DANS LE PATH

$ sudo gedit ~/.bashrc #ouvrir le fichier bashrc

$ export PATH="$PATH:/home/user/Downloads/samtools-1.12" #ajouter cette ligne de commande à la fin du fichier

$ source ~/.bashrc #sauvevarder puis quitter

samtools est desormais installé et peut etre executé en tapant la commande $ samtools dans le terminal.

### PICARD TOOLS 

sudo apt-get install picard-tools

### GATK 

wget https://github.com/broadinstitute/gatk/releases/download/4.2.3.0/gatk-4.2.3.0.zip
    
unzip gatk-4.2.3.0.zip
    
cd  gatk-4.2.3.0
    
java -jar gatk-package-4.2.3.0-local.jar

### VEP 

suivre les étapes indiquées sur le site officiel de VEP : https://www.ensembl.org/info/docs/tools/vep/script/vep_download.html

### Haplogrep

sudo apt install openjdk-11-jre-headless #install java

wget https://github.com/genepi/haplogrep3/releases/download/v3.2.1/haplogrep3-3.2.1-linux.zip

sudo apt install unzip #installe la fonction unzip

unzip haplogrep3-3.2.1-linux.zip #unzip le zip

./haplogrep3 #execute haplogrep3 et affiche toutes les commandes

### eKlipse

Toutes les indications d'installation sont disponibles sur le GitHub officiel du logiciel : https://github.com/dooguypapua/eKLIPs. Suivez les étapes rigoureusement.


#### EXECUTION DU PIPELINE
