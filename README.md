# GRAINERY 

Aplikace Granery umožňuje pracovat s technickými a administrativními metadaty z webových archivů. Staví na metadatový specifikaci Grainery 0.35 pro webarchivy vychádzejíc zo širších specifikací IIPC. Na tomto základě přispíva k precizaci monitoringu úložišťě webarchivu, jeho správě, bitové a logické ochraně a grafickému přiblížení jeho obsahu pomocí statistik pro nejširší veřejnost. 

Více: https://github.com/WebarchivCZ/grainery/wiki/Popis-aplikace 

# Krátce o aplikaci

## Skladba
 
Aplikace se skládá ze dvou hlavních částí: pythoní extraktor metadat Extarc a prezentační vrstva. Komunikujú společne cez NoSQL bázi cez formát JSON dále upresněn technickou metadatovou specifikací Grainery.

# Začíname

## Prerekvizity

* Git
* Python 3.5 a 3.7 
* Pip3 instalátor dependencies
* Mongo DB - např. cez docker
* Pre Extarc: shellovú konzolu, Gzip (>=1.6), pracujúce napojenie na storage 

## Instalace

```
#Naklonuj repo

git clone https://github.com/WebarchivCZ/grainery.git

#Nainstaluj dependencies pre Extarc a Web Applikáciu
cd grainery
pip3 install requirements.txt

```

## Rozběhnutí Extarcu

*Púštaj nad úložišťom len lokálne vnútry zabezpečenej, alebo izolovanej siete*

Extarc potřebuje i když je záťěž poňatá minimalisticky, systém s kvalitným a rychlým úložištěm, příjemným pásmovým rozsahem a priměřenou pamětí, ideálne 16 GB RAM, může však běžet i na daleko nižších konfiguracích, eg. 2 GB RAM.

```
#copy extarc to top directory of your archive
cp ./extarc /archive/mightyTopFolder  
cd /archive/mightyTopFolder
python3 Extarc.py > ExtarcYYYYMMDD-folder.log

# opakuj nad top adresármi obsahujúcimi warc, cdx, crawl logy, linuxfixity
# spojení disparátnich úložišť je otázkou revize
```

## Verzovaní

** Grainery 0.3 **

* Webová aplikace:
* Extarc: 0.3
* Metadatová specifikace: 0.35 

## Autoři

* **Zdenko Vozár** -  *back-end app, extraction and specification*
* **Jirka Kvasnica** - *front-end app, representation, theoretical base*

## Více

Více najdete v dokumentaci: https://github.com/WebarchivCZ/grainery/wiki
