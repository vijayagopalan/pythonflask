from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.String(32),primary_key=True,unique=True,default=get_uuid())
    email = db.Column(db.String(500),unique=True)
    password = db.Column(db.Text,nullable=False)
    password_hash = db.Column(db.Text,nullable=False)