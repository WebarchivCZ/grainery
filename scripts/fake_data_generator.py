from datetime import datetime
import random
import uuid
from pymongo import MongoClient
from hashlib import md5

# vytvoření mongo klienta
mongo = MongoClient()

# název databáze, kolekce pro sklizně a kolekce pro kontejnery
db = mongo.grainery
collection_harvest = db.hareasy
collection = db.coneasy

#
# Vygenerování sklizně
#
for i in range(random.randint(10, 20)):

    # náhodně vygeneuji datum
    year = random.randint(2015, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 30)
    hour = random.randint(1, 23)
    minute = random.randint(1, 59)
    second = random.randint(1, 59)

    # seznam možných typů sklizní
    types = ['1M_archiveit', '2M_archiveit',
             '12M_archiveit', 'domain', 'topic']

    # hlavička grainery
    grainery_type = 'harvest'
    grainery_author = 'Rudolf'
    grainery_date = str(datetime.now())
    grainery_standard = 'Grainery 1.0'

    #
    # začátek generování sklizně
    #

    # náhodně vyberu jeden typ sklizně
    harvest_type = random.choice(types)

    # datum sklizně
    harvest_date = datetime(year, month, day, hour, minute, 0)

    # složím název sklizně z data a typu
    harvest_name = harvest_type + "_" + str(harvest_date.date())

    # generuji uuid, velikost a jestli má nebo nemá sklizeň logy
    harvest_ID = str(uuid.uuid4())
    harvest_size = random.randint(100000, 10000000)
    harvest_logs = random.choices([True, False])

    # vytvořím dictionary pro mongo
    h = {"type": grainery_type, "author": grainery_author,
         "date": grainery_date, "standard": grainery_standard,
         "harvest_name": harvest_name, "harvest_date": harvest_date,
         "harvest_ID": harvest_ID, "harvest_type": harvest_type,
         "harvest_size": harvest_size, "harvest_logs": harvest_logs}

    # vložím do mongodb
    collection_harvest.insert_one(h)

    #
    # začátek generování kontejneru
    #

    # deklarace seznamu (list) kontejerů
    new_posts = []

    for i in range(random.randint(10000, 30000)):
        # znovu generuji časy, aby byly rozdílné pro každý kontejner
        hour = random.randint(1, 23)
        minute = random.randint(1, 59)
        second = random.randint(1, 59)

        # datum pro filename
        container_date = datetime(year, month, day,
                                  hour, minute, second).date()
        # filename složím z typu sklizně, data a statické přípony
        container_filename = harvest_type + "_" + str(container_date) \
            + "-crawler00.webarchiv.cz-warc.gz"

        # harvest id je stejné jako u mateřské sklizně
        container_harvestID = harvest_ID

        # generuji nové uuid pro kontejner a velikost
        container_ID = str(uuid.uuid4())
        container_size = random.randint(90000, 1200000)

        # cdx vžddy existuje, generuji mu md5, velikost, počet sloupců a řádků
        container_cdx = True
        container_cdx_md5 = md5(container_filename.encode('utf-8')).hexdigest()
        container_cdx_size = round(container_size*0.15)
        container_cdx_columns = random.randint(9, 11)
        container_cdx_lines = random.randint(100000, 999999)

        # md5 pro kontejner
        container_md5 = md5(container_ID.encode('utf-8')).hexdigest()

        # staticky info k formátu kontejneru
        container_format = 'WARC File Format 1.0'
        container_format_to = 'https://iipc.github.io/warc-specifications/ \
                               specifications/warc-format/warc-1.0/'
        container_format_mime = 'application/warc'

        new_posts.append({
            "type": grainery_type, "author": grainery_author,
            "date": grainery_date, "standard": grainery_standard,
            "container_filename": container_filename,
            "container_ID": container_ID,
            "container_harvestID": container_harvestID,
            "container_size": container_size,
            "container_cdx": container_cdx,
            "container_cdx_md5": container_cdx_md5,
            "container_cdx_size": container_cdx_size,
            "container_cdx_columns": container_cdx_columns,
            "container_cdx_lines": container_cdx_lines,
            "container_md5": container_md5,
            "container_format": container_format,
            "container_format_to": container_format_to,
            "container_format_mime": container_format_mime
        })


# po ukončení cyklu vložím list záznamů do databáze
# to je hlavně z důvodů, abych si vyzkpoušel oběd metody insert_one (many)
result = collection.insert_many(new_posts)
