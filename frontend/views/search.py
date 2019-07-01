from datetime import datetime

from flask import Blueprint, render_template, request

from config.config import Config, mongo
from flask_pymongo import pymongo

smod = Blueprint('search', __name__)


def logSearch(query):
    """logování výsledku vyhledávání, dostane query z formuláře a doplní datum,
    které uloží do souboru /logs/searchlog.txt, zkontroluje zda se podaří
    soubor otevřít a zda má práva do něj zapisovat.
    Pro správnou funkci musí existovat složka /logs,
    stejně jako u ostatních logů. Grainery se jí pokusí vytvořit již
    při startu aplikace, tak to nemusí zkoušet zde."""
    try:
        with open(Config.LOG_PATH + '/searchlog.txt', 'a') as f:
            date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            f.write(f'"{query}";"{date}"\n')
    except FileNotFoundError:
        print("Missing directory /logs "
              "Search logging is off. For more information see "
              "https://github.com/WebarchivCZ/grainery/wiki/")
        return
    except PermissionError as e:
        print(str(e) + " Search logging is off. For more information see "
              "https://github.com/WebarchivCZ/grainery/wiki/")
        return


@smod.route('/search', methods=['POST'])
def search():
    # Pole, ve kterých se prohledává se nastavují přímo v MongoDB
    # konkrétně v indexu s název 'text' v MongoDB
    # index 'text' musí být vytvořen alespoň s jedním polem, jinak tato stránka
    # vrátí err, defaultní index:
    # db.harvest.createIndex( { "harvest.harvestName": "text",
    #                           "harvest.description": "text",
    #                           "paths.harvestID": "text" } )

    query = request.form['query']
    logSearch(query)

    results = mongo.db.harvest.find(
        {
            '$text': {'$search': query}
        },
        {
            'paths.harvestID': True,
            'harvest.harvestName': True,
            'harvest.date': True,
            'harvest.operator': True
        }
    )

    try:
        return render_template('search.html', results=results,
                               query=query, length=results.count())
    # odchycení chyby, když je při instalaci zapomenuto na vytvoření indexu
    except pymongo.errors.OperationFailure:
        error = ("No fulltext index is set."
                 "See https://github.com/WebarchivCZ/grainery/wiki/")

        return render_template('search.html', results={},
                               query=query, error=error)
