from pymongo import MongoClient
from datetime import datetime, timedelta
from random import randint, choice
from uuid import uuid4
from hashlib import md5

mongo = MongoClient()

db = mongo.grainery
collection_harvest = db.harvest
collection_container = db.container
collection_cdx = db.cdx

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
    grainery_standard = 'Grainery 0.35'

    # harvest
    harvest_type = choice(types)
    harvest_name = harvest_type + "_" + str(datetime(year, month, day).date())
    harvest_date = datetime(year, month, day, hour, minute, 0)
    harvest_size = randint(100000, 10000000)
    harvest_dateOfValidation = datetime.now() \
        + timedelta(days=randint(1, 20))
    harvest_nextValidation = harvest_dateOfValidation + timedelta(days=730)
    harvest_audience = 'Webarchiv.cz users'
    harvest_status = 'NonValidated'
    harvest_from = 'webarchiv@nkp.cz'
    harvest_publisher = 'National Library of the Czech Republic - Webarchiv.cz'
    harvest_robots = 'ignore'
    harvest_operator = 'Zdenko Vozar'
    harvest_description = 'Výběrová sklizeň webů'
    harvest_agent = 'Mozilla/5.0 (compatible; heritrix/3.2.0 \
        +http://webarchiv.cz/kontakty/...'

    # harvestCrawl
    harvest_logs = True
    harvest_path = 'logs/crawl'
    harvest_file = ['crawler00.tar.gz', 'crawler01.tar.gz', 'crawler03.tar.gz']

    # path
    harvest_ID = str(uuid4())

    # commentaries
    harvest_exists = False
    harvest_commentaries = 'NA'

    # vložení sklizně do databáze
    collection_harvest.insert_one(
        {
            "recType": grainery_type,
            "author": grainery_author,
            "date": grainery_date,
            "standard": grainery_standard,
            "harvest": {
                # "harvestType": harvest_type,
                "harvestNameFull": harvest_name,
                "harvestType": harvest_type,
                "harvestSuffix": harvest_name.split('_'),
                "date": harvest_date,
                "size": harvest_size,
                # "audience": harvest_audience,
                "publisher": harvest_publisher,
                "robots": harvest_robots,
                # "harvestDuration": "NA",
                "operator": harvest_operator,
                "http-header-from": harvest_agent,
                # "description": harvest_description,
                "status": harvest_status
            },
            "harvestCrawl": {
                "logs": harvest_logs,
                "path": harvest_path,
                "filename": harvest_file
            },
            "paths": {
                # "mount": "NA",
                "harvestID": harvest_ID,
                # "pathToHarvest": "NA",
                # "LTP": "NA",
                # storage": "NA",
                # "cdxID": "NA"
            },
            "revision": {
                "dateOfValidation": harvest_dateOfValidation,
                "nextLastDateOfValidation": harvest_nextValidation,
                "hashLast": "NA",
                "hashOrig": "NA",
                "statusOfValidation": "NA"
            },
            "commentaries": {
                "exists": harvest_exists,
                "text": harvest_commentaries
            }
        }
    )

    # Vygenerování kontejneru
    for i in range(randint(100, 300)):

        hour = randint(1, 23)
        minute = randint(1, 59)
        second = randint(1, 59)
        date = datetime(year, month, day, hour, minute, second)

        # hlavička grainery
        grainery_container_type = 'container'
        grainery_container_author = 'NKCR'
        grainery_container_date = datetime.now()
        grainery_container_standard = 'Grainery 0.35'

        # container
        container_filename = harvest_type + "_" \
            + str(date.date()) + "-crawler00.webarchiv.cz-warc.gz"
        container_recordID = str(uuid4())
        container_dateOfOrigin = date
        container_size = randint(900, 1200)
        container_isPartOf = harvest_name
        container_ip = '10.3.0.23'
        container_hostname = 'crawler00.webarchiv.cz'
        container_operator = harvest_operator
        container_contentLength = container_size - 100
        container_robot = harvest_robots
        container_software = 'Heritrix/3.2.0 http://crawler.archive.org'

        # cdx
        container_cdx_exists = True
        container_cdx_path = f"./logs/index/{container_filename}-crawler00.webarchiv.cz-warc.gz.cdx"
        container_cdx_md5 = md5(
            container_filename.encode('utf-8')).hexdigest()
        container_cdx_size = round(container_size*0.15)
        container_cdx_columns = randint(9, 11)
        container_cdx_lines = randint(100000, 999999)
        container_cdx_version = "openwayback 1.2"

        # paths
        container_harvestID = harvest_ID

        # type
        container_format = 'WARC File Format 1.0'
        container_conformsTo = 'https://iipc.github.io/warc-specifications/' \
            + 'specifications/warc-format/warc-1.0/'
        container_mimetype = 'application/warc'
        container_warcType = 'warcinfo'

        # revision
        container_dateOfValidation = datetime.now() \
            + timedelta(days=randint(1, 20))
        container_statusOfValidation = True
        container_nextValidation = container_dateOfValidation \
            + timedelta(days=730)
        container_hash = md5(container_recordID.encode('utf-8')).hexdigest()

        collection_container.insert_one(
            {
                "recType": grainery_container_type,
                "author": grainery_container_author,
                "date": grainery_container_date,
                "standard": grainery_container_standard,
                "container": {
                    "filename": container_filename,
                    "warcID": container_recordID,
                    "isPartOf": container_isPartOf,
                    "hostname": container_hostname,
                    "ip": container_ip,
                    "contentLength": container_contentLength,
                    "operator": container_operator,
                    "publisher": "Narodni knihovna CR",
                    "audience": "Narodni knihovna CR users",
                    "robots": container_robot,
                    "dateOfOrigin": container_dateOfOrigin,
                    "software": container_software,
                    "size": container_size
                },
                "paths": {
                    "harvestID": container_harvestID
                },
                "type": {
                    "format": container_format,
                    "warcType": container_warcType,
                    "conformsTo": container_conformsTo,
                    "mimeType": container_mimetype
                },
                "revision": {
                    "dateOfValidation": container_dateOfValidation,
                    "statusOfValidation": container_statusOfValidation,
                    "nextLastDateValidation": container_nextValidation,
                    "hashOrigin": container_hash,
                    "hastLast": "NA"
                }
            }
        )

        collection_cdx.insert_one(
            {
                "recType": grainery_container_type,
                "author": grainery_container_author,
                "date": grainery_container_date,
                "standard": grainery_container_standard,
                "cdx": {
                    "exists": container_cdx_exists,
                    "path": container_cdx_path,
                    "md5": container_cdx_md5,
                    "size": container_cdx_size,
                    "columns": container_cdx_columns,
                    "lines": container_cdx_lines,
                    "version": container_cdx_version
                },
                "revision": {
                    "dateOfValidation": container_dateOfValidation,
                    "statusOfValidation": container_statusOfValidation,
                    "nextLastDateValidation": container_nextValidation,
                    "hashOrigin": container_hash,
                    "hastLast": "NA"
                }
            }
        )
