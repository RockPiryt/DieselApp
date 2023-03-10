#models.py

from diesel_api import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    trips=db.relationship('Trip', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f" Username {self.username}"

class Trip(db.Model):
    
    #users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #user.id tabela users z paramatrem id
    
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trip_frequency = db.Column(db.String(12), nullable=False)
    amount_trip = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    type_trip = db.Column(db.String(12), nullable=False)
    average_usage = db.Column(db.Float, nullable=False)

    def __init__(self, trip_frequency, amount_trip, distance, type_trip, average_usage, user_id):
        self.trip_frequency = trip_frequency
        self.amount_trip = amount_trip
        self.distance = distance
        self.type_trip = type_trip
        self.average_usage = average_usage
        self.user_id = user_id

    def __repr__(self):
        return f" Trip ID: {self.id} Date: {self.amount_trip}"

# diesel=7.7
	
# def calc_km(trip):
#     km_month= trip.distance*trip.amount_trip
#     av_usage=trip.usage*(km_month/100)
#     cost=diesel*av_usage
#     print(f'you drive  {km_month} km per month')
#     print(f'you used {av_usage} L diesel')
#     print(f'you spend {cost} zl on diesel fuel')
#     return cost

# tripinfo1= Trip(distance=30, amount_trip=20, usage=7)

# print(calc_km(trip=tripinfo1))



class Car():
    pass
























# class CalcTrip:
#     def __init__(self, trip_frequency, amount_trip, distance, type_trip, average_usage, km_month, fuel_consumpcy, diesel_price, total_cost):
#         self.trip_frequency = trip_frequency
#         self.amount_trip = amount_trip
#         self.distance = distance
#         self.type_trip = type_trip
#         self.average_usage = average_usage
#         self.km_month = km_month
#         self.fuel_consumpcy = fuel_consumpcy
#         self.diesel_price = diesel_price
#         self.total_cost = total_cost