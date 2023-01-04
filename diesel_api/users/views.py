#users/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from diesel_api import db
from diesel_api.models import User, Trip
from diesel_api.users.forms import RegistrationForm,LoginForm, UpdateUserForm
from diesel_api.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

#register
@users.route('/register', methods = ['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user=User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


#login
@users.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()#sprawdzenie czy taki email jest w bd(jest zarejestrowany)

        if user.check_password(form.password.data) and user is not None: #za pomocą funkcji check_password, sprawdzam czy przesłane password jest ok

            login_user(user)
            flash('Log in success!')

            #w przypadku zalogowania, przechowywanie danych aby móc robić coś na innych stronach będąc zalogowanym, bez potrzeby ponownego zalogowania
            next =request.args.get('next')
            #albo wracają do hompage albo po zalogowaniu przejdą do strony która wymaga zalogowania
            if next == None or not next[0] == '/': #jeśeli nie next jest none to przekieruje do stroy logowania, jeżeli next nie był homepage to zostanie przekierowany na homepage
                next =url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)


#logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))



#account (update Userform)

@users.route('/account',methods = ['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        #aktualizacja zdjęcia usera
        if form.picture.data:# jeżeli coś jest w przesłanym picture
            username = current_user.username #przechwycenie nazwy usera
            pic=add_profile_pic(form.picture.data, username)# przesłąnie do funkcji add pic potrzebnych danyc - zdjecia oraz nazwy usera z formularza
            current_user.profile_image = pic
        
        #aktualizacja email i username zgodnie z formularzem update
        current_user.username =form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash('User account was updated!')
        return redirect(url_for('users.account'))
    elif request.method=="GET":
        #jeżeli nic nie przesyłamy to przechywtujemy obecne dane
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename = 'profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)



# user's list of Trips
@users.route("/<username>")
def user_trips(username):
    page =request.args.get('page', 1, type=int)
    user =User.query.filter_by(username=username).first_or_404() # wybranie unikalnego użytkownika
    trips_collection =Trip.query.filter_by(author=user).order_by(Trip.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_trips_collection.html', trips_collection=trips_collection, user=user)
