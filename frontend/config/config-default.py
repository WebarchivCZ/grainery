# fill and rename file to config.py
from flask_pymongo import PyMongo
mongo = PyMongo()


class Config(object):
    # basic security settings
    DEBUG = False

    # mongodb connection settings
    DBNAME = ''
    HOST = ''
    PORT = '27017'


class ProductionConfig(Config):
    # mongodb user credentials for production run
    USERNAME = ''
    PASSWORD = ''
    MONGO_URI = ('mongodb://'
                 + USERNAME
                 + ':'
                 + PASSWORD
                 + '@'
                 + Config.HOST
                 + ':'
                 + Config.PORT
                 + '/'
                 + Config.DBNAME)


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = ('mongodb://'
                 + Config.HOST
                 + ':'
                 + Config.PORT
                 + '/'
                 + Config.DBNAME)
