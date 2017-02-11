import http.client
import base64
#from log import log
import logging
import json
from configparser import ConfigParser


class DBHTTPSetup(object):
    def __init__(self, db):
        self.db = db
        self.log = logging.getLogger(__name__)

    def __get_parser__(self):
        """This returns the parser of the config.ini file"""
        parser = ConfigParser()
        self.log.debug('Load config.ini')
        parser.read('config.ini')
        return parser

    def __conn_setup__(self,ssl=True):
        """This establishes a connection to influxDB which can be used to send requests to the influxdb instance"""
        self.log.info('Setup Connection')
        parser = self.__get_parser__()
        try:
            if ssl:
                return http.client.HTTPSConnection(parser.get(self.db, 'host') + ':' + parser.get(self.db, 'port'))
            elif not ssl:
                return http.client.HTTPConnection(parser.get(self.db, 'host') + ':' + parser.get(self.db, 'port'))
        except Exception:
            self.log.error('The http connection to the host: ' + self.db + ' instance could not be instanciated')
            return None

    def __get_header__(self, user=None, password=None, content_type="application/x-www-form-urlencoded"):
        """This returns the header with correct basic auth"""
        self.log.info('Create Header')
        parser = self.__get_parser__()
        if user is None:
            user = parser.get(self.db, 'user')
        if password is None:
            password = parser.get(self.db, 'pass')
        self.log.info('Create Header')
        user_and_pass = base64.b64encode(
            bytes(user + ':' + password, "utf-8")).decode("ascii")
        headers = {'Authorization': 'Basic %s' % user_and_pass, "Content-type": content_type}
        self.log.info('header:' + str(headers))
        return headers


class InfluxDBWrapper(DBHTTPSetup):
    """The __ functions are helpers, defines functions to create a client and register a karana"""

    def __init__(self):
        super().__init__(db='influxdb')

    def create_db(self, db):
        """This method creates a db in influx"""
        resp = self.__send_post_request__('_internal', 'create+database+' + db)
        return resp < 300

    def create_user(self, name, password):
        """This method creates a user on the database db"""
        resp = self.__send_post_request__('_internal', "create+user+" + name + "+with+password+'" + password + "'")
        return resp < 300

    def grant_privilege_user(self, db, name, privilege):
        """This method grants a user privileges on the database db, only all write and read are possible"""
        if privilege not in ['all', 'write', 'read']:
            self.log.error('Privilege was not in all, write, read!')
            return False
        resp = self.__send_post_request__(db, "grant+" + privilege + "+on+" + db + "+to+" + name)
        return resp < 300

    def remove_db(self, db):
        """This method removes a db in influx"""
        resp = self.__send_post_request__('_internal', 'drop+database+' + db)
        return resp < 300

    def remove_user(self, name):
        """This method removes a user in influx"""
        resp = self.__send_post_request__('_internal', 'drop+user+' + name)
        return resp < 300

    def insert_timepoint(self, db, timeseries, config, karana_id, user=None, password=None):
        """This method inserts a config into the influx db with the karana id, note there is no style checing
        for the config!"""
        resp = self.__send_insert_request__(db, timeseries + ',data=' + config + ',id=' + karana_id + ' v=0', user, password)
        return resp == 204

    def get_last_timepoint(self, db, timeseries, karana_id, user=None, password=None):
        """This method returns the last config for a certain karana id"""
        resp = self.__send_get_request__(db, "select+last(*),data+from+" + timeseries + "+where+id='" + karana_id + "'", user, password)
        if resp:
            self.log.debug('config is: ' + str(resp))
            index = resp['results'][0]['series'][0]['columns'].index('data')
            config = resp['results'][0]['series'][0]['values'][0][index]
            return str(config)
        return False

    def __send_get_request__(self, db, query, user=None, password=None):
        '''This method sends a get request with the appropriate query for SHOW and SELECT!'''
        self.log.info('Start get request: db=' + db + ' q=' + query)
        client = self.__conn_setup__()
        try:
            client.request("GET", "/query?db=" + db + "&q=" + query, headers=self.__get_header__(user, password))
            resp = client.getresponse()
            self.log.info('Get response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            return json.loads(str(resp.read().decode('utf-8'))[:-1])
        except json.JSONDecodeError:
            self.log.error('No JSON came back from the get request to influx DB')
            return None
        except Exception:
            self.log.error('The GET Request did not succeed, Status: ')
            return None

    def __send_post_request__(self, db, query):
        """This method sends a post request with the appropriate query for ALTER CREATE DELETE DROP GRANT KILL
        REVOKE! """
        self.log.info('Start post request: db=' + db + ' q=' + query)
        client = self.__conn_setup__()
        try:
            client.request("POST", "/query?db=" + db + "&q=" + query, headers=self.__get_header__())
            resp = client.getresponse()
            self.log.info('Post response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            iserror = str(resp.read().decode('utf-8'))
            self.log.debug(iserror)
            if iserror.find('error') >= 0:
                raise Exception
            return resp.status
        except json.JSONDecodeError:
            self.log.error('No JSON came back from the get request to influx DB')
            return 400
        except Exception:
            self.log.error('The POST Request did not succeed, Status: ' )
            return 400

    def __send_insert_request__(self, db, data, user=None, password=None):
        """This method sends a write request with the appropriate data in influx command line syntax"""
        self.log.info('Start insert request: db=' + db + ' insert=' + data)
        client = self.__conn_setup__()
        try:
            client.request("POST", "/write?db=" + db, data, headers=self.__get_header__(user, password))
            resp = client.getresponse()
            self.log.info('Insert response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            return resp.status
        except Exception:
            self.log.error('The Insert Request did not succeed, Status: ' )
            return 400
