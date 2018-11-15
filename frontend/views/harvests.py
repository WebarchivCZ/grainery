from flask import Blueprint, render_template
from views.functions import paginationQuery
from config.config import mongo, Config

hmod = Blueprint('harvests', __name__)


@hmod.route('/harvests/<page>')
def harvests(page):
    harvs = paginationQuery(mongo.db.harvest, int(page)-1)

    return render_template('harvests.html',
                           harvs=harvs[0],
                           limit=Config.ROW_LIMIT,
                           page=int(page),
                           max=harvs[1])


@hmod.route('/harvest/<id>')
def harvest(id):
    harv = mongo.db.harvest.find_one({'harvest.harvestID': id})
    return render_template('harvest.html', harv=harv)


@hmod.route('/containers/<harvestID>/<page>')
def containers(harvestID, page):
    containers = paginationQuery(mongo.db.container,
                                 int(page)-1,
                                 cond={'container.harvestID': harvestID}
                                 )

    return render_template('containers.html',
                           harvestID=harvestID,
                           containers=containers[0],
                           limit=Config.ROW_LIMIT,
                           page=int(page),
                           max=containers[1])


@hmod.route('/container/<id>')
def container(id):
    container = mongo.db.container.find_one({'container.recordID': id})
    return render_template('container.html', container=container)
