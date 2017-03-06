import schema
from faker import Faker

fake = Faker()
import random
import string
import json


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_admin_user():
    admin = {
        'name': 'admin',
        'email': 'admin@example.com',
        'role': 'admin',
        'credentials': {
            'login': 'admin@example.com',
            'password': 'admin'
        }
    }
    return json.dumps(admin)


def create_fake_user():
    email = fake.email()
    user = {
        'name': fake.name(),
        'email': email,
        'credentials': {
            'login': email,
            'password': id_generator()
        }
    }
    return json.dumps(user)

