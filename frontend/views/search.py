from flask import Blueprint, render_template, request
from config.config import mongo

smod = Blueprint('search', __name__)


@smod.route('/search', methods=['POST'])
def search():
    query = request.form['mainSearch']
    results = mongo.db.harvest.find(
        {
            '$text': {'$search': query}
        },
        {
            'harvest.harvestID': True,
            'harvest.harvestName': True,
            'harvest.dateOfValidation': True,
            'harvest.operator': True
        }
    )

    return render_template('search.html',
                           results=results,
                           query=query)
