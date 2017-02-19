# grainery
Keeping knowledge about harvested ARC/WARCs and related files such as logs, CDX files etc.


<b> 1.Vyhodene: </b>

?, "originalMimetype": "original_application_X-warc",
sekvencia z harvestu:  "seq": 1,
"dateOfOrigin": "exDateOfOrigin",

<b> 2.Zamena </b>
Server ("server": "exServer",) = hostname crawlera vytvarajuceho warc
HARVESTDATE - HARVESTDURATION
ISPARTOF-HARVESTISPARTOF a HARVESTNAME - HARVESTISPARTOF , duplikacia odstranena

# 3.Presun </b>
OPERATOR ("operator": "exOperator") a DESCRIPTION z warcu do harvestu
CDX z harvestu do warcu, rozsierenie o md5, pociet linii a velkost
STORAGE z containeru do PATH

# 4.Posun </b>

HARVESTISPARTOF v Harvest posunuto na #0CR

# 5.Pridane</b>

Do HARVEST:  HOSTS - NUMBER + NAME /aby sme mohli operovat s potrojnou strukturou v harvestCrawl
