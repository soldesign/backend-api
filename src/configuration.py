
''' this file contains the configuration'''

################################################################################
## resource definition section
################################################################################

####### single resources (take care with the structure)
users = {'metadata': {'res_table_id': 1,\
                      'schema': {'entry_create_schema': "UserSchema",\
                                 'entry_import_schema': "UserDbSchema"
                                 },\
                      'name': "users",\
                      'unique_schema_fields': ['uuid', 'email'],\
                      'credentials_login_field': 'email',\
                     }\
        }

karanas = {'metadata': {'res_table_id': 2,\
                        'schema': {'entry_create_schema': "KaranaSchema",\
                                   'entry_import_schema': "KaranaDbSchema"
                                   },\
                        'name': "karanas",\
                        'unique_schema_fields': ['uuid'],
                        'credentials_login_field': None,\
                        }\
          }


######## the collection of used resources (only this structure is directly used)
resources = {users['metadata']['name']: users,\
             karanas['metadata']['name']: karanas\
             }
################################################################################
################################################################################

################################################################################
## api instance general metadata + configuration
################################################################################

api_metadata = {'tenant_id': 'SMNTYQIUB4YTC',
                'tenant_customer_name': 'Bintumani e.V.',
                'tenant_login_credentials_resource': 'users', # path to the login credentials (define in Schema: here 'UserSchema')
                'tenant_login_credentials_field': 'credentials', # path to the login credentials (define in Schema: here 'UserSchema')
                'tenant_used_login_credentials': ['login', 'pwhash'],
                'logging_config_file': 'logging.yaml',
                'db_dump': {'table_db_path': "storage/table_db.json",\
                            'table_meta_db_path': "storage/tablestate_db.json"
                            }
               }




'''
##########################
#### example tenant_id generator dunction
import base64
import random

keysize = 64
example_id = base64.b32encode(random.getrandbits(keysize).to_bytes(int(keysize/8), "big"))[:-3]
##########################
'''