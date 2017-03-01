# grainery
Keeping knowledge about harvested ARC/WARCs and related files such as logs, CDX files etc.


Zavedena podvojna struktura pre skladovanie dat v Grainary DB, json for container a json for harvest samotny. Extrakcia pomocou propriety type a mappingu, idem parovanie. Issue, automaticke dovodenie (rsp aj. nacitanie) logu z harvestov na viacerych strojoch.

<b> 1.Vyhodene: </b>

?, "originalMimetype": "original_application_X-warc", <br>
sekvencia z harvestu:  "seq": 1, <br>
"dateOfOrigin": "exDateOfOrigin", <br>

<b> 2.Zamena </b><br>
Server ("server": "exServer",) = hostname crawlera vytvarajuceho warc <br>
HARVESTDATE - HARVESTDURATION <br>
ISPARTOF-HARVESTISPARTOF a HARVESTNAME - HARVESTISPARTOF , duplikacia odstranena je <b>harvestName</b> <br>

<b>3.Presun </b><br>
OPERATOR ("operator": "exOperator") a DESCRIPTION z warcu do harvestu <br>
CDX z harvestu do warcu, rozsierenie o md5, pociet linii a velkost <br>
STORAGE z containeru do PATH <br>
Pridane <b>harvest</b> a <b>container</b> ostatne zlozky mimo <b>deklarativne patriace k vzniku a strukture dokumentu</b> v DB nim podriadene 

<b> 4.Posun </b><br>

HARVESTISPARTOF v Harvest posunuto na #0CR <br>

<b> 5.Pridane</b><br>

Do HARVEST:  HOSTS - NUMBER + NAME /aby sme mohli operovat s potrojnou strukturou v harvestCrawl <br>
Do HARVEST: SIZE, tj. celková velikosť zberu (vrátane, alebo bez logov?) <br>
Do HARVEST: STATUS, stav integrity zberu vrátane dát
Do HARVEST: dateOfValidation A nextLastDateOfValidation
<ul> Stavy
<li>NonValidated</li>
<li>OK</li>
<li>Corrupted</li>
<li>Lost</li>
<li></li>
</ul>

<ul>Deklarativne zlozky
<li><b>author</b>: autor ci skript, ktory vklada dokument</li>
<li><b>date</b>: moment zapisu</li>
<li><b>standart</b>: štandard pre formátovanie JSONU - k príp. updatom</li>
<li><b>type</b>: typ dokumentu, tj. harvest alebo jeho container</li></ul>

<h2>B.1 Pridávanie nových a prepisovanie stávajúcich štruktúr</h2>

Pridávanie nových štruktúr do existujúcich dokumentov, je veľmi jednoduché pomocou práce s objektami v json a príkaze zo shellu pomocou curl. Pri prepisovaní sa prepíše stávajúce pole KOMPLETNE, nová štruktúra, napr. pri upgrade standardu sa vytvorí rovnakým spôsobom. Dôležité je ale poznať <b>_id</b> a <b>_rev</b> dokumentu, inak sa vytvori novy document s vlastným ID. 

<i>Príkaz:</i> root@localhost ~]# curl -X PUT http://zdenko:XXXXXX@127.0.0.1:10000/grainary/67f80e4db8ab23f8fb247e1a4d008597 -d '{"_rev":"2-eb8febb1d0d811391214eaf23b38f0b5", "container.storage.HNAS4":"24"}'

<i>CouchDB:</i> {"ok":true,"id":"67f80e4db8ab23f8fb247e1a4d008597","rev":"3-60a369de508fa82479d14179f9469e43"}

<h4>Rozšírená práca s update handlermy</h4>

Odkaz:

Invokácia zmienených funkcií:

PUT+ Handler function with a document id: /<database>/_design/<design>/_update/<function>/<docid>

Na špeciálne dotazovanie zas slúži PUT request: 

http://zdenko:XXXX@127.0.0.1:10000/<my_database>/_design/<my_designdoc>/_update/in-place-query/<mydocId>?field=title&value=test

Priklad: 

<i>Prikaz:</i> curl -X PUT http://zdenko:vino@127.0.0.1:10000/grainary/_design/Typologie/_update/in-place-query/?field=type&value=harvest

<i>CouchDB</i> 
[2] 28677
[1]   Done 


<h2>B.2 Views:</h2>

1. Typologie

Pristup k naprogramovanym views cez curl

<i>Prikaz:</i> curl -X GET http://zdenko:vino@127.0.0.1:10000/grainary/_design/Typologie/_view/Typologie

<i>CouchDB:</i> {"total_rows":5,"offset":0,"rows":[ <br>
{"id":"67f80e4db8ab23f8fb247e1a4d007ed7","key":"2013/07/15 15:52:20","value":{"Type":"container","Author":"Jan Testerovic"}},<br>
{"id":"67f80e4db8ab23f8fb247e1a4d009f3c","key":"2013/07/15 15:52:20","value":{"Type":"harvest","Author":"Jan Testerovic"}},<br>
{"id":"67f80e4db8ab23f8fb247e1a4d008597","key":"2014/05/15 15:52:20","value":{"Type":"container","Author":"Rudolf Rudolfovic"}},<br>
{"id":"67f80e4db8ab23f8fb247e1a4d0089f3","key":"2014/05/15 15:52:20","value":{"Type":"container","Author":"Rudolf Rudolfovic"}},<br>
{"id":"67f80e4db8ab23f8fb247e1a4d0096a5","key":"2014/05/15 15:52:20","value":{"Type":"harvest","Author":"Rudolf Rudolfovic"}}
]}<br>

<b>Respektíve pomocou -o moznosti sa nam priamo stiahne:</b>

<i>Prikaz:</i> curl -X GET http://zdenko:XXXXXX@127.0.0.1:10000/grainary/_design/Typologie/_view/Typologie -o ResponseTest.json

<i>CouchDB:</i>  
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed<br>
100   679    0   679    0     0   226k      0 --:--:-- --:--:-- --:--:--  331k

2. Upload nových views skrz SSH

<i>Príkaz:</i> curl -X PUT http://zdenko:XXXXX@127.0.0.1:10000/grainary/_design/grainary -d @more_views.json
