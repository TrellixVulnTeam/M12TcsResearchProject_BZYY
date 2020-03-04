import datetime

from flask import current_app
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import db, login_manager
#from app.__init__ import db

# with current_app.app_context():
#     db = SQLAlchemy(current_app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(20), unique=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, uname,password,email,phone = None, confirmed=False,confirmed_on = None ):
        self.uname = uname
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.phone = phone
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def serialize(self):
        return {"id": self.id,
                "uname": self.uname,
                "password": self. password_hash,
                "email" : self.email,
                "phone": self.phone,
                "confirmed": self.confirmed,
                "confirmed_on" : self.confirmed_on}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Manager(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def serialize(self):
        return {"user_id": self.user_id}


class HouseKeeper(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)

    def __init__(self, user_id, module_id = None, course_id =None):
        self.user_id = user_id
        self.module_id = module_id
        self.course_id = course_id

    def serialize(self):
        return {"user_id": self.user_id,
                "module_id": self.module_id,
                "course_id": self.course_id}


class Student(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)

    def __init__(self, user_id, house_id=None, module_id=None,):
        self.user_id = user_id
        self.house_id = house_id
        self.module_id = module_id

    def serialize(self):
        return {"user_id": self.user_id,
                "house_id": self.house_id,
                "module_id": self.module_id}


class House(db.Model):
    house_id = db.Column(db.Integer, primary_key=True)
    house_keeper = db.Column(db.Integer)
    module = db.Column(db.Integer)
    color = db.Column(db.String)

    def __init__(self, house_keeper, module, color):
        self.house_keeper = house_keeper
        self.module = module
        self.color = color

    def serialize(self):
        return {"house_id": self.house_id,
                "house_keeper": self.house_keeper,
                "module": self.module,
                "color": self.color}


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String)
    module = db.Column(db.Integer)

    def __init__(self, name, description, module):
        self.name = name
        self.description = description
        self.module = module

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "module": self.module}


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, unique=True)
    module_id = db.Column(db.Integer)
    content = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, owner_id, module_id, content, status):
        self.owner_id = owner_id
        self.module_id = module_id
        self.content = content
        self.status = status

    def serialize(self):
        return {"id": self.id,
                "owner_id": self.owner_id,
                "module_id": self.module_id,
                "content": self.content,
                "status": self.status}

# database methods


def create_all_table():
    db.create_all()


def get_user_by_name(uname):
    user = User.query.filter_by(uname=uname).first()
    if user is None:
        return None
    else:
        return user.serialize()






def add_a_user(uname, password, email, phone, confirmed, confirmed_on):
    user = User(uname, password, email, phone, confirmed, confirmed_on)
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def add_a_user_by_enity(user):
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def delete_a_user(uname):
    # Maybe try this
    user = User.query.filter_by(uname=uname).first()
    if user is not None:
        print(user.serialize())
        db.session.delete(user)
        db.session.commit()

    # User.query.filter_by(uname=uname).delete()
    # db.session.commit()


def confirm_a_user_by_email(email):
    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed = True
    user.confirmed_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    return user.serialize()
