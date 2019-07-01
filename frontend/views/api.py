from flask import jsonify

from config.config import mongo
from flask_restful import Resource
from views.data import DataContainer, DataHarvest


class Harvests(Resource):
    def __init__(self):
        self.data = DataHarvest(mongo.db.harvest)

    def get(self):
        docs = []

        for doc in self.data.listQuery():
            docs.append(doc)

        return jsonify(docs)


class Harvest(Resource):
    def __init__(self):
        self.data = DataHarvest(mongo.db.harvest)

    def get(self, id):
        return jsonify(self.data.oneQuery(id))


class Containers(Resource):
    def __init__(self):
        self.data = DataContainer(mongo.db.container)

    def get(self, harvestID):
        docs = []

        for doc in self.data.listQuery(harvestID):
            docs.append(doc)

        return jsonify(docs)


class Container(Resource):
    def __init__(self):
        self.data = DataContainer(mongo.db.container)

    def get(self, id):
        return jsonify(self.data.oneQuery(id))
