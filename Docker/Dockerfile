#Auteurs : Cros Esther, Guiberteau Yaelle, Le corre Mallory, Serain Corentin et Vanney Noah

FROM ubuntu:22.04

######################################
##### INSTALLATION DES LOGICIELS #####
######################################

# Installation des dépendances
RUN apt-get update && apt-get install --no-install-recommends -y \
 libncurses5-dev \
 libbz2-dev \
 liblzma-dev \
 libcurl4-gnutls-dev \
 zlib1g-dev \
 libssl-dev \
 gcc \
 wget \
 make \
 perl \
 bzip2 \
 gnuplot \
 ca-certificates \
 gawk && \
 apt-get autoclean && rm -rf /var/lib/apt/lists/*



############ INSTALLATION DE JAVA ############

RUN apt-get update && apt-get install -y openjdk-11-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"


RUN java -version

############ INSTALLATIONS DE SAMTOOLS ############

ARG SAMTOOLSVER=1.13

RUN wget https://github.com/samtools/samtools/releases/download/${SAMTOOLSVER}/samtools-${SAMTOOLSVER}.tar.bz2 && \
 tar -xjf samtools-${SAMTOOLSVER}.tar.bz2 && \
 rm samtools-${SAMTOOLSVER}.tar.bz2 && \
 cd samtools-${SAMTOOLSVER} && \
 ./configure && \
 make && \
 make install && \
 cd .. && \
 rm -rf samtools-${SAMTOOLSVER} && \
 mkdir /data

RUN apt-get update && apt-get install -y git

############ INSTALLATION DE BWA ############

RUN apt-get update

RUN apt-get install -y bwa

############ INSTALLATION DE PICARD TOOLS ############
# Picard Tools
RUN wget https://github.com/broadinstitute/picard/releases/download/2.25.6/picard.jar

RUN mv picard.jar /usr/local/bin/picard.jar
ENV PICARD_HOME /usr/local/bin

RUN echo '#!/bin/bash' >> /usr/local/bin/picard
RUN echo 'java -jar /usr/local/bin/picard.jar "$@"' >> /usr/local/bin/picard
RUN chmod +x /usr/local/bin/picard

# ajout du chemin d'accès dans le PAT
ENV PATH $PATH:/usr/local/bin

############ INSTALLATION DE GATK ############
# Installation des dépendances
RUN apt-get update && apt-get install -y \
 openjdk-8-jdk \
 curl \
 unzip

# Téléchargement et installation de GATK
RUN curl -L -o gatk.zip "https://github.com/broadinstitute/gatk/releases/download/4.4.0.0/gatk-4.4.0.0.zip" && \
 unzip gatk.zip -d /gatk && \
 rm gatk.zip

# Définition de la variable d'environnement PATH
ENV PATH="/gatk/gatk-4.4.0.0:${PATH}"

############ INSTALLATION DE VEP ############
RUN apt-get update && apt-get install -y \
 build-essential \
 cpanminus \
 libdbi-perl \
 libset-intervaltree-perl \
 libwww-perl \
 libhttp-daemon-perl \
 git \
 libdbd-mysql-perl

RUN cpanm Module::Build \
 && cpanm DBI \
 && cpanm Set::IntervalTree \
 && cpanm LWP::Simple \
 && cpanm HTTP:aemon \
 && cpanm Test::Needs
 # && cpanm DBD-mysql

RUN git clone https://github.com/Ensembl/ensembl-vep.git

WORKDIR /ensembl-vep
RUN ./INSTALL.pl -a cfp -n -s "homo_sapiens_refseq" --ASSEMBLY GRCh38 --PLUGINS all



############ INSTALLATION HAPLOGREP ############
# Mise à jour du système et installation des dépendances nécessaires
RUN apt-get update && apt-get install -y \
 openjdk-11-jre-headless \
 unzip

RUN wget https://github.com/genepi/haplogrep3/releases/download/v3.2.1/haplogrep3-3.2.1-linux.zip

RUN unzip haplogrep3-3.2.1-linux.zip && \
 rm haplogrep3-3.2.1-linux.zip

CMD tail -f /dev/null

############################################################
####### CREATION DES RÉPERTOIRES ET CLONAGE DU GITHUB ######
############################################################

WORKDIR /
# Création du répertoire dans lequel seront présents les scripts du GitHub
RUN mkdir /github

# Création du répertoire "output" qui sera transféré vers le répertoire de l'ordinateur de l'utilisateur
RUN mkdir /output

#Creation du repertoire data dans lequel seront place les data de l'utilisateur 

COPY REF.fasta /data/REF.fasta

COPY fastq_file.fastq /data/fastq.fastq

WORKDIR /github

# Clone du référentiel GitHub, copie de son contenu dans le repertoire "github"
RUN git clone https://github.com/yguiberteau/Pipeline-pour-l-analyse-des-maladies-mito /tmp/repo && \
 cd /tmp/repo && \
 # Un pull est effesctue afin d'avoir toujours la derniere version du GitHub
 git pull && \ 
 cp -r /tmp/repo/* /github && \
 rm -rf /tmp/repo

RUN mkdir -p /.github/workflows


################################
####### Appel des scripts ######
################################

WORKDIR /github/script

###### Allignement ######

RUN sh Allignement.sh


############ INSTALLATION DE PYTHON2 ############
# gatk utilise python2, il faut donc passer python en python 2 le temps du script
RUN apt-get update

# Installation de Python 2
RUN apt-get install -y python2

# Configuration de Python 2 comme la version par défaut
RUN ln -s /usr/bin/python2 /usr/bin/python


###### Variant Call #####

RUN sh VariantCall.sh


############ Remise à niveau en python3 ############
# le docker repassé en python 3 pour la suite

##### Annotations #####

RUN python3 Annotation.py

###### Haplogrep ######

RUN sh Haplogrep.sh

############ PYTHON 2 ############
# gatk utilise python2, il faut donc passer python en python 2 le temps du script
RUN apt-get update

# Installation de Python 2
RUN apt-get install -y python2

# Configuration de Python 2 comme la version par défaut
RUN ln -s /usr/bin/python2 /usr/bin/python

####### eKLIPse #######

RUN sh eKLIPse.sh

# Commande de fin du Dockerfile
CMD ["echo", "finished"]
