##

docstring = '''db wrapper for the karana backend api'''
from log import log
import tinydb
import os
import sys
from configuration import resources as resourceConfig
from synch import SynchInflux
import inspect
import schema
import json
from uuid import UUID

# get the db file path
defaultKaranaDbPath = "src/backup/db.json"
__karanaDbPath__ = ""

if 'KARANA_BACKEND_DB' in os.environ.keys():
    try:
        fp = open(os.environ['KARANA_BACKEND_DB'], "rw")
        fp.close()
        __karanaDbPath__ = os.environ['KARANA_BACKEND_DB']
    except PermissionError:
        log.warning("can't open the path defined in env var 'KARANA_BACKEND_DB': " + \
                    str(os.environ['KARANA_BACKEND_DB']).replace('\n', '   ') + \
                    "\n the default db path is used: " + \
                    str(defaultKaranaDbPath) \
                    )
        __karanaDbPath__ = defaultKaranaDbPath
else:
    __karanaDbPath__ = defaultKaranaDbPath

# all defined schemas in a dict
globalschemas = {}
for name, obj in inspect.getmembers(schema):
    if 'Schema' in name:
        globalschemas[name] = obj

log.debug("List of all implemented schemas: " + str(globalschemas.keys()))


class KaranaDBWrapper(object):
    ''' Karana DB Wrapper'''

    def __init__(self):
        self.db = {}
        self.res_schema = None
        log.debug("initialize empty main_state and special 'pointers'")
        self.pre_tables = {}
        self.main_state = {'metadata': {}, \
                           'tables': {}, \
                           'uuid_index': {}, \
                           'uniqueness_index': {}, \
                           'sync_state': {} \
                           }
        self.__load_pre_main_state__()
        self.tables = self.main_state['tables']
        self.uuid_index = self.main_state['uuid_index']
        self.uniqueness_index = self.main_state['uniqueness_index']
        self.sync_state = self.main_state['sync_state']
        self.schema_index = {}

        log.debug("This is how the main_state looks right now: " + str(self.main_state))

        ########
        log.debug("Now the population methods will be started:")
        ##
        log.debug("self.__build_schema_index__():")
        self.__build_schema_index__()
        self.__sync_state_action__()

        log.debug("This is how the main_state looks right now: " + str(self.main_state))
        ##
        log.debug("")

    def __build_schema_index__(self):
        self.sync_state['sync'] = False
        for res_table_id in resourceConfig.keys():
            log.debug("create table instances ")
            log.debug("pull res_table_name and schema_name from the config")
            res_table_name = resourceConfig[res_table_id]['metadata']['name']
            log.debug("create dict with in self.schema_index '" + str(
                res_table_name) + "' with the resource table name from the config.")
            self.schema_index[res_table_name] = {}
            log.debug("Schema: " + str(resourceConfig[res_table_id]['metadata']['schema'].keys()))
            for schema_type in resourceConfig[res_table_id]['metadata']['schema']:
                schema_name = resourceConfig[res_table_id]['metadata']['schema'][schema_type]
                log.debug("try to find the schema for this table as mentioned in the config.")
                if schema_name in globalschemas.keys():
                    self.schema_index[res_table_name][schema_type] = globalschemas[schema_name]
                    log.debug("the following schema is added to the schema_index: " + str(schema_name))
                else:
                    log.error(
                        "Major error, the configuration is corrupted!\nThe following schema with the schema_import_name: '" + \
                        str(schema_name) + \
                        "' from the configuration is not implemented! \n" + \
                        "Only on of the following schemas are defined: " +
                        str(globalschemas) + \
                        "\nThe service ist stopped, repair the configuration and restart it.")
                    sys.exit(1)
            log.debug(
                "Now the data structure in the schema_index and the empty table is set up.\n\nLet's populate the table '" + res_table_name + "'")
            if not res_table_name in self.tables:
                self.tables[res_table_name] = {}  # TODO: is this correct??

            self.__import_table_from_db__(res_table_name)
        self.sync_state['sync'] = True

    def __import_table_from_db__(self, table_name):
        # sanitatized import, consistency checks and repair/migration of old databases needed
        # resourceConfig[res_id]['name'] need to fit in a schema (a-z,A-Z,0-9)
        log.debug("Schema Index " + str(self.schema_index))
        table_import_schema = self.schema_index[table_name]['entry_import_schema']
        if table_name in self.pre_tables:
            db_table_state = self.pre_tables[table_name]
            log.debug("go through all entries in table: '" + \
                      str(table_name) + \
                      "' and try to import it to the internal table representation")
            for entry in db_table_state:
                log.debug(
                    "every entry in the list of all entries should have the length == 1 and a key which is 'metadata' or an uuid-type string.\n" + \
                    "every thing else is malformed")
                log.debug("Entry: " + str(entry) + ' length ' + str(len(entry)))
                if len(entry) == 36:
                    try:
                        # get the 'metadata' entry which is special and can be imported without checks ?!
                        # if dict(entry).keys()[0] == 'metadata':
                        #     try:
                        #         self.tables[table_name]['metadata'] = dict(entry)
                        #     except:
                        #         log.error("could not load 'metadata' field from config/db.")
                        #         sys.exit(1)
                        #     continue
                        # else:
                        # all others will be reimported through a dict to a json again
                        entry_json = json.dumps(self.pre_tables[table_name][entry])
                    except Exception as e:
                        log.error("The following entry in the table '" + \
                                  str(table_name) + \
                                  "' could not be converted to a dict: '" + \
                                  str(entry) + \
                                  "'.\nIt will not be imported!", e)
                        # this should be discussed: break or exit?
                        exit()
                        # try to import it, through the validation from the import schema of the table
                    try:
                        validated_entry = table_import_schema(strict=True).loads(entry_json)
                        log.debug('validated? ' + str(validated_entry))
                        # now everything is checked and filtered, the entry may be written as element to the table
                        # maybe here or somewhere else a the uniqueness could be checked:
                        # I think here the uniqueness index should be filled and there it could be checked
                        if validated_entry.errors != {}:
                            raise
                        self.main_state['tables'][table_name][entry] = json.loads(entry_json)
                        log.debug("This is how the main_state looks right now: " + str(self.main_state))
                        continue
                    except Exception as e:
                        log.error("could not import the following entry: '" + \
                                  str(entry) + ': ' + str(entry_json) +\
                                  "'.", e)
                        exit()
                elif len(entry) == 0:
                    log.warning("An empty entry was found and ignored in the db (table: '" + \
                                table_name + \
                                "').")
                    exit()
                else:
                    log.warning("A malformed entry was found in the db table: '" + \
                                table_name + \
                                "'.")
                    exit()

    def __sync_state_action__(self):
        log.info('synching the created user and karanas with the influxdb and dumping the main_stateS')
        Synch = SynchInflux()
        for uuid in self.sync_state:
            if uuid != 'sync':
                log.info('Synching uuid ' + uuid)
                if not self.sync_state[uuid]:
                    log.debug("Theses key are usable: " + str(self.tables['users'].keys()))
                    if uuid in self.tables['users'].keys():
                        try:
                            log.debug('Synching User ' + uuid + 'with the influx')
                            password = self.tables['users'][uuid]['credentials']['password']
                            if not Synch.check_user_read(uuid, password):
                                if not Synch.register_user(uuid, password):
                                    raise
                                self.sync_state[uuid] = True
                            continue
                        except:
                            log.debug('Synching User ' + uuid + 'with the influx failed')
                            return False
                    elif uuid in self.tables['karanas'].keys():
                        try:
                            log.debug('Synching Karana ' + uuid + 'with the influx')
                            password = self.tables['karanas'][uuid]['credentials']['password']
                            user_id = self.tables['karanas'][uuid]['owner']
                            if not Synch.check_karana_read(user_id, uuid, password) or Synch.check_karana_write(user_id,
                                                                                                                uuid,
                                                                                                                password):
                                if not Synch.register_karana(user_id, uuid, password):
                                    raise
                                self.tables['users'][user_id]['karanas'].append(uuid)
                                self.sync_state[uuid] = True
                            continue
                        except:
                            log.debug('Synching Karana ' + uuid + 'with the influx failed')
                            return False
                    else:
                        log.debug('set synch state true for a non user or karana uuid')
                        self.sync_state[uuid] = True
        if self.sync_state['sync']:
            self.__dump_main_state__()
        return True

    def __dump_main_state__(self):
        log.info("Dumping the main state to the location: " + defaultKaranaDbPath)
        try:
            with open(defaultKaranaDbPath, 'w')as db_file:
                db_file.write(json.dumps(self.main_state['tables']))
            self.sync_state['sync'] = True
            return True
        except Exception as e:
            log.error("Dumping Database failed", e)
            return False

    def __load_pre_main_state__(self):
        log.info("Loading the main state to the location: " + defaultKaranaDbPath)
        try:
            with open(defaultKaranaDbPath, 'r') as db_file:
                content = db_file.read()
            self.pre_tables = json.loads(content)
            return True
        except Exception as e:
            log.error("Dumping Database failed", e)
            return False

    def __push_deb__(self):
        pass

    def update_uniqueness_index(self):
        for table in self.tables:
            for entry in table.all():
                pass

    def __update_uuid_index__(self):
        try:
            for table in self.tables:
                for entry in self.tables[table].keys():
                    if 'uuid' in entry.keys():
                        self.uuid_index[entry["uuid"]] = table[entry["uuid"]]
        except:
            log.error("could not update uuid index, maybe some tables or entries are broken")

    def get_res_by_id(self, table: str, uuid: str):
        try:
            log.debug("Request id: " + uuid + " of table " + table)
            UUID(uuid, version=4)
            return self.tables[table][uuid]
        except ValueError:
            log.error('The provided uuid is no uuid version 4')
            return False
        except:
            log.error("resource not found")
            return False

    def get_res(self, table: str):
        try:
            log.debug("Request table " + table)
            return self.tables[table]
        except:
            log.error("resource not found")
            return False

    def add_new_res(self, table: str, body: str):
        try:
            schema_class = self.schema_index[table]['entry_create_schema']
            new_res, errors = schema_class(strict=True).loads(body)
            userdict = dict(schema_class().dump(new_res).data)
            # unique field check
            self.tables[table][userdict['uuid']] = userdict
            log.debug('Main State: ' + str(self.main_state))
            # is one of the following fails the entriy needs to be deleted again TODO: check this!
            try:
                self.sync_state['sync'] = False
                #self.__update_uuid_index__()
                self.sync_state[userdict['uuid']] = False
                self.__dump_main_state__()
            except:
                del self.tables[table][userdict['uuid']]
                raise
            return userdict['uuid']
        except Exception as e:
            log.error("resource json validation or db import error", e)
            return False

    def update_res(self, table: str, uuid: str, body: str):
        try:
            log.debug("Request to update id: " + uuid + " of table " + table + "with body: " + body)
            UUID(uuid, version=4)
            schema_class = self.schema_index[table]['entry_import_schema']
            up_res, errors = schema_class(partial=True).loads(body)
            if len(up_res) < 2:
                raise
            for key, value in up_res.items():
                self.tables[table][uuid][key] = value
            log.debug('Main State: ' + str(self.main_state))
            self.sync_state['sync'] = False
            self.__dump_main_state__()
            return self.tables[table][uuid]
        except ValueError:
            log.error('The provided uuid is no uuid version 4')
            return False
        except Exception as e:
            log.error("resource json validation or db import error")
            return False

    def modify_res(self, table: str, uuid: str, body: str):
        try:
            log.debug("Request to modify id: " + uuid + " of table " + table + "with body: " + body)
            UUID(uuid, version=4)
            schema_class = self.schema_index[table]['entry_import_schema']
            mod_res, errors = schema_class(partial=True).loads(body)
            if len(mod_res) != 1:
                raise
            key, value = list(mod_res.items())[0]
            self.tables[table][uuid][key] = value
            log.debug('Main State: ' + str(self.main_state))
            self.sync_state['sync'] = False
            self.__dump_main_state__()
            return self.tables[table][uuid]
        except ValueError:
            log.error('The provided uuid is no uuid version 4')
            return False
        except Exception as e:
            log.error("resource could not be modified")
            return False

    def rm_res(self, table: str, uuid: str):
        try:
            log.debug("Request id: " + uuid + " of table " + table)
            UUID(uuid, version=4)
            del self.tables[table][uuid]
            del self.sync_state[uuid]
            log.debug('Main State: ' + str(self.main_state))
            self.sync_state['sync'] = False
            self.__dump_main_state__()
            return self.tables[table]
        except ValueError:
            log.error('The provided uuid is no uuid version 4')
            return False
        except:
            log.error("resource not found")
            return False
