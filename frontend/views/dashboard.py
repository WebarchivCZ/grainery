from flask import Blueprint, render_template
import pandas as pd
from config.config import mongo
from views.functions import lastImport, dataframeFromColumn
from views.figures import harvestPerYear, sizePerYear, sizeGrowth, \
    typesPie, containerCount

dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    cursor = mongo.db.harvest.find({}, {'harvest': True})

    df = dataframeFromColumn(cursor, column='harvest')

    # create new column only for year
    df['year'] = df['date'].str.slice(0, 4)
    roky = []
    for x in df['year']:
        roky.append(int(x))

    df['year'] = roky

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

    # 4th
#    harvest_types = df['harvestType'].value_counts()
#    script4, div4 = typesPie(harvest_types)

    return render_template('index.html',
                           last=lastImport(mongo.db.harvest),
                           script=script, div=div,
                           script2=script2, div2=div2,
                           script3=script3, div3=div3,
                           #   script4=script4, div4=div4,
                           )


@dmod.route('/dashboard-containers')
def cdash():
    # 1st
    # TODO nahradit harvestID za ispartof?
    agg_containers = [{"$group": {"_id": "$container.isPartOf",
                                  "count": {"$sum": 1}
                                  }},
                      {'$sort': {'container.dateOfOrigin': 1}
                       }]

    cursor_containers = mongo.db.container.aggregate(agg_containers)

    df_containers = pd.DataFrame(list(r for r in cursor_containers))

    script, div = containerCount(df_containers)

    return render_template('cdash.html',
                           last=lastImport(mongo.db.container, 'container'),
                           script=script, div=div)
