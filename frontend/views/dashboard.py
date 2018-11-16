from flask import Blueprint, render_template
from config.config import mongo
from views.functions import lastImport, dataframeFromColumn
from views.figures import harvestPerYear

dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    cursor = mongo.db.harvest.find({}, {'harvest': True})

    df = dataframeFromColumn(cursor, column='harvest')

    # create new column only for year
    df['year'] = df['date'].dt.year

    # 1st plot
    #
    # data for first plot
    harvest_counts = df['year'].value_counts().sort_index(ascending=True)

    # Embed plot into HTML via Flask Render
    script, div = harvestPerYear(harvest_counts.index, harvest_counts.values)

    return render_template('index.html',
                           last=lastImport(mongo.db.harvest),
                           script=script,
                           div=div
                           )


@dmod.route('/dashboard-containers')
def cdash():
    return render_template('cdash.html')
