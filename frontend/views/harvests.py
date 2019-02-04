from flask import Blueprint, render_template
from views.data import Data
from config.config import mongo

hmod = Blueprint('harvests', __name__)


@hmod.route('/harvests/<page>')
def harvests(page):
    data = Data(mongo.db.harvest)
    harvs = data.paginationQuery(int(page) - 1)

    return render_template('harvests.html',
                           harvs=harvs[0],
                           limit=data.limit,
                           page=int(page),
                           max=harvs[1])


@hmod.route('/harvest/<id>')
def harvest(id):
    data = Data(mongo.db.harvest)
    harv = data.collection.find_one({'paths.harvestID': id})
    return render_template('harvest.html', harv=harv)


@hmod.route('/containers/<harvestID>/<page>')
def containers(harvestID, page):
    data = Data(mongo.db.container)
    containers = data.paginationQuery(int(page) - 1,
                                      cond={'paths.harvestID': harvestID}
                                      )

    return render_template('containers.html',
                           harvestID=harvestID,
                           containers=containers[0],
                           limit=data.limit,
                           page=int(page),
                           max=containers[1])


@hmod.route('/container/<id>')
def container(id):
    container = mongo.db.container.find_one({'container.filename': id})
    return render_template('container.html', container=container)


@hmod.route('/cdxs/<page>')
def cdxs(page):
    data = Data(mongo.db.cdx)
    indexes = data.paginationQuery(int(page)-1)

    return render_template('cdxs.html',
                           cdxs=indexes[0],
                           limit=data.limit,
                           page=int(page),
                           max=indexes[1])


@hmod.route('/cdx/<id>')
def cdx(id):
    indx = mongo.db.harvest.find_one({'cdx.md5': id})
    return render_template('cdx.html', indx=indx)
