"""This file contains 2 users and three karanas for testing purposes"""
import schema

user1 = '{"name": "Micha", "email": "Micha@python.com", "role": "admin"}'
user2 = '{"name": "Daniel", "email": "Daniel@python.com", "role": "admin"}'

karana1 = '{"name": "KaranaUltimate", "note": "This is Michas first karana"}'
karana2 = '{"name": "KaranaGiga", "note": "This is Michas second karana"}'
karana3 = '{"name": "KaranaFantastic", "note": "This is Daniels first karana"}'


user1 = schema.UserSchema().loads(user1).data
user2 = schema.UserSchema().loads(user2).data

karana1 = schema.KaranaSchema().loads(karana1).data
karana2 = schema.KaranaSchema().loads(karana2).data
karana3 = schema.KaranaSchema().loads(karana3).data

user1.karanas.append(karana1)
user1.karanas.append(karana2)
user2.karanas.append(karana3)

seed = dict(user=[dict(schema.UserSchema().dump(user1).data),
                  dict(schema.UserSchema().dump(user2).data)],
            karana=[dict(schema.KaranaSchema().dump(karana1).data),
                    dict(schema.KaranaSchema().dump(karana2).data),
                    dict(schema.KaranaSchema().dump(karana3).data)]
            )
