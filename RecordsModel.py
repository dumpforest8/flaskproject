from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app
import json
from datetime import date
from UserModel import User

db = SQLAlchemy(app)

class Records(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer,primary_key=True)
    superhero = db.Column(db.String(80),nullable=False)
    power = db.Column(db.String(80),nullable=False)
    creation_date = db.Column(db.String(80),nullable=False)
    user = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return str({
            'superhero': self.superhero,
            'power': self.power,
            'date': self.creation_date,
            'user': self.user
        })

    def get_user_records(_username):
        user = User.query.filter_by(username=_username).first()
        if user is None:
            return False
        else:
            return [Records.json(listing) for listing in Records.query.filter_by(user=_username).all()]

    def add_record(_username, hero, ability):
        user = User.query.filter_by(username=_username).first()
        if user is None:
            return False
        else:
            today = str(date.today())
            new_hero = Records(superhero=hero, power=ability,creation_date=today,user=_username)
            db.session.add(new_hero)
            db.session.commit()
            return True

    def delete_all_rec(username):
        is_successful = Records.query.filter_by(user=username).delete()
        db.session.commit()
        return bool(is_successful)

    def json(self):
        return {'superhero': self.superhero,'power': self.power, 'date': self.creation_date,'user': self.user}






