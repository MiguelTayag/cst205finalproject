from flask import Flask, render_template, flash, redirect
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
endpoint = "https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=FeJBzzela4w41klzeTQ0rYP056JXSWJX"
try:
    r = requests.get(endpoint)
    data = r.json()
    pprint(data)
except:
    print('please try again')

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

@app.route('/', methods=('GET', 'POST'))
def main():
    form = Location()
    if form.validate_on_submit():
        # store_location(form.song_title.data, form.song_artist.data)
        return redirect('/view_playlist')
    return render_template('temp.html', form=form)