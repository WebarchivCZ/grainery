from flask_pymongo import pymongo
from config.config import Config
import pandas as pd


def paginationQuery(collection, page, cond={}, limit=Config.ROW_LIMIT):
    """Vrátí stanovený počet řádků (limit) a přeskočí jich o offset
    (pouze pokud je offset vyšší než nula) a celkový počet řádků """
    offset = page * limit

    rows = collection.find(cond) \
        .skip(offset if offset > 0 else 0) \
        .limit(limit) \
        .sort('_id', pymongo.ASCENDING)

    return (rows, rows.count())


def lastImport(collection, type='harvest'):
    """Vrátí poslední vytvořený záznam v kolekci"""

    if type == 'harvest':
        query = {'date': True,
                 'standard': True,
                 'paths.harvestID': True,
                 'harvest.harvestName': True,
                 'harvest.status': True,
                 'harvest.date': True,
                 'harvest.size': True,
                 'harvest.description': True
                 }
    else:
        query = {'date': True,
                 'standard': True,
                 'container.isPartOf': True,
                 'container.filename': True,
                 'container.contentLength': True,
                 'container.size': True,
                 'container.dateOfOrigin': True,
                 'paths.harvestID': True
                 }

    return collection.find_one({}, query,
                               sort=[('_id', pymongo.DESCENDING)]
                               )


def dataframeFromColumn(cursor, column):
    """ Vytvoří vlastní dataframe ze sloupce, který obsahuje pouze
        dictionary  """
    df = pd.DataFrame(list(cursor))
    listOfHarvests = []

    for row in df[column]:
        listOfHarvests.append(row)

    return pd.DataFrame(listOfHarvests)
