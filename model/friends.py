""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class Friend(db.Model):
    __tablename__ = 'friends'  # table name is plural, class name is singular

    # Define the Friend schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _uidfriend = db.Column(db.String(255), unique=False, nullable=False)   

    # constructor of a uid object, initializes the instance variables within object (self)
    def __init__(self, uid, uidfriend):
        self._uid = uid    # variables with self prefix become part of the object, 
        self._uidfriend = uidfriend

    # a name getter method, extracts name from object
    @property
    def uidfriend(self):
        return self._uidfriend
    
    # a setter function, allows name to be updated after initial object creation
    @uidfriend.setter
    def uidfriend(self, uidfriend):
        self._uidfriend = uidfriend
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a friend object from Friend(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "uidfriend": self.uidfriend,
            "uid": self.uid
        }

    # CRUD update: updates name, uid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "uidfriend":
                self.name = dictionary[key]
            if key == "uid":
                self.uid = dictionary[key]
        db.session.commit()
        return self

    # CRUD delete: remove self
    # return self
    def delete(self):
        friend = self
        db.session.delete(self)
        db.session.commit()
        return friend


"""Database Creation and Testing """


# Builds working data for testing
def initFriends():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        friends = [
            Friend(uid='sjohua2', uidfriend='josh3'),
            Friend(uid='sjosh3', uidfriend='johnM')
        ]

        """Builds sample user/note(s) data"""
        for friend in friends:
            try:
                friend.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {friend.uid}")