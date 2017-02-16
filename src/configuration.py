
''' this file contains the configuration'''



users = {'metadata': {'res_table_id': 1,\
                      'schema': {'entry_create_schema': "UserSchema",\
                                 'entry_import_schema': "UserDbSchema"
                                 },\
                      'name': "users",\
                      'unique_schema_fields': ['uuid', 'email']
                     }\
        }

karanas = {'metadata': {'res_table_id': 2,\
                        'schema': {'entry_create_schema': "KaranaSchema",\
                                   'entry_import_schema': "KaranaDbSchema"
                                   },\
                        'name': "karanas",\
                        'unique_schema_fields': []
                       }\
          }


resources = { users['metadata']['res_table_id']: users,\
              karanas['metadata']['res_table_id']: karanas\
              }

loginresource = 'users'

# maybe used later
index = {}
