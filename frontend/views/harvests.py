from flask import Blueprint, render_template
from config.config import mongo

mod = Blueprint('harvests', __name__)


@mod.route('/harvests/')
def harvests():
    harvs = mongo.db.harvest.find({}, {'_id': True,
                                       'harvest.harvestName': True,
                                       'harvest.dateOfValidation': True,
                                       'harvest.operator': True
                                       }
                                  )
    return render_template('harvests_list.html', harvs=harvs)


@mod.route('/harvest/<id>')
def harvest(id):
    harv = mongo.db.harvest.find_one({'_id': id})
    return render_template('harvest.html', harv=harv)


@mod.route('/containers/<harvestID>')
def containers(harvestID):
    containers = mongo.db.container.find(
        {
            'container.harvestID': harvestID
        },
        {
            '_id': True,
            'container.filename': True,
            'container.dateOfOrigin': True
        }
    )
    return render_template('containers.html', containers=containers)


@mod.route('/container/<id>')
def container(id):
    container = mongo.db.container.find_one({'_id': id})
    return render_template('container.html', container=container)
