#core/views.py

from flask import Blueprint, render_template

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html', active_menu='index')

@core.route('/diagram')
def diagram():
    return render_template('diagram.html', active_menu='diagram')