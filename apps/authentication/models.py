# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

from datetime import datetime, timedelta

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Posts(db.Model):

    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    type = db.Column(db.String(64)) # look at type on hacdias.com: food, note, micro, article, checin, drink, photo, itinerary, like
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    images = db.relationship('Images', backref='post', lazy='dynamic')
    tags = db.relationship('Tags', backref='post', lazy='dynamic')


    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Images(db.Model):

    __tablename__ = 'Images'

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64))
    image_path = db.Column(db.String(140))
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))

    def __init__(self, image_name, image_path, post_id):
        self.image_name = image_name
        self.image_path = image_path
        self.post_id = post_id

    def __repr__(self):
        return '<Image {}>'.format(self.image_name)


class Tags(db.Model):

    __tablename__ = 'Tags'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))

    def __init__(self, tag, post_id):
        self.tag = tag
        self.post_id = post_id

    def __repr__(self):
        return '<Tag {}>'.format(self.tag)



@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
