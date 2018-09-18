from flask import Blueprint, render_template
from views.functions import paginationQuery
from config.config import mongo, Config

mod = Blueprint('harvests', __name__)


@mod.route('/harvests/<page>')
def harvests(page):
    harvs = paginationQuery(mongo.db.harvest, int(page)-1)

    return render_template('harvests.html',
                           harvs=harvs[0],
                           limit=Config.ROW_LIMIT,
                           page=int(page),
                           max=harvs[1])


@mod.route('/harvest/<id>')
def harvest(id):
    harv = mongo.db.harvest.find_one({'harvest.harvestID': id})
    return render_template('harvest.html', harv=harv)


@mod.route('/containers/<harvestID>')
def containers(harvestID):
    containers = mongo.db.container.find(
        {
            'container.harvestID': harvestID
        },
        {
            'container.recordID': True,
            'container.filename': True,
            'container.dateOfOrigin': True
        }
    )
    return render_template('containers.html',
                           containers=containers,
                           id=harvestID
                           )


@mod.route('/container/<id>')
def container(id):
    container = mongo.db.container.find_one({'container.recordID': id})
    return render_template('container.html', container=container)
