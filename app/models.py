# coding: utf-8
from hashlib import md5

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import login

db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(32), nullable=False)
    type = db.Column(db.ForeignKey('item_type.id'))
    small_image = db.Column(db.Text(64))
    large_image = db.Column(db.Text(64))
    gained = db.Column(db.Text(64))

    item_type = db.relationship('ItemType', primaryjoin='Item.type == ItemType.id', backref='items')
    users = db.relationship('User', secondary='user_item', backref='items')


class ItemType(db.Model):
    __tablename__ = 'item_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(16), nullable=False)


class OperatorOrg(db.Model):
    __tablename__ = 'operator_org'

    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.ForeignKey('Item.id'))
    org_id = db.Column(db.ForeignKey('Item.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(32), nullable=False)
    password = db.Column(db.Text(256), nullable=False)
    email = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s{}'.format(digest, size)


t_user_item = db.Table(
    'user_item',
    db.Column('user_id', db.ForeignKey('user.id')),
    db.Column('item_id', db.ForeignKey('item.id'))
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
