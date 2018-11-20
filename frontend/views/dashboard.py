from flask import Blueprint, render_template
from config.config import mongo
from views.functions import lastImport, dataframeFromColumn
from views.figures import harvestPerYear, sizePerYear, sizeGrowth

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

    # 2nd
    wa_yearsize = df.groupby('year')['size'].sum()
    script2, div2 = sizePerYear(wa_yearsize.index, wa_yearsize.values)

    # 3rd
    size = []
    for i in wa_yearsize:
        size.append(i+sum(size))

    script3, div3 = sizeGrowth(wa_yearsize.index, size)

    return render_template('index.html',
                           last=lastImport(mongo.db.harvest),
                           script=script,
                           div=div,
                           script2=script2,
                           div2=div2,
                           script3=script3,
                           div3=div3,
                           )


@dmod.route('/dashboard-containers')
def cdash():
    return render_template('cdash.html')
