##

docstring='''db wrapper for the karana backend api'''
from log import log
import tinydb
import sys
import os
from configuration import resources as resourceConfig
import inspect
import schema

# get the db file path
defaultKaranaDbPath = "~/karana_db.json"
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
    globalschemas[name]=obj()

class KaranaDBWrapper(object):
    ''' Karana DB Wrapper'''

    def __init__(self):
        self.db = tinydb.TinyDB(__karanaDbPath__)
        self.res_schema = None
        self.tables = {}
        self.uuid_index = {}
        self.schema_index = {}
        self.__prepare_db__()

    def __prepare_db__(self):
        # sanitatized import, consistency checks and repair/migration of old databases needed
        # resourceConfig[res_id]['name'] need to fit in a schema (a-z,A-Z,0-9)
        for res_table_id in resourceConfig.keys():
            log.debug('"create table instances (no overwrite)"')
            res_table_name = resourceConfig[res_table_id]['name']
            self.tables[res_table_name] = self.db.table(res_table_name)
            log.debug('"overwrite metadata entry in db with the one from configuration"')
            self.tables[res_table_name].insert(resourceConfig[res_table_name]['metadata'])
            schema_name = resourceConfig[res_table_name]['entry_schema']
            if schema_name in globalschemas.keys():
                self.schema_index[res_table_name] = globalschemas[schema_name]

    def update_uuid_index(self):
        try:
            for table in self.tables:
                for entry in table.all():
                    if 'uuid' in entry.keys():
                        self.uuid_index[entry["uuid"]] = table[entry["uuid"]]
        except:
            log.error("could not update uuid index, maybe some tables or entries are broken")

    def add_new_res(self, table: str, res: str):
        try:
            new_res = False
            new_res = self.schema_index[table].loads(res)
            if not new_res.errors:
                self.tables[table].insert(new_res.data)
                return new_res.data['uuid']
        except:
            log.error("resource json validation or db import error")

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



