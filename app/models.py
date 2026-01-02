from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(100))
    email=db.Column(db.String(100)) 
    role=db.Column(db.String(20))

class Securitylog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    event_type=db.Column(db.String(100))
    user_id=db.Column(db.Integer)
    ip_address=db.Column(db.String(50))
    timestamp=db.Column(db.DateTime, default=datetime)
