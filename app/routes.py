from flask import render_template, url_for, redirect, flash
from app import app, db
# from app.models import
# from app.forms import


@app.route('/')
def home():
    return render_template('home.html', page_title='Home')
