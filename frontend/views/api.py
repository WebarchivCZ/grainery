from flask_restful import Resource
from flask import jsonify
from views.data import DataHarvest, DataContainer
from config.config import mongo


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
