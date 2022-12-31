#trip_calculator/views.py

from flask import Blueprint, render_template

trip = Blueprint('trip', __name__)

@trip.route('/calculator')
def calculator():
    return render_template('calculator.html', active_menu='calculator')

@trip.route('/calculator_wtf')
def calculator_wtf():
    return render_template('calculator_wtf.html', active_menu='calculator_wtf')

@trip.route('/trips_history')
def trips_history():
    return render_template('trips_history.html', active_menu='trips_history')