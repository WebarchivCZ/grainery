from datetime import datetime
import random
import uuid
from pymongo import MongoClient

# vytvoření mongo klienta
mongo = MongoClient()

# názevy databáze, kolekce pro sklizně a kolekce pro kontejnery
db = mongo.grainery
collection_harvest = db.hareasy
collection = db.coneasy

# cyklus pro generování sklizní
# generuju datum a uuid
for i in range(10):
    year = random.randint(2015, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 30)

    # vygenerování data
    date_harvest = datetime(year, month, day)

    # vygenerování UUID, používá se pak i při generování kontejneru
    harvestID = str(uuid.uuid4())

    # vytvoření jsonu z generovaných dat
    h = {"harvestID": harvestID, "type": "total", "date": date_harvest}

    # vložení jednoho záznamu do databáze
    collection_harvest.insert_one(h)

    # deklarace seznamu (list) kontejerů
    new_posts = []

    # cyklus pro vytvoření kontejnerů
    # generuju datum, velikost kontejneru, uuid
    for i in range(10000):
        hour = random.randint(1, 23)
        minute = random.randint(1, 59)
        second = random.randint(1, 59)
        date = datetime(year, month, day, hour, minute, second)

        # generátor velikosti kontejneru
        size = random.randint(900, 1200)

        # přidělení uuid kontejneru
        containerID = str(uuid.uuid4())

        # přidání položky do seznamu kontejnerů (json)
        new_posts.append({
            "date": date,
            "size": size,
            "harvestID": harvestID,
            "containerID": containerID
        })

# po ukončení cyklu vložím list záznamů do databáze
result = collection.insert_many(new_posts)
