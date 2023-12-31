# CST205 - Multimedia
# Forecast Finder
# Authors: Miguel Tayag, Ryan Hopper, Kenia Munoz-Ordaz, Oliva Avalos 

# Sources:
#   Getting Previous Date: https://www.geeksforgeeks.org/get-yesterdays-date-using-python/#

from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from datetime import datetime
from datetime import date
from datetime import timedelta
import requests, json
from pprint import pprint
from image_info import image_info
import os

# ------------------------------------------ Miguel Tayag -------------------------------------------------------------
# includes:
    # result.html
    # temp.html
    # typeChoice.html

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

# Getting Previous Date (See Source Above)
global prevDate
today = date.today()
delta = timedelta(days = 1)
prevDate = today - delta
prevDate = prevDate.strftime("%Y-%m-%d")
print(f'prevDate: {prevDate}')

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


@app.route('/type-searcher', methods=('GET', 'POST'))
def typeSearcher():
    form = TypeForm()
    if request.method == "POST":
        print('Validated')
        # global so can be accessed anywhere
        global typeChosen
        typeChosen = form.forecastType.data
        print(f'type chosen: {typeChosen}')
        return redirect('/weatherSearcher')
    return render_template('typeChoice.html', form=form)

@app.route('/weatherSearcher', methods=('GET', 'POST'))
def main():
    form = WeatherForm()
    print(typeChosen)
    # if Real Time or History is picked, don't need to ask for the date
    if(typeChosen == 'Real Time' or typeChosen == 'History'):
        visibility = 'hidden'
    else:
        visibility = 'visible'
    if form.validate_on_submit():
        print('Validated')
        print(f'Location: {form.location.data}')
        global location
        global dateChosen
        dateChosen = form.date.data
        location = form.location.data
        return redirect('/weatherResults')
    return render_template('temp.html', form=form, visibility = visibility)

@app.route('/weatherResults')
def results():
    weatherCodeMinImg = ""
    weatherCodeMaxImg = ""
    weatherCodeImg = ""
    # pick api string depending on typeChosen ('Real Time', 'Forecast', 'History')
    apiString = endpoints[typeChosen] + location + '&apikey=' + apiKey
    global apiData
    apiData = readAPI(apiString)
    if(typeChosen == 'Real Time'):
        apiData = apiData['data']['values']

        # pick image based off weatherCode
        weatherCodeImg = real_time_wc(apiData)
        print(f"passing in {weatherCodeImg}")
        return render_template ('result.html', apiData = apiData,location=location,dateChosen=dateChosen,
        image_info=image_info,typeChosen=typeChosen,weatherCodeImg=weatherCodeImg)
    elif(typeChosen == 'History'):
        apiData = apiData['timelines']['daily'] 
        for data in apiData:
            if(prevDate in data['time']):
                apiData = data['values']
        weatherCodeMinImg = min_wc(apiData)
        weatherCodeMaxImg = max_wc(apiData)
        return render_template ('result.html', apiData = apiData, location = location, dateChosen = prevDate,
         image_info=image_info, typeChosen=typeChosen,weatherCodeMaxImg=weatherCodeMaxImg, weatherCodeMinImg=weatherCodeMinImg)
    else:
        print(f"date: {dateChosen.strftime('%Y-%m-%d')}")
        apiData = apiData['timelines']['daily'] 
        for data in apiData:
            if((dateChosen.strftime("%Y-%m-%d")) in data['time']):
                apiData = data['values']
        weatherCodeMinImg = min_wc(apiData)
        weatherCodeMaxImg = max_wc(apiData)
        return render_template ('result.html', apiData = apiData, location = location, dateChosen = dateChosen,
        image_info=image_info, typeChosen=typeChosen,weatherCodeMaxImg=weatherCodeMaxImg, weatherCodeMinImg=weatherCodeMinImg)

# pick image based off weatherCode
def real_time_wc(apiData):
    weatherCode = ""
    weatherCodeImg = ""
    weatherCode = str(apiData['weatherCode'])
    for item in image_info:
        print(f'item: {item} = weatherCode: {weatherCode}.....Results = {weatherCode in item}')
        if (weatherCode in item[:4]):
            weatherCodeImg = item
            break
    print(f'code: {weatherCodeImg}')
    return weatherCodeImg

# pick image based off weatherCodeMin (For Forecast and History only)
def min_wc(apiData):
    weatherCodeMin = ""
    weatherCodeMinImg = ""
    weatherCodeMin = str(apiData['weatherCodeMin'])
    for item in image_info:
        if (weatherCodeMin in item[:4]):
            weatherCodeMinImg = item
            break
    print(f'code: {weatherCodeMinImg}')
    return weatherCodeMinImg

# pick image based off weatherCodeMax (For Forecast and History only)
def max_wc(apiData):
    weatherCodeMax = ""
    weatherCodeMaxImg = ""
    weatherCodeMax = str(apiData['weatherCodeMax'])
    for item in image_info:
        if (weatherCodeMax in item[:4]):
            weatherCodeMaxImg = item
            break
    print(f'code: {weatherCodeMaxImg}')
    return weatherCodeMaxImg
# ----------------------------------------------------- END OF SECTION (Miguel) -------------------------------------------------------------

# ---------------------------------------------------- Ryan Hopper & Oliva Avalos -------------------------------------------------------------
# includes:
    # about.html
@app.route('/about')
def about():
    return render_template('about.html')
# ----------------------------------------------------- END OF SECTION (Ryan & Oliva) -------------------------------------------------------------

#---------------------------------------------------------- Kenia Munoz-Ordaz -------------------------------------------------------------
# includes:
    # home.html
    # styles.css
    # styling for all of the other routes..
@app.route('/')
def home():
    return render_template('home.html')

 #------------------------------------------ END OF SECTION (Kenia) -------------------------------------------------------------    