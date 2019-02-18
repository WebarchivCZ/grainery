from flask import Blueprint, render_template, request
from datetime import datetime
from config.config import mongo

smod = Blueprint('search', __name__)


def logSearch(query):
    """logování výsledku vyhledávání, dostane query z formuláře a doplní datum,
    které uloží do souboru /logs/searchlog.txt, zkontroluje zda se podaří
    soubor otevřít a zda má práva do něj zapisovat.
    Pro správnou funkci musí existovat složka /logs,
    stejně jako u ostatních logů. Grainery se jí pokusí vytvořit již
    při startu aplikace, tak to nemusí zkoušet zde."""
    try:
        f = open('logs/searchlog.txt', 'a+')
    except FileNotFoundError:
        print("Missing directory /logs "
              "Search logging is off. For more information see"
              "https://github.com/WebarchivCZ/grainery/wiki/")
        return
    except PermissionError as e:
        print(str(e) + " Search logging is off. For more information see"
              "https://github.com/WebarchivCZ/grainery/wiki/")
        return

    date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    f.write(f'"{query}";"{date}"\n')
    f.close()


@smod.route('/search', methods=['POST'])
def search():
    # Pole, ve kterých se prohledává se nastavují přímo v MongoDB
    # konkrétně v indexu s název 'text' v MongoDB
    # index 'text' musí být vytvořen alespoň s jedním polem, jinak tato stránka
    # vrátí err, defaultní index:
    # db.harvest.createIndex( { "harvest.harvestName": "text",
    #                           "harvest.description": "text",
    #                           "paths.harvestID": "text" } )
    if request.method == 'POST':
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

        return render_template('search.html', results=results, query=query)
    else:
        return render_template('index.html')
