from os import path
from flask import Flask, render_template, send_from_directory
import config.config as cfg
from views.harvests import mod

# create objekt with configuration DevelopmentConfig x
# Configuration = cfg.ProductionConfig
Configuration = cfg.DevelopmentConfig

# Create app
app = Flask(__name__)

# pass flask configuration object
app.config.from_object(Configuration)

# initialize mongodb object for queries
cfg.mongo.init_app(app)

# blueprints register
app.register_blueprint(mod)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon'
                               )


if __name__ == '__main__':
    app.run()
