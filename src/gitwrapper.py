"""This class checks if the configuration for the meta data already exists and establishes version control for the backup"""
import os.path
from configuration import resources as resourceConfig
import json
from logger import log




class GitWrapper(object):
    def __init__(self, dump_files):
        self.table_db_path = dump_files['table_db_path']
        self.table_meta_db_path = dump_files['table_meta_db_path']

    def check_table_file_exists(self):
        if os.path.isfile(self.table_db_path):
            return True
        return False

    def check_table_meta_file_exists(self):
        if os.path.isfile(self.table_meta_db_path):
            return True
        return False

    def create_table_file(self):
        log.debug("Creating EmptyTable File ")
        # maybe it should not be empty (no one can log into this api!)
        # but do it with the initial user credentials from the multitenant
        try:
            with open(self.table_db_path, 'w')as db_file:
                db_file.write('{}')
        except Exception as e:
            log.error("Creating Table File failed", e)
            return False

    def create_table_meta_file(self):
        try:
            log.debug("Creating Table Meta File with configuration.py")
            with open(self.table_meta_db_path, 'w')as db_file:
                db_file.write(json.dumps(resourceConfig))
        except Exception as e:
            log.error("Creating Table Meta File failed", e)
            return False

