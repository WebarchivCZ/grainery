from flask import Blueprint, render_template, request
from config.config import mongo

smod = Blueprint('search', __name__)


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
