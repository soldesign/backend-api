'''This file contains the short Version of the two main schemas User and Karanas'''
import datetime as dt
import uuid
import random
import string
from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load
from marshmallow import validate


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


##################################### MODELS ####################################################


class User(object):
    def __init__(self, name, email, role):
        self.uuid = uuid.uuid4()
        self.name = name
        self.credentials = {"password": id_generator()}
        self.email = email
        self.created_at = dt.datetime.now()
        self.role = role
        self.karanas = []


class Karana(object):
    def __init__(self, name,  owner, note=''):
        self.uuid = uuid.uuid4()
        self.name = name
        self.credentials = {"password": id_generator()}
        self.note = note
        self.created_at = dt.datetime.now()
        self.owner = owner

##################################### Schemas ##################################################


class UserSchema(Schema):
    uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    credentials = fields.Dict()
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(required=True)
    #karanas = fields.Nested('KaranaSchema', many=True, exclude=('user', 'note', 'created_at'))
    karanas = fields.List(fields.UUID(), validate=validate.Length(max=1000))

    @post_load
    def make_user(self, data):
        return User(**data)


class UserDbSchema(Schema):
    uuid = fields.UUID(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True) # should be in unix epoch time
    role = fields.Str(required=True) # should be a OneOf from a list in config
    karanas = fields.List(fields.UUID(), validate=validate.Length(max=1000), required=True) # should be a OneOf from a list of karanas


class KaranaSchema(Schema):
    uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    note = fields.Str()
    credentials = fields.Dict()
    created_at = fields.DateTime(dump_only=True)
    #user = fields.Nested('UserSchema', only=["uuid", "email"], required=True)
    owner = fields.UUID(required=True) # should be a OneOf from a list of users

    @post_load
    def make_karana(self, data):
        return Karana(**data)


class KaranaDbSchema(Schema):
    uuid = fields.UUID(required=True)
    name = fields.Str(required=True)
    note = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    owner = fields.UUID(required=True) # should be a OneOf from a list of users
