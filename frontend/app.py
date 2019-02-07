from os import path
from flask import Flask, send_from_directory
from logging import FileHandler, WARNING
from config.config import Config, mongo
from functions import niceDate, niceSize
from views.browse import bmod
from views.search import smod
from views.dashboard import dmod

# create object with configuration
configuration = Config()

# Create app
app = Flask(__name__)

# logging errors into file
if not configuration.DEBUG:
    file_handler = FileHandler('logs/errorlog.txt')
    file_handler.setLevel(WARNING)

    app.logger.addHandler(file_handler)

# pass flask configuration object
app.config.from_object(configuration)

# initialize mongodb object for queries
mongo.init_app(app)

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
