##

docstring='''db wrapper for the karana backend api'''
from log import log
import tinydb
import sys
import os
from configuration import resources as resourceConfig

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

class KaranaDBWrapper(object):
    ''' Karana DB Wrapper'''

    def __init__(self):
        self.db = tinydb.TinyDB(__karanaDbPath__)
        self.res_schema = None
        self.tables = {}
        if "uuid_index" not in self.db.tables():
            self.__uuid_index__ = {}

        # sanitation old databases needed
        for res_id in resourceConfig.keys():
            self.tables[resourceConfig[res_id]['name']] = self.db.table(resourceConfig[res_id]['name'])
            self.tables[resourceConfig[res_id]['name']].insert(resourceConfig[res_id]['metadata'])


    def update_uuid_index(self):
        for table in self.tables:
            pass
        pass

    def add_new_res(self, table, res):
        pass

    def modify_value_in_res(self, res, key, value):
        pass

    def get_res_tables(self):
        pass

    def get_table_schema(self):
        pass

    def get_res(self):
        pass

    def create_res(self):
        pass

    def rm_res(self):
        pass



