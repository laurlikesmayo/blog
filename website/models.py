from . import db
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import Date
import json

def default_list():
    return []

#puts all the users information into the database
class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(50), nullable = False)

class Post(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    date_added = db.Column(Date, default=datetime.now().date)
    category = (db.Column(db.String(500))) 
    title = db.Column(db.String(100))
    image_path = db.Column(db.String(500))
    video_url=db.Column(db.String(500), default='')
    content = db.Column(db.String(10000))

