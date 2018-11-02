from pymongo import MongoClient
from datetime import datetime, timedelta
from random import randint, choice
from uuid import uuid4
from hashlib import md5

mongo = MongoClient()

db = mongo.grainery
collection_harvest = db.harvest
collection_container = db.container

# Vygenerování sklizně
for i in range(randint(10, 20)):
    year = randint(2015, 2018)
    month = randint(1, 12)
    day = randint(1, 27)
    hour = randint(1, 23)
    minute = randint(1, 59)
    second = randint(1, 59)

    types = ['V1M', 'V2M', 'V6M', 'V12M', 'V-1' 'CZ', 'T']

    # hlavička grainery
    grainery_type = 'harvest'
    grainery_author = 'NKCR'
    grainery_date = datetime.now()
    grainery_standard = 'Grainery 1.0'

    # harvest
    harvest_type = choice(types)
    harvest_name = harvest_type + "_" + str(datetime(year, month, day).date())
    harvest_date = datetime(year, month, day, hour, minute, 0)
    harvest_ID = str(uuid4())
    harvest_size = randint(100000, 10000000)
    harvest_dateOfValidation = datetime.now() \
        + timedelta(days=randint(1, 20))
    harvest_nextValidation = harvest_dateOfValidation + timedelta(days=730)

    # harvestCrawl
    harvest_logs = True
    harvest_path = 'logs/crawl'
    harvest_file = ['crawler00.tar.gz', 'crawler01.tar.gz', 'crawler03.tar.gz']

    # commentaries
    harvest_exists = False
    harvest_commentaries = ''

    # vložení sklizně do databáze
    h = {
        "type": grainery_type,
        "author": grainery_author,
        "date": grainery_date,
        "standard": grainery_standard,
        "harvest": {
            "harvestName": harvest_name,
            "date": harvest_date,
            "harvestID": harvest_ID,
            "harvestType": harvest_type,
            "size": harvest_size,
            "dateOfValidation": harvest_dateOfValidation,
            "nextValidation": harvest_nextValidation
        },
        "harvestCrawl": {
            "logs": harvest_logs,
            "path": harvest_path,
            "filename": harvest_file
        },
        "commentaries": {
            "exists": harvest_exists,
            "text": harvest_commentaries
        }
    }

    collection_harvest.insert_one(h)

    # Vygenerování kontejneru
    for i in range(randint(10000, 30000)):

        hour = randint(1, 23)
        minute = randint(1, 59)
        second = randint(1, 59)
        date = datetime(year, month, day, hour, minute, second)

        # hlavička grainery
        grainery_container_type = 'container'
        grainery_container_author = 'NKCR'
        grainery_container_date = datetime.now()
        grainery_container_standard = 'Grainery 1.0'

        # container
        container_filename = harvest_type + "_" \
            + str(date.date()) + "-crawler00.webarchiv.cz-warc.gz"
        container_recordID = str(uuid4())
        container_harvestID = harvest_ID
        container_dateOfOrigin = date
        container_size = randint(900, 1200)

        # cdx
        container_cdx_exists = True
        container_cdx_path = './logs/index/' + container_filename \
            + "-crawler00.webarchiv.cz-warc.gz.cdx"
        container_cdx_md5 = md5(container_filename.encode('utf-8')).hexdigest()
        container_cdx_size = round(container_size*0.15)
        container_cdx_columns = randint(9, 11)
        container_cdx_lines = randint(100000, 999999)

        # format
        container_format = 'WARC File Format 1.0'
        container_conformsTo = 'https://iipc.github.io/warc-specifications/' \
            + 'specifications/warc-format/warc-1.0/'
        container_mimetype = 'application/warc'

        # md5
        container_dateOfValidation = datetime.now() \
            + timedelta(days=randint(1, 20))
        container_statusOfValidation = True
        container_nextValidation = container_dateOfValidation \
            + timedelta(days=730)
        container_hash = md5(container_recordID.encode('utf-8')).hexdigest()

        c = {
            "type": grainery_container_type,
            "author": grainery_container_author,
            "date": grainery_container_date,
            "standard": grainery_container_standard,
            "container": {
                "filename": container_filename,
                "recordID": container_recordID,
                "harvestID": container_harvestID,
                "dateOfOrigin": container_dateOfOrigin,
                "size": container_size
            },
            "cdx": {
                "exists": container_cdx_exists,
                "path": container_cdx_path,
                "md5": container_cdx_md5,
                "size": container_cdx_size,
                "columns": container_cdx_columns,
                "lines": container_cdx_lines
            },
            "format": {
                "format": container_format,
                "conformsTo": container_conformsTo,
                "mimeType": container_mimetype
            },
            "md5": {
                "dateOfValidation": container_dateOfValidation,
                "statusOfValidation": container_statusOfValidation,
                "nextValidation": container_nextValidation,
                "hash": container_hash
            }

        }

    collection_container.insert_one(c)
