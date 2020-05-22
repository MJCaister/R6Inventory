# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Charm(db.Model):
    __tablename__ = 'charm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(64))



class Headgear(db.Model):
    __tablename__ = 'headgear'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(32))



class Operator(db.Model):
    __tablename__ = 'operator'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    org_id = db.Column(db.ForeignKey('organisation.id'))

    org = db.relationship('Organisation', primaryjoin='Operator.org_id == Organisation.id', backref='operators')
    weaps = db.relationship('Weapon', secondary='operator_weapon', backref='operators')



t_operator_weapon = db.Table(
    'operator_weapon',
    db.Column('op_id', db.ForeignKey('operator.id')),
    db.Column('weap_id', db.ForeignKey('weapon.id'))
)



class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))



class Skin(db.Model):
    __tablename__ = 'skin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(32), nullable=False)



t_sqlite_sequence = db.Table(
    'sqlite_sequence',
    db.Column('name', db.NullType),
    db.Column('seq', db.NullType)
)



class Uniform(db.Model):
    __tablename__ = 'uniform'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(32), nullable=False)



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(32), nullable=False)
    password = db.Column(db.Text(256), nullable=False)
    image = db.Column(db.String)



class Weapon(db.Model):
    __tablename__ = 'weapon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(16))
