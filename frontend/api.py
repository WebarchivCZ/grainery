from flask_restful import Resource


class Harvests(Resource):
    def get(self):
        return "Všechny sklizně"


class Harvest(Resource):
    def get(self, id):
        return "sklizeň " + id
