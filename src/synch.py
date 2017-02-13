"""This file checks a given seed of database entries and performs idempoten synchs"""
from influx import InfluxDBWrapper
import logging


class SynchInflux(object):
    """This class provides the methods to synch a given seed with an influxdb instance"""
    def __init__(self):
        #self.seed = seed
        self.wrapper = InfluxDBWrapper()
        self.log = logging.getLogger(__name__)

    def check_user_read(self, user_id, password):
        """This function checks if a given user can read from the database behind user_id"""
        self.log.info('Check that user ' + user_id + ' exists. And can read.')
        self.wrapper.insert_timepoint(user_id, 'check', 'check', '123')
        return self.wrapper.get_last_timepoint(user_id, 'check', '123', user_id, password) == 'check'

    def check_karana_read(self, user_id, karana_id, password):
        """This function checks if a given karana can read from the database behind user_id"""
        self.log.info('Check that karana ' + karana_id + ' exists. And can read.')
        self.wrapper.insert_timepoint(user_id, 'check', 'check', '123')
        return self.wrapper.get_last_timepoint(user_id, 'check' '123', karana_id, password) == 'check'

    def check_karana_write(self, user_id, karana_id, password):
        self.log.info('Check that karana ' + karana_id + ' exists. And can read.')
        """This function checks if a given karana can write to the database behind user_id"""
        return self.wrapper.insert_timepoint(user_id, 'check', 'check', '123' , karana_id, password)

    def register_user(self, user_id, password):
        """This function creates a database for a given user and a user with read privileges on that db"""
        self.log.info('Register user ' + user_id + ' and create db')
        db_created = self.wrapper.create_db(user_id)
        user_created = self.wrapper.create_user(user_id, password)
        privileges = self.wrapper.grant_privilege_user(user_id, user_id, 'read')
        return db_created and user_created and privileges

    def register_karana(self, user_id, karana_id, password):
        """This function creates a user with read and write privileges on a given db"""
        self.log.info('Register karana ' + karana_id + ' on db ' + user_id)
        karana_created = self.wrapper.create_user(karana_id, password)
        privileges = self.wrapper.grant_privilege_user(user_id, karana_id, 'all')
        return karana_created and privileges

    def remove_user(self, user_id):
        """This function creates a database for a given user and a user with read privileges on that db"""
        self.log.info('Remove user ' + user_id + ' and remove db')
        db_removed = self.wrapper.remove_db(user_id)
        user_removed = self.wrapper.remove_user(user_id)
        return user_removed and db_removed

    def remove_karana(self, karana_id):
        """This function creates a user with read and write privileges on a given db"""
        self.log.info('Remove karana user ' + karana_id)
        return self.wrapper.remove_user(karana_id)







