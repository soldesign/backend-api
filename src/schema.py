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
    def __init__(self, name, email, role, credentials):
        self.uuid = uuid.uuid4()
        self.name = name
        self.credentials = credentials
        self.email = email
        self.created_at = dt.datetime.now()
        self.role = role
        self.karanas = []


class Karana(object):
    def __init__(self, name, owner, config, note=''):
        self.uuid = uuid.uuid4()
        self.name = name
        self.config = config
        self.note = note
        self.created_at = dt.datetime.now()
        self.owner = owner


class Credential(object):
    def __init__(self, login, password):
        self.login = login
        self.password = password


class Config(object):
    def __init__(self, series='data', signal=10, post_int=30, get_int=6):
        self.series = series
        self.password = id_generator()
        self.signal = signal
        self.post_int = post_int
        self.get_int = get_int


##################################### Schemas ##################################################


class CredentialsSchema(Schema):
    login = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=5, max=128))


class ConfigSchema(Schema):
    series = fields.Str()
    password = fields.Str()
    signal = fields.Int()
    post_int = fields.Int()
    get_int = fields.Int()


class UserSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    credentials = fields.Nested(CredentialsSchema, many=False)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(required=True)
    # karanas = fields.Nested('KaranaSchema', many=True, exclude=('user', 'note', 'created_at'))
    karanas = fields.List(fields.UUID(), validate=validate.Length(max=1000))

    @post_load
    def make_user(self, data):
        return User(**data)


class UserDbSchema(Schema):
    uuid = fields.UUID(required=True, dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    credentials = fields.Nested(CredentialsSchema, required=True, many=False)
    created_at = fields.DateTime(required=True, dump_only=True)  # should be in unix epoch time
    role = fields.Str(required=True)  # should be a OneOf from a list in config
    karanas = fields.List(fields.UUID(), validate=validate.Length(max=1000),
                          required=True)  # should be a OneOf from a list of karanas


class KaranaSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=128))
    note = fields.Str()
    config = fields.Nested(ConfigSchema, many=False)
    created_at = fields.DateTime(dump_only=True)
    owner = fields.UUID(required=True)  # should be a OneOf from a list of users

    @post_load
    def make_karana(self, data):
        data['config'] = Config(**(data['config']))
        return Karana(**data)


class KaranaDbSchema(Schema):
    uuid = fields.UUID(required=True, dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=128))
    note = fields.Str(required=True)
    config = fields.Nested(ConfigSchema, required=True, many=False)
    created_at = fields.DateTime(required=True, dump_only=True)
    owner = fields.UUID(required=True)  # should be a OneOf from a list of users
