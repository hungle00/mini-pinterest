from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


class Pin(db.Model):
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), db.ForeignKey('users.nickname'))
    text = db.Column(db.String(140))
    image = db.Column(db.String(140))