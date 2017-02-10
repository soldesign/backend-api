'''This file contains the short Version of the two main schemas User and Karanas'''
import datetime as dt
import uuid
from marshmallow import Schema, fields, post_load


##################################### MODELS ####################################################


class User(object):
    def __init__(self, name, email, role):
        self.uuid = uuid.uuid4()
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.role = role
        self.karanas = []


class Karana(object):
    def __init__(self, name, note, user):
        self.uuid = uuid.uuid4()
        self.name = name
        self.note = note
        self.created_at = dt.datetime.now()
        self.user = user

##################################### Schemas ##################################################


class UserSchema(Schema):
    uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(required=True)
    karanas = fields.Nested('KaranaSchema', many=True, exclude=('user', 'note', 'created_at'))

    @post_load
    def make_user(self, data):
        return User(**data)


class KaranaSchema(Schema):
    uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    note = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema', only=["uuid", "email"], required=True)

    @post_load
    def make_karana(self, data):
        return Karana(**data)
