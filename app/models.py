# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
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
    orgs = db.relationship(
        'Item',
        secondary='operator_org',
        primaryjoin='Item.id == operator_org.c.operator_id',
        secondaryjoin='Item.id == operator_org.c.org_id',
        backref='items'
    )
    users = db.relationship('User', secondary='user_item', backref='items')


class ItemType(db.Model):
    __tablename__ = 'item_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(16), nullable=False)


t_operator_org = db.Table(
    'operator_org',
    db.Column('operator_id', db.ForeignKey('item.id')),
    db.Column('org_id', db.ForeignKey('item.id'))
)


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
