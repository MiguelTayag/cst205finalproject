from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import requests, json
from pprint import pprint



# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

my_data = {}
endpoint = 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=vLbGMAWNX6B0a0sRd9Wg16E6HgbNtEJ7'
# "https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=FeJBzzela4w41klzeTQ0rYP056JXSWJX"
try:
    r = requests.get(endpoint)
    data = r.json()
    #pprint(data)
except:
    print('please try again')

# url = "https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey=XXX"
# headers = {"accept": "application/json"}
# response = requests.get(url, headers=headers)

# print(response.text)

class Location(FlaskForm):
    city = StringField(
        'City', 
        validators=[DataRequired()]
    )
    state = StringField(
        'State', 
        validators=[DataRequired()]
    )
    zip = StringField(
        'Zip Code', 
        validators=[DataRequired()]
    )


@app.route('/', methods=('GET', 'POST'))
def main():
    form = Location()
    if form.validate_on_submit():
        # store_location(form.song_title.data, form.song_artist.data)
        return redirect('/weather')
    return render_template('temp.html', form=form)

@app.route('/weather')
def display():
    return render_template('weathertemp.html')
#Want to get fire, lightning, precipitation, wind speed info
