#trip_calculator/views.py

from flask import Blueprint, render_template, redirect,  url_for, flash, request, abort
from flask_login import current_user, login_required
from diesel_api.trip_calculator.forms import TripForm
from diesel_api.models import Trip
from diesel_api import db

trip = Blueprint('trip', __name__)

#CRUD
#create trip
@trip.route('/create_trip', methods=['GET','POST'])
@login_required
def create_trip():

    form = TripForm()

    if form.validate_on_submit():
        usertrip = Trip(user_id =current_user.id,
                    trip_frequency=form.trip_frequency.data,
                    amount_trip=form.amount_trip.data,
                    distance=form.distance.data,
                    type_trip=form.type_trip.data,
                    average_usage=form.average_usage.data)

        db.session.add(usertrip)
        db.session.commit()
        flash('You add new trip!')
        return redirect(url_for('trip.view_trip', usertrip_id=usertrip.id))
    return render_template('create_trip.html',active_menu='create_trip', form=form)


diesel=7.7

@trip.route('/calc_trip/<int:usertrip_id>', methods=['GET','POST'])
@login_required
def calc_trip(usertrip_id):
    usertrip = Trip.query.get_or_404(usertrip_id)
    km_month= usertrip.distance*usertrip.amount_trip
    av_usage=usertrip.average_usage*(km_month/100)
    cost=diesel*av_usage
    # print(f'you drive  {km_month} km per month')
    # print(f'you used {av_usage} L diesel')
    # print(f'you spend {cost} zl on diesel fuel')
    return render_template('calc_trip.html', km_month=km_month, av_usage=av_usage, cost=cost, usertrip=usertrip)

#tripinfo1= Trip(distance=30, amount_trip=20, usage=7)

#print(calc_trip(usertrip_id=usertrip.id))

#read trip
@trip.route('/view_trip/<int:usertrip_id>')
def view_trip(usertrip_id):
    usertrip = Trip.query.get_or_404(usertrip_id)
    return render_template('view_usertrips.html', date=usertrip.date, usertrip=usertrip)


#update trip
@trip.route('/update_trip/<int:usertrip_id>', methods=['GET','POST'])
@login_required
def update_trip(usertrip_id):

    usertrip = Trip.query.get_or_404(usertrip_id)

    if usertrip.author != current_user:
        abort(403)

    form = TripForm()

    if form.validate_on_submit():

        usertrip.trip_frequency = form.trip_frequency.data
        usertrip.amount_trip = form.amount_trip.data
        usertrip.distance = form.distance.data
        usertrip.type_trip = form.type_trip.data
        usertrip.average_usage = form.average_usage.data

        db.session.commit()
        flash(f'You update trip!{usertrip_id}')
        return redirect(url_for('trip.view_trip', usertrip_id=usertrip.id))
    elif request.method =='GET':
        form.trip_frequency.data = usertrip.trip_frequency
        form.amount_trip.data = usertrip.trip_frequency
        form.distance.data = usertrip.distance
        form.type_trip.data = usertrip.type_trip
        form.average_usage.data = usertrip.average_usage

    return render_template('create_trip.html',active_menu='create_trip', form=form, title='updating')

#delete trip
@trip.route('/delete_trip/<int:usertrip_id>', methods=['GET','POST'])
@login_required
def delete_trip(usertrip_id):
    usertrip = Trip.query.get_or_404(usertrip_id)

    if usertrip.author != current_user:
        abort(403)

    db.session.delete(usertrip)
    db.session.commit()

    flash(f'You delete trip!{usertrip_id}')
    return redirect(url_for('trip.view_trip'))


@trip.route('/trip_list')
def trip_list():
    page = request.args.get('page',1,type=int)
    usertrip_list = Trip.query.order_by(Trip.date.desc()).paginate(page=page, per_page=5)
    return render_template('trip_list.html', active_menu='trip_list', usertrip_list=usertrip_list)


# @trip.route('/calculator', methods=['GET','POST'])
# def calculator():
#     if request.method == 'GET':
#         return render_template("calculator.html")
#     else:
#         flash('Debug:starting exchange in POST mode')
        
#         #trzeba dodać usera żeby wyfiltrować jego trips
#         ##ADD INFO FROM DATABASE####
#         # trip_frequency = Trip.query.first# trzeba dodać z bazy danych info
#         # amount_trip=
#         # distance=
#         # type_trip=
#         # average_usage=

#         def calc_km(amount_trip,distance):
#             return amount_trip * distance

#         def calc_consumpcy(km_month, average_usage):
#             return (km_month/100) * average_usage

#         def calc_total(fuel_consumpcy, diesel_price):
#             return fuel_consumpcy* diesel_price

#         km_month = float(calc_km(amount_trip,distance))
#         fuel_consumpcy = float(calc_consumpcy(km_month, average_usage))
#         diesel_price = 7.7
#         total_cost = float(calc_total(fuel_consumpcy, diesel_price))



#         cost_trip = CostTrip(trip_frequency=trip_frequency,
#                             amount_trip=amount_trip, 
#                             distance=distance, 
#                             type_trip=type_trip, 
#                             average_usage=average_usage, 
#                             km_month=km_month, 
#                             fuel_consumpcy=fuel_consumpcy, 
#                             total_cost=total_cost)

#         db.session.add(cost_trip)
#         db.session.commit()
#         flash('Your trip informations were calculated! ')

#     return render_template("cost_trip.html", 
#                                 trip_frequency=trip_frequency,
#                                 amount_trip=amount_trip, 
#                                 distance=distance, 
#                                 type_trip=type_trip, 
#                                 average_usage=average_usage, 
#                                 km_month=km_month, 
#                                 fuel_consumpcy=fuel_consumpcy, 
#                                 total_cost=total_cost)


