from app import db

weaps = db.Table('operator_weapon',
                 db.Column('operator_id', db.Integer, db.ForeignKey('operator.id')),
                 db.Column('weapon_id', db.Integer, db.ForeignKey('weapon.id'))
                 )


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    operators = db.relationship('Operator', backref='org')


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    weapons = db.relationship('Weapon', secondary=weaps, backref=db.backref('operators', lazy='dynamic'))


class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
