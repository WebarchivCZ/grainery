from flask_pymongo import pymongo
from config.config import Config
from bitmath import Byte
import pandas as pd


class Data():
    """ handling data for vizualization """

    def __init__(self, collection, limit=Config.ROW_LIMIT):
        self.limit = limit
        self.collection = collection

    def paginationQuery(self, page, cond={}):
        """Vrátí stanovený počet řádků (limit) a přeskočí jich o offset
        (pouze pokud je offset vyšší než nula) a celkový počet řádků """
        offset = page * self.limit

        rows = self.collection.find(cond) \
            .skip(offset if offset > 0 else 0) \
            .limit(self.limit) \
            .sort('_id', pymongo.ASCENDING)

        return (rows, rows.count())

    def dataframeFromColumn(self, column):
        """ Vytvoří vlastní dataframe ze sloupce, který obsahuje
            dictionary  """
        df = pd.DataFrame(list(self.cursor))
        x = []

        for row in df[column]:
            x.append(row)

        return pd.DataFrame(x)


class DataHarvest(Data):
    """ specific data handlig for harvest """

    def __init__(self, collection, limit=Config.ROW_LIMIT):
        super().__init__(collection, limit)
        self.cursor = self.collection.find({}, {'harvest': True})
        self.df = super().dataframeFromColumn('harvest')

        # create new column only for year
        self.df['year'] = self.df['date'].str.slice(0, 4).astype(int)

    def lastImport(self):
        """Vrátí poslední vytvořený záznam v kolekci"""
        query = {'date': True,
                 'standard': True,
                 'paths.harvestID': True,
                 'harvest.harvestName': True,
                 'harvest.status': True,
                 'harvest.date': True,
                 'harvest.size': True,
                 'harvest.description': True
                 }

        return self.collection.find_one({}, query,
                                        sort=[('_id', pymongo.DESCENDING)]
                                        )

    def harvestCounts(self, column):
        "vrátí počet sklizní za každý rok"
        return self.df[column].value_counts().sort_index(ascending=True)

    def yearSize(self, unit='TB'):
        """vrátí velikost sklizní za každý rok v jednotkách lidsky čitelných
         a zároveň popis osy y"""

        # musí se převést na float kvůli převodu jednotek níže
        s = self.df.groupby('year')['size'].sum().astype('float')
        y_axis_label = "Size in " + unit

        # převádí jednotky z bytů na GB pomocí knihovny bitmath.
        # Pokud je jiná vstupní musí se vyměnit funkce Byte() za adekvátní
        # v případě jiné výstupní jednotky se mění atribut (TB, MB, atd.)
        if unit == 'TB':
            for i, v in s.items():
                s[i] = float(Byte(s[i]).TB)
        else:
            for i, v in s.items():
                s[i] = float(Byte(s[i]).GB)

        return s, y_axis_label

    def growth(self, yearsize):
        "vrátí růst velikostí archivu po letech"
        size = []

        for i in yearsize:
            size.append(i + sum(size))

        return size


class DataContainer(Data):
    """ specific data handlig for container """

    def __init__(self, collection, limit=Config.ROW_LIMIT):
        super().__init__(collection, limit)
        self.cursor = \
            self.collection.aggregate([{"$group":
                                        {"_id": "$container.isPartOf",
                                         "count": {"$sum": 1}}
                                        },
                                       {'$sort': {'container.dateOfOrigin': 1}
                                        }
                                       ])
        self.df = pd.DataFrame(list(r for r in self.cursor))

    def lastImport(self):
        """Vrátí poslední vytvořený záznam v kolekci"""

        query = {'date': True,
                 'standard': True,
                 'container.isPartOf': True,
                 'container.filename': True,
                 'container.contentLength': True,
                 'container.size': True,
                 'container.dateOfOrigin': True,
                 'paths.harvestID': True
                 }

        return self.collection.find_one({}, query,
                                        sort=[('_id', pymongo.DESCENDING)]
                                        )


class dataCdx(Data):
    """ specific data handlig for cdx (TODO) """
    pass
