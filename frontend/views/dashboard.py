from flask import Blueprint, render_template
from config.config import mongo
from views.functions import lastImport


dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    collection_harvest = mongo.db.harvest

    return render_template('index.html',
                           last=lastImport(collection_harvest)
                           )


@dmod.route('/dashboard-containers')
def cdash():
    collection_container = mongo.db.container

    return render_template('cdash.html')
