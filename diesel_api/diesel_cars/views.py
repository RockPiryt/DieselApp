#diesel_cars/views.py

from flask import Blueprint, render_template

car = Blueprint('car', __name__)

@car.route('/cars')
def cars():
    return render_template('cars.html', active_menu='cars')
