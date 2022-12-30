from flask_wtf import FlaskForm 
from wtforms import RadioField, IntegerField, DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired

class TripForm(FlaskForm):
    trip_frequency = RadioField('Trip Frequency', choices=['cyclical', 'single'])
    amount_trip = IntegerField('Amount of trip in month', validators=[InputRequired("Enter amount")])
    distance = DecimalField('Trip distance in kilometers', places=2, validators=[InputRequired("Enter amount of distance")])
    type_trip = SelectField('Type of trip', choices=['roads', 'city'])
    average_usage = DecimalField('Average fuel usage per 100km', places=2, validators=[InputRequired("Enter amount of distance")])
    submit = SubmitField('Add trip')
    