import pdb

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import authenticate
from database_setup import Base, User


# Starts the database
engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Retrieves the db session
def getDbSession():
    return session


# Creates a new user record from OAuth sign-ins. Returns the newly created id
def createUser(login_session):
    temp_pw = random_pw()
    hashbrown = make_pw_hash(login_session['username'], temp_pw)
    newUser = User(name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'],
        salt = hashbrown.split('|')[1],
        hashedpw = hashbrown.split  ('|')[0])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get user by id
def getUserById(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get user by email
def getUserByEmail(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except:
        return None

# Get distinct object properties
def getUnique(cls_attr):
    return session.query(cls_attr).distinct(cls_attr).all()

# Get object properties sorted in ascending order
def getAscending(cls_attr, order, limit = 0):
    if limit == 0:
        return session.query(cls_attr).order_by(asc(order)).all()
    else:
        return session.query(cls_attr).order_by(asc(order)).limit(limit).all()

# Get object properties sorted in descending order
def getDescending(cls_attr, order, limit = 0):
    if limit == 0:
        return session.query(cls_attr).order_by(desc(order)).all()
    else:
        return session.query(cls_attr).order_by(desc(order)).limit(limit).all()