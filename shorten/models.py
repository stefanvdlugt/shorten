from shorten import db, login
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from time import time as sec_since_epoch
from os import urandom

def keygen():
    '''
    Returns a 16 bytes string.
    The first 6 bytes give a timestamp (# milliseconds since 1 Jan 1970),
    and the last 10 bytes are random.
    '''
    return int(sec_since_epoch()*1000).to_bytes(6,byteorder='big') + urandom(10)

class User(UserMixin, db.Model):
    id = db.Column(db.BINARY(length=16), primary_key=True, default=keygen)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"User {self.username}"

    def get_id(self):
        return self.id.hex()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(bytes.fromhex(id))

class ShortenedURL(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(32), index=True, unique=True)
    dest = db.Column(db.String(2000))
    modification_date = db.Column(db.DateTime())

