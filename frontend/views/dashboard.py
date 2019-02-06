from flask import Blueprint, render_template
from config.config import mongo
from views.data import DataHarvest, DataContainer
from views.figures import ContainerFigures, HarvestFigures

dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    dh = DataHarvest(mongo.db.harvest)
    gf = HarvestFigures(dh)

    script, div = gf.harvestPerYear()
    script2, div2 = gf.sizePerYear()
    script3, div3 = gf.sizeGrowth()

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
    gf = ContainerFigures(dc)

    script, div = gf.containerCount()

    return render_template('cdash.html',
                           last=dc.lastImport(),
                           script=script, div=div)
