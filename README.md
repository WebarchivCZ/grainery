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
<ul>Deklarativne zlozky
<li><b>author</b>: autor ci skript, ktory vklada dokument</li>
<li><b>date</b>: moment zapisu</li>
<li><b>standart</b>: štandard pre formátovanie JSONU - k príp. updatom</li>
<li><b>type</b>: typ dokumentu, tj. harvest alebo jeho container</li></ul>
