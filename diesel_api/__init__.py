# diesel_api/__init__.py

from flask import Flask

app = Flask(__name__)

from diesel_api.core.views import core
app.register_blueprint(core)

from diesel_api.trip_calculator.views import trip
app.register_blueprint(trip)

from diesel_api.diesel_cars.views import car
app.register_blueprint(car)

from diesel_api.error_pages.handlers import error_pages
app.register_blueprint(error_pages)