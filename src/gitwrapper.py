"""This class checks if the configuration for the meta data already exists and establishes version control for the backup"""
import os.path
import os
from configuration import resources as resourceConfig
import json
import git
from logger import log




class GitWrapper(object):
    def __init__(self, dump_files):
        self.table_db_path = dump_files['table_db_path']
        self.table_meta_db_path = dump_files['table_meta_db_path']
        self.table_db_folder = dump_files['table_db_folder']

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

    def check_git_repo_exists(self):
        try:
            log.debug('loading git repo')
            git.Repo(self.table_db_folder)
            return True
        except git.InvalidGitRepositoryError:
            log.debug('not a git repo')
            return False

    def create_git_repo(self):
        try:
            log.debug('creating git repo' )
            os.environ['PATH'] = os.environ['PATH'] + ':' + '/root/api/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin'
            log.debug('check if git is seen: ' + os.environ['PATH'])
            git.Repo.init(self.table_db_folder)
            return True
        except Exception as e:
            log.error('couldnt create git repo', e)
            return False

    def commit_changes(self):
        """This function commits changes should be called after every write"""
        try:
            log.debug('loading git repo')
            repo = git.Repo(self.table_db_folder)
            repo.git.add('.')
            repo.git.commit(m='committing database json')
            return True
        except git.InvalidGitRepositoryError:
            log.debug('not a git repo')
            return False
        except git.GitCommandError:
            log.debug('empy commit nothing changed')
            return True
