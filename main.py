from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from datetime import datetime
import requests, json
from pprint import pprint




# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

global apiKey
apiKey = "FeJBzzela4w41klzeTQ0rYP056JXSWJX"
# Different API links for different type of Time forecasts
endpoints = {'Real Time' : "https://api.tomorrow.io/v4/weather/realtime?location=",
            'Forecast' : "https://api.tomorrow.io/v4/weather/forecast?location=",
            'History' : "https://api.tomorrow.io/v4/weather/history/recent?location="
            }

# Read API Link
def readAPI(str):
    try:
        r = requests.get(str)
        data = r.json()
        print("Success!")
        return data
    except:
        print('please try again')
        return

class TypeForm(FlaskForm):
    forecastType = SelectField(
        'Type',
        choices = [('Real Time', 'Real Time'), ('Forecast', 'Forecast'), ('History', 'History')],
        validators=[DataRequired()]
    )

class WeatherForm(FlaskForm):
    location = StringField(
        'Location', 
        validators=[DataRequired()]
    )
    date = DateField(
        'Date',
        format='%Y-%m-%d',
        default=datetime.now(),
        validators=[DataRequired()]
    )


@app.route('/', methods=('GET', 'POST'))
def typeSearcher():
    form = TypeForm()
    if request.method == "POST":
        print('Validated')
        global typeChosen
        typeChosen = form.forecastType.data
        print(f'type chosen: {typeChosen}')
        return redirect('/weatherSearcher')
    return render_template('typeChoice.html', form=form)

@app.route('/weatherSearcher', methods=('GET', 'POST'))
def main():
    form = WeatherForm()
    print(typeChosen)
    if(typeChosen == 'Real Time'):
        visibility = 'hidden'
    else:
        visibility = 'visible'
    if form.validate_on_submit():
        print('Validated')
        print(f'Location: {form.location.data}')
        global location
        location = form.location.data
        return redirect('/weatherResults')
    return render_template('temp.html', form=form, visibility = visibility)

@app.route('/weatherResults')
def results():
    if(typeChosen == 'Real Time'):
        apiString = endpoints[typeChosen] + location + '&apikey=' + apiKey
        global apiData
        apiData = readAPI(apiString)
    else:
        visibility = 'visible'
    return render_template ('result.html', apiData = apiData)


    # class Playlist(FlaskForm):
#     song_title = StringField(
#         'Song Title', 
#         validators=[DataRequired()]
#     )


# route decorator binds a function to a URL
# @app.route('/', methods=('GET', 'POST'))
# def hello():
#     form = Playlist()
#     if form.validate_on_submit():
#         return redirect('/view_playlist')
#     return render_template('index.html', form=form)