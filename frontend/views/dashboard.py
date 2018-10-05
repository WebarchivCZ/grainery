from flask import Blueprint, render_template

dmod = Blueprint('dashboard', __name__)


@dmod.route('/')
def index():
    return render_template('index.html')
