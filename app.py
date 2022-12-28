from flask import Flask, render_template, request ,flash, g
import sqlite3

app_info = {'db_file': 'C:/Users/Popuś/Desktop/Python/flask/DIESEL ON/data/trip.db'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'makaronGwaizdka2022'

def get_db(): # funkcja do uzyskania połączenia do bazy danych
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])# połączenie do bazy danych określonej w app_info
        conn.row_factory = sqlite3.Row #będziemy dostawać słowniki nie duplety
        g.sqlite_db = conn #zapisanie połaczenia w zmiennej g
    return g.sqlite_db

@app.teardown_appcontext #w przypadku zamknięcia przez klienta okna zamknięcie połączenia z baza danych
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/diagram")
def diagram():
    return render_template("diagram.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    if request.method == 'GET':
        return render_template("calculator.html")
    else:
        flash('Debug:starting exchange in POST mode')

        trip_frequency = 'cyclical'
        if 'user_trip_frequency' in request.form:
            trip_frequency = request.form['user_trip_frequency']

        amount_trip = '1'
        if 'user_amount_trip' in request.form:
            amount_trip = int(request.form['user_amount_trip'])

        distance = '6'
        if 'user_distance' in request.form:
            distance = float(request.form['user_distance'])

        type_trip = 'city'
        if 'user_type_trip' in request.form:
            type_trip = request.form['user_type_trip']

        average_usage='8'
        if 'user_average_usage' in request.form:
            average_usage = float(request.form['user_average_usage'])

        km_month = float(calc_km(amount_trip,distance))
        fuel_consumpcy = float(calc_consumpcy(km_month, average_usage))
        diesel_price = 7.7
        total_cost = float(calc_total(fuel_consumpcy, diesel_price))

        db = get_db() # połączenie do bazy danych
        sql_command = 'insert into usertrips (trip_frequency, amount_trip, distance, km_month, type_trip, average_usage, fuel_consumpcy, diesel_price, total_cost) values (?,?,?,?,?,?,?,?,?)'
        db.execute(sql_command, [trip_frequency, amount_trip, distance, km_month, type_trip, average_usage, fuel_consumpcy, diesel_price, total_cost])
        db.commit()
        flash('Your trip informations to calculate were saved to our database trip.db. ')

    return render_template("calculator.html", amount_trip=amount_trip, trip_frequency=trip_frequency, distance=distance, type_trip=type_trip, average_usage=average_usage, km_month=km_month, fuel_consumpcy=fuel_consumpcy, total_cost=total_cost)

# km_month=km_month, fuel_consumpcy=fuel_consumpcy, total_cost=total_cost
def calc_km(amount_trip,distance):
    return amount_trip * distance

def calc_consumpcy(km_month, average_usage):
    return (km_month/100) * average_usage

def calc_total(fuel_consumpcy, diesel_price):
    return fuel_consumpcy* diesel_price

@app.route("/cars")
def cars():
    return render_template("cars.html")


if __name__== '__main__':
    app.run()