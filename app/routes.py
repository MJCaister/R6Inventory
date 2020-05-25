from flask import render_template, url_for, redirect, flash
from app import app, db
from models import Item
# from app.forms import

# charm = Item.query.filter(Item.type.in_([2])).all()
# headgear = Item.query.filter(Item.type.in_([3])).all()
# uniform = Item.query.filter(Item.type.in_([4])).all()
# operator = Item.query.filter(Item.type.in_([5])).all()
# org = Item.query.filter(Item.type.in_([6])).all()
# skin = Item.query.filter(Item.type.in_([7])).all()
# weapon = Item.query.filter(Item.type.in_([8])).all()


@app.route('/')
def home():
    return render_template('home.html', page_title='Home', item=item)
