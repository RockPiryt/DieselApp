#core/views.py
###################IMPORTS#################################
import datetime as dt
import requests


##################BLUEPRINT################################
from flask import Blueprint, render_template

core = Blueprint('core', __name__)


#################ROUTES#####################################

#HOME PAGE - SLIDER
@core.route('/')
def index():
    return render_template('index.html', active_menu='index')

#DIAGRAM PAGE
@core.route('/diagram')
def diagram():
    #Current date
    now_date = dt.datetime.now().date()
    #NPB API request
    response = requests.get(url="http://api.nbp.pl/api/exchangerates/rates/a/usd/")
    data = response.json()
    #print(data)

    mid_rate = data["rates"][0]["mid"]
    dollar_code = data["code"]
    #print(mid_rate)
    return render_template('diagram.html', active_menu='diagram', now_date=now_date, mid_rate=mid_rate, dollar_code=dollar_code)
