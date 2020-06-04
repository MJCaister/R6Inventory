# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(32), nullable=False)
    type = db.Column(db.ForeignKey('item_type.id'))
    small_image = db.Column(db.Text(64))
    large_image = db.Column(db.Text(64))

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
    

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(32), nullable=False)
    password = db.Column(db.Text(256), nullable=False)
    image = db.Column(db.Text(64))


t_user_item = db.Table(
    'user_item',
    db.Column('user_id', db.ForeignKey('user.id')),
    db.Column('item_id', db.ForeignKey('item.id'))
)
