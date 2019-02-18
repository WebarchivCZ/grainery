from flask_pymongo import PyMongo
mongo = PyMongo()


class Config(object):
    # database settings

    # mongo connection settings
    DBNAME = 'grainery'
    PORT = '27017'
    HOST = ''

    # mongodb user credentials
    USERNAME = ''
    PASSWORD = ''

    # app parameters settings
    # debug mode, for production run should be false
    DEBUG = False

    # number of rows in tables
    ROW_LIMIT = 50

    # nastavení kodování pro json výstup v UTF8
    JSON_AS_ASCII = False

    # creating mongo URI
    if USERNAME != '' and PASSWORD != '':
        MONGO_URI = ('mongodb://'
                     + USERNAME
                     + ':'
                     + PASSWORD
                     + '@'
                     + HOST
                     + ':'
                     + PORT
                     + '/'
                     + DBNAME)
    else:
        MONGO_URI = ('mongodb://'
                     + HOST
                     + ':'
                     + PORT
                     + '/'
                     + DBNAME)
