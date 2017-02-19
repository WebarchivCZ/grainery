# grainery
Keeping knowledge about harvested ARC/WARCs and related files such as logs, CDX files etc.


<b> 1.Vyhodene: </b>

?, "originalMimetype": "original_application_X-warc", <br>
sekvencia z harvestu:  "seq": 1, <br>
"dateOfOrigin": "exDateOfOrigin", <br>

<b> 2.Zamena </b><br>
Server ("server": "exServer",) = hostname crawlera vytvarajuceho warc <br>
HARVESTDATE - HARVESTDURATION <br>
ISPARTOF-HARVESTISPARTOF a HARVESTNAME - HARVESTISPARTOF , duplikacia odstranena <br>

<b>3.Presun </b><br>
OPERATOR ("operator": "exOperator") a DESCRIPTION z warcu do harvestu <br>
CDX z harvestu do warcu, rozsierenie o md5, pociet linii a velkost <br>
STORAGE z containeru do PATH <br>

<b> 4.Posun </b><br>

HARVESTISPARTOF v Harvest posunuto na #0CR <br>

<b> 5.Pridane</b><br>

Do HARVEST:  HOSTS - NUMBER + NAME /aby sme mohli operovat s potrojnou strukturou v harvestCrawl <br>
