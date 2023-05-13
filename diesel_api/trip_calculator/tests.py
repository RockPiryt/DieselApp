

class Trip():
    
    def __init__(self, user_id, trip_frequency, amount_trip, distance, type_trip, average_usage,):
        self.user_id = user_id
        self.trip_frequency = trip_frequency
        self.amount_trip = amount_trip
        self.distance = distance
        self.type_trip = type_trip
        self.average_usage = average_usage


    def create_test_trip(self):
        print(f"User with id:{self.user_id} add new trip")



class User():
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

usertrip = Trip(user_id=7, trip_frequency="cylical", amount_trip=11, distance=11, type_trip="roads", average_usage=5)
usertrip.create_test_trip()