from flask_pymongo import PyMongo
mongo = PyMongo()


class Config(object):
    """class where is stored essential setting for application """
    # app parameters settings:
    # debug mode, for production run should be false
    DEBUG = False

    # number of rows in tables
    ROW_LIMIT = 50

    # path to logs directory depends where the application is running
    # if is running directly from frontend directory,
    # the path should be just /logs
    # if it's running from grainery/frontend it should be frontend/logs, etc.
    LOG_PATH = 'frontend/logs'

    # JSON output in UTF8 (mandatory for czech language)
    JSON_AS_ASCII = False

    # database settings:
    # mongo connection settings
    DBNAME = 'grainery'
    PORT = '27017'
    HOST = ''

    # mongodb user credentials
    USERNAME = ''
    PASSWORD = ''

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
