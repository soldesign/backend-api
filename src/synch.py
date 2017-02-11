"""This file checks a given seed of database entries and performs idempoten synchs"""
from influx import InfluxDBWrapper


class SynchInflux(object):
    """This class provides the methods to synch a given seed with an influxdb instance"""
    def __init__(self, seed):
        self.seed = seed
        self.wrapper = InfluxDBWrapper()

    def check_users(self):
        pass

    def check_dbs(self):
        pass






