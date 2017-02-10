
''' this file contains the configuration'''



users = {'metadata': {'res_table_id': 1,\
                      'entry_schema:' "UserSchema",\
                     }\
        }

karanas = {'metadata': {'res_table_id': 2,\
                       'entry_schema:' "KaranaSchema",\
                       }\
          }


resources = { users['metadata']['res_table_id']: users,\
              karanas['metadata']['res_table_id']: karanas\
              }


# maybe used later
index = {}
