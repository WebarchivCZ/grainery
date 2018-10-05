from os import path
from flask import Flask, send_from_directory
import config.config as cfg
from views.harvests import hmod
from views.search import smod
from views.dashboard import dmod

# create object with configuration
# Configuration = cfg.ProductionConfig
Configuration = cfg.DevelopmentConfig

# Create app
app = Flask(__name__)

# pass flask configuration object
app.config.from_object(Configuration)

# initialize mongodb object for queries
cfg.mongo.init_app(app)

# blueprints register
app.register_blueprint(hmod)
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
