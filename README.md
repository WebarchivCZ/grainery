# GRAINERY 

Aplikace Granery umožňuje pracovat s technickými a administrativními metadaty z webových archivů. Staví na metadatové specifikaci Grainery 0.35 pro webové archivy vychádzející z širších specifikací IIPC. Na tomto základě přispívá k precizaci monitoringu úložišťě webarchivu, jeho správě, bitové a logické ochraně a grafickému přiblížení jeho obsahu pomocí statistik pro správce a kurátory, ale také pro nejširší veřejnost. 

Více: https://github.com/WebarchivCZ/grainery/wiki/Popis-aplikace 

# Krátce o aplikaci

## Skladba
 
Aplikace se skládá ze dvou hlavních částí: python extraktor metadat Extarc a prezentační vrstva (Grainery frontend). Komunikují společně přes NoSQL bázi (MongoDB) přes formát JSON, která je definován technickou metadatovou specifikací Grainery.

# Začíname

Podrobněji:

https://github.com/WebarchivCZ/grainery/wiki/Instalace

## Prerekvizity

* Git
* Python 3.5 a 3.7 
* Pip3 instalátor dependencies
* Mongo DB - např. přes docker
* Pro Extarc: shell console, Gzip (>=1.6), funkční připojení na storage 

## Instalace

```
#Naklonuj repo

git clone https://github.com/WebarchivCZ/grainery.git

#Nainstaluj dependencies pre Extarc a Web Applikáciu
cd grainery
pip3 install -r requirements.txt

```

## Rozběhnutí Extarcu

*Pouštěj lokálne, nad úložištěm jen vnitru zabezpečený, anebo izolovaný sítě*

Extarc potřebuje i když je záťěž poňatá minimalisticky, serverový systém s dostupným a rychlým úložištěm, příjemným pásmovým rozsahem a priměřenou pamětí, ideálne 8-16 GB RAM a osmijádrovým procesorem . Pro domáci testovaní, alebo ako dlouhodobá servica na pozadí může běžet i na daleko nižších konfiguracích, eg. 2 GB RAM.

```
#copy extarc to top directory of your archive
cp ./extarc /archive/mightyTopFolder  
cd /archive/mightyTopFolder
python3 Extarc.py > ExtarcYYYYMMDD-folder.log

# opakuj nad top adresármi obsahujúcimi warc, cdx, crawl logy, linuxfixity
# spojení disparátnich úložišť je otázkou revize
# ideálně pouštět ako proces na pozadí
```

## Rozběhnutí Grainery frontendu
Grainery frontend je postavený na frameworku Flask a je testovaný na Pythonu 3.7.0
V MongoDB potřebuje databázi _grainery_ a v ní tři kolekce: _harvest_, _container_, _cdx_
Dalším krokem je vytvoření indexu pro full textové vyhledávání v kolekci harvest. Vytvoření indexu v Mongo shellu

```
set db grainery

db.harvest.createIndex( { "harvest.name": "text", "harvest.harvestID": "text" } )
```
Připojení aplikace k MongoDB se nastavuje v config souboru frontend/config/config.py (při první instalaci přepište config_default.py na config.py)

Přesunout config_default.py do config.py a nastavit v něm připojení k mongoDB

Grainery má defaultně nastavenou produkční konfiguraci, v případě potřeby je to možné změnit v souboru app.py, kde se přepíše řádek `Configuration = cfg.ProductionConfig na Configuration = cfg.DevelopmentConfig`

## Verzovaní

**Grainery 0.3**

* Webová aplikace: 0.3
* Extarc: 0.3
* Metadatová specifikace: 0.35 

## Vývoj

* **Zdenko Vozár** -  *back-end app, extraction and specification*
* **Jaroslav Kvasnica** - *front-end app, representation, theoretical base*

## Více

Více najdete v dokumentaci: https://github.com/WebarchivCZ/grainery/wiki


_Realizováno v rámci institucionálního výzkumu Národní knihovny České republiky financovaného Ministerstvem kultury ČR v rámci Dlouhodobého koncepčního rozvoje výzkumné organizace._
