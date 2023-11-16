from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)


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

@app.route('/')
def main():
    return render_template('temp.html')