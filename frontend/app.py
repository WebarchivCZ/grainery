from os import path, mkdir
from flask import Flask, send_from_directory
from logging import FileHandler, WARNING
from functions import niceDate, niceSize
from config.config import Config, mongo
from views.browse import bmod
from views.search import smod
from views.dashboard import dmod

# create object with configuration
configuration = Config()

# Create app
app = Flask(__name__)

# logging errors into file (only if debug mode is off)
# pokud neexistuje adresář /logs, tak se pokusí ho vytvořit
# pokud se nepovede ani vytvoření adresáře, tak se logování nezapne
if not configuration.DEBUG:
    try:
        file_handler = FileHandler('logs/errorlog.txt')
    except FileNotFoundError:
        try:
            mkdir('logs')
        except Exception:
            print("Missing directory /logs and creation failed."
                  " For more information see"
                  "https://github.com/WebarchivCZ/grainery/wiki/")
    else:
        file_handler.setLevel(WARNING)
        app.logger.addHandler(file_handler)

# pass flask configuration object
app.config.from_object(configuration)

# initialize mongodb object for queries
mongo.init_app(app)

# jinja functions from functions.py
app.jinja_env.filters['nicedate'] = niceDate
app.jinja_env.filters['nicesize'] = niceSize

# blueprints register
app.register_blueprint(bmod)
app.register_blueprint(smod)
app.register_blueprint(dmod)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon'
                               )


if __name__ == '__main__':
    app.run()
