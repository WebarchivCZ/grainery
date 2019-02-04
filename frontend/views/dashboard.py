from flask import Blueprint, render_template
import pandas as pd
from config.config import mongo
from views.data import DataHarvest, DataContainer
from views.figures import Figures

dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    dh = DataHarvest(mongo.db.harvest)

    df = dh.dataframeFromColumn(column='harvest')
    gf = Figures()

    # create new column only for year
    df['year'] = df['date'].str.slice(0, 4).astype(int)

    # 1st plot
    # data for first plot
    harvest_counts = dh.harvestCounts(df['year'])

    # Embed plot into HTML via Flask Render
    script, div = gf.harvestPerYear(harvest_counts.index,
                                    harvest_counts.values)
    # 2nd
    wa_yearsize = dh.yearSize(df)
    script2, div2 = gf.sizePerYear(wa_yearsize.index, wa_yearsize.values)

    # 3rd
    script3, div3 = gf.sizeGrowth(wa_yearsize.index, dh.growth(wa_yearsize))

    # 4th
#    harvest_types = df['harvestType'].value_counts()
#    script4, div4 = typesPie(harvest_types)

    return render_template('index.html',
                           last=dh.lastImport(),
                           script=script, div=div,
                           script2=script2, div2=div2,
                           script3=script3, div3=div3,
                           #   script4=script4, div4=div4,
                           )


@dmod.route('/dashboard-containers')
def cdash():
    dc = DataContainer(mongo.db.container)
    gf = Figures()
    # 1st
    df_containers = pd.DataFrame(list(r for r in dc.cursor))

    script, div = gf.containerCount(df_containers)

    return render_template('cdash.html',
                           last=dc.lastImport(),
                           script=script, div=div)
