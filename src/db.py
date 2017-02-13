##

docstring='''db wrapper for the karana backend api'''
from log import log
import tinydb
import os
import sys
from configuration import resources as resourceConfig
import inspect
import schema
import json


# get the db file path
defaultKaranaDbPath = "/tmp/karana_db.json"
__karanaDbPath__ = ""

if 'KARANA_BACKEND_DB' in os.environ.keys():
    try:
        fp = open(os.environ['KARANA_BACKEND_DB'], "rw")
        fp.close()
        __karanaDbPath__ = os.environ['KARANA_BACKEND_DB']
    except PermissionError:
        log.warning("can't open the path defined in env var 'KARANA_BACKEND_DB': " + \
                    str(os.environ['KARANA_BACKEND_DB']).replace('\n', '   ') + \
                    "\n the default db path is used: " +\
                    str(defaultKaranaDbPath)\
                    )
        __karanaDbPath__ = defaultKaranaDbPath
else:
     __karanaDbPath__  = defaultKaranaDbPath

# all defined schemas in a dict
globalschemas = {}
for name, obj in inspect.getmembers(schema):
    globalschemas[name]=obj

log.debug("List of all implemented schemas: " + str(globalschemas.keys()))


class KaranaDBWrapper(object):
    ''' Karana DB Wrapper'''

    def __init__(self):
        self.db = tinydb.TinyDB(__karanaDbPath__, indent=4, sort_keys=True)
        self.res_schema = None
        log.debug("initialize empty main_state and special 'pointers'")
        self.main_state = {'metadata': {},\
                           'tables': {},\
                           'uuid_index': {},\
                           'uniqueness_index': {},\
                           'sync_state': {},\
                           'schema_index': {}
                           }
        self.tables = self.main_state['tables']
        self.uuid_index = self.main_state['uuid_index']
        self.uniqueness_index = self.main_state['uniqueness_index']
        self.sync_state = self.main_state['sync_state']
        self.schema_index = self.main_state['schema_index']
        log.debug("This is how the main_state looks right now: " + str(self.main_state) )

        ########
        log.debug("Now the population methods will be started:")
        ##
        log.debug("self.__import_state_from_db__():")
        self.__import_state_from_db__()
        log.debug("This is how the main_state looks right now: " + str(self.main_state) )
        ##
        log.debug("")

    def __build_schema_index__(self):
        for res_table_id in resourceConfig.keys():
            log.debug("create table instances ")
            log.debug("pull res_table_name and schema_name from the config")
            res_table_name = resourceConfig[res_table_id]['metadata']['name']
            log.debug("create dict with in self.schema_index '" + str(res_table_name) + "' with the resource table name from the config.")
            self.schema_index[res_table_name] = {}
            for schema_type, schema_name in resourceConfig[res_table_id]['metadata']['schema'].keys(), resourceConfig[res_table_id]['metadata']['schema'].keys():
                log.debug("try to find the schema for this table as mentioned in the config.")
                if schema_name in globalschemas.keys():
                    self.schema_index[res_table_name][schema_type] = globalschemas[schema_name]
                    log.debug("the following schema is added to the schema_index: " + str(schema_import_name))
                else:
                    log.error("Major error, the configuration is corrupted!\nThe following schema with the schema_import_name: '" + \
                              str(schema_import_name) + \
                              "' from the configuration is not implemented! \n" +  \
                              "Only on of the following schemas are defined: " +
                              str(globalschemas) + \
                              "\nThe service ist stopped, repair the configuration and restart it.")
                    sys.exit(1)
            log.debug("Now the data structure in the schema_index and the empty table is set up.\n\nLet's populate the table '" + res_table_name + "'")
            self.tables[table_name] = {}
            self.__import_table_from_db__(res_table_name)


    def __import_table_from_db__(self, table_name):
        # sanitatized import, consistency checks and repair/migration of old databases needed
        # resourceConfig[res_id]['name'] need to fit in a schema (a-z,A-Z,0-9)
        table_import_schema = self.schema_index[table_name + '_import']
        if table_name in self.db.tables():
            db_table = self.db.table(table_name)
            db_table_state = db_table.all()
            log.debug("go through all entries in table: '"+\
                      str(table_name) +\
                      "' and try to import it to the internal table representation")
            for entry in db_table_state:
                log.debug("every entry in the list of all entries should have the length == 1 and a key which is 'metadata' or an uuid-type string.\n" +\
                          "every thing else is malformed")
                if len(entry) == 1:
                    try:
                        # get the 'metadata' entry which is special and can be imported without checks ?!
                        if dict(entry).keys()[0] == 'metadata':
                            try:
                                self.tables[table_name]['metadata'] = dict(entry)
                            except:
                                log.error("could not load 'metadata' field from config/db.")
                                sys.exit(1)
                            continue
                        else:
                            # all others will be reimported through a dict to a json again
                            entry = json.dumps(dict(entry))
                    except:
                        log.error("The following entry in the table '" + \
                                  str(table_name) + \
                                  "' could not be converted to a dict: '" + \
                                  str(entry) + \
                                  "'.\nIt will not be imported!")
                        # this should be discussed: break or exit?
                        break
                    # try to import it, through the validation from the import schema of the table
                    try:
                        validated_entry = dict(table_import_schema(strict=True).loads(entry).data)
                        # now everything is checked and filtered, the entry may be written as element to the table
                        # maybe here or somewhere else a the uniqueness could be checked:
                        # I think here the uniqueness index should be filled and there it could be checked
                        self.tables[table_name][validated_entry['uuid']] = validated_entry
                        continue
                    except:
                        log.error("could not import the following entry: '" + \
                                  str(entry) + \
                                  "'.")

                elif len(entry) == 0:
                    log.warning("An empty entry was found and ignored in the db (table: '" +\
                                table_name + \
                                "').")
                else:
                    log.warning("A malformed entry was found in the db table: '" +\
                                table_name + \
                                "'.")



    def __push_deb__(self):
        pass

    def update_uniqueness_index(self):
        for table in self.tables:
            for entry in table.all():
                pass

    def update_uuid_index(self):
        try:
            for table in self.tables:
                for entry in self.tables[table].keys():
                    if 'uuid' in entry.keys():
                        self.uuid_index[entry["uuid"]] = table[entry["uuid"]]
        except:
            log.error("could not update uuid index, maybe some tables or entries are broken")

    def add_new_res(self, table: str, body: str):

        try:
            Schema_class = self.schema_index[table + '_create']
            new_res, errors = Schema_class(strict=True).loads(body)
            userdict = dict(Schema_class().dump(new_res).data)
            ### unique field check
            self.tables[table][userdict['uuid']] = userdict
            log.debug('Main State: ' + str(self.main_state))
            return userdict['uuid']
        except Exception as e:
            log.error("resource json validation or db import error")
            return False

    def get_db_dump(self):
        try:
            rodb = open(__karanaDbPath__, "r")
            dbdump = rodb.read()
            rodb.close()
            return dbdump
        except:
            return False


    def modify_value_in_res(self, res, key, value):
        pass

    def get_table_schema(self):
        pass

    def get_res(self):
        pass

    def create_res(self):
        pass

    def rm_res(self):
        pass



