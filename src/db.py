##

docstring='''db wrapper for the karana backend api'''
from log import log
import tinydb
import os
import sys
from configuration import resources as resourceConfig
import inspect
import schema


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


class KaranaDBWrapper(object):
    ''' Karana DB Wrapper'''

    def __init__(self):
        self.db = tinydb.TinyDB(__karanaDbPath__, indent=4, sort_keys=True)
        self.res_schema = None
        self.main_state = {'metadata': {},\
                           'tables': {}}
        self.tables = self.main_state['tables']
        self.uuid_index = {}
        self.schema_index = {}
        self.__prepare_state__()
        self.__uniqueness_index__ = {}

    def __prepare_state__(self):
        # sanitatized import, consistency checks and repair/migration of old databases needed
        # resourceConfig[res_id]['name'] need to fit in a schema (a-z,A-Z,0-9)
        for res_table_id in resourceConfig.keys():
            log.debug("create table instances ")
            log.debug("pull res_table_name and schema_name from the config")
            res_table_name = resourceConfig[res_table_id]['metadata']['name']
            schema_name = resourceConfig[res_table_id]['metadata']['entry_schema']
            log.debug("try to find the schema for this table as mentioned in the config.")
            if schema_name in globalschemas.keys():
                self.schema_index[res_table_name] = globalschemas[schema_name]
                log.debug("the following schema is added to the schema_index: " + str(schema_name))
            else:
                log.error("Major error, the configuration is corrupted!\nThe following schema with the schema_name: '" + \
                          str(schema_name) + \
                          "' from the configuration is not implemented! \n" +  \
                          "Only on of the following schemas are defined: " +
                          str(globalschemas) + \
                          "\nThe service ist stopped, repair the configuration and restart it.")
                sys.exit(1)

            self.tables[res_table_name] = {}
            table_schema = self.schema_index[res_table_name]
            if res_table_name in self.db.tables():
                db_table = self.db.table(res_table_name)
                db_table_state = db_table.all()
                for entry in db_table_state:
                    if len(entry) == 1:
                        try:
                            entry = dict(entry)
                        except:
                            log.error("The following entry in the table '" + \
                                      str(res_table_name) + \
                                      "' could not be converted to a dict: '" + \
                                      str(entry) + \
                                      "'.\nIt will not be imported!")
                            break
                        #import it
                        try:
                            pass
                        except:
                            pass

                    elif len(entry) == 0:
                        log.warning("An empty entry was found and ignored in the db (table: '" +\
                                    res_table_name + \
                                    "').")
                    else:
                        log.warning("A malformed entry was found in the db table: '" +\
                                    res_table_name + \
                                    "'."))
            #log.debug('"overwrite metadata entry in db with the one from configuration"')
            #self.tables[res_table_name].insert(resourceConfig[res_table_id]['metadata'])


    def __push_deb__(self):
        pass

    def update_uniqueness_index(self):
        for table in self.tables:
            for entry in table.all():
                pass

    def update_uuid_index(self):
        try:
            for table in self.tables:
                for entry in table.all():
                    if 'uuid' in entry.keys():
                        self.uuid_index[entry["uuid"]] = table[entry["uuid"]]
        except:
            log.error("could not update uuid index, maybe some tables or entries are broken")

    def add_new_res(self, table: str, body: str):

        try:
            Schema_class = self.schema_index[table]
            new_res, errors = Schema_class().loads(body)
            userdict = dict(Schema_class().dump(new_res).data)
            ### unique field check
            self.tables[table].insert(userdict)
            return userdict['uuid']
        except:
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



