"""This file contains 2 users and three karanas for testing purposes"""
import schema

user1 = '{"name": "Micha", "email": "Micha@python.com", "role": "admin"}'
user2 = '{"name": "Daniel", "email": "Daniel@python.com", "role": "admin"}'

karana1 = '{"name": "KaranaUltimate", "note": "This is Michas first karana"}'
karana2 = '{"name": "KaranaGiga", "note": "This is Michas second karana"}'
karana3 = '{"name": "KaranaFantastic", "note": "This is Daniels first karana"}'


seed = dict(user=[dict(schema.UserSchema().dump(schema.UserSchema().loads(user2).data).data),
                  dict(schema.UserSchema().dump(schema.UserSchema().loads(user2).data).data)],
            karana=[dict(schema.KaranaSchema().dump(schema.KaranaSchema().loads(karana1).data).data),
                    dict(schema.KaranaSchema().dump(schema.KaranaSchema().loads(karana2).data).data),
                    dict(schema.KaranaSchema().dump(schema.KaranaSchema().loads(karana3).data).data)]
            )
