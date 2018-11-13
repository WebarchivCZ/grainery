from flask_pymongo import pymongo
from config.config import Config


def paginationQuery(collection, page, limit=Config.ROW_LIMIT):
    """Vrátí stanovený počet řádků (limit) a přeskočí jich o offset
    (pouze pokud je offset vyšší než nula) a celkový počet řádků """
    offset = page * limit

    rows = collection.find() \
        .skip(offset if offset > 0 else 0) \
        .limit(limit) \
        .sort('_id', pymongo.ASCENDING)

    return (rows, rows.count())


def lastImport(collection):
    """Vrátí poslední vytvořený záznam v kolekci"""
    return collection.find_one({},
                               {'date': True,
                                'standard': True,
                                'harvest': True},
                               sort=[('_id', pymongo.DESCENDING)]
                               )
