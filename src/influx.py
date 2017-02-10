import http.client
import base64
from log import log
import json
from configparser import ConfigParser

class InfluxDBWrapper(object):
    """The __ functions are helpers, defines functions to create a client and register a karana"""
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
            log.error('Privilege was not in all, write, read!')
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

    def insert_config(self, db, config, karana_id):
        """This method inserts a config into the influx db with the karana id, note there is no style checing
        for the config!"""
        resp = self.__send_insert_request__(db, 'config,data=' + config + ',id=' + karana_id + ' v=0')
        return resp == 204

    def get_config(self, db, karana_id):
        """This method returns the last config for a certain karana id"""
        resp = self.__send_get_request__(db, "select+last(*),data+from+config+where+id='" + karana_id + "'")
        if resp:
            log.debug('config is: ' + str(resp))
            index = resp['results'][0]['series'][0]['columns'].index('data')
            config = resp['results'][0]['series'][0]['values'][0][index]
            return str(config)
        return False

    def __get_parser__(self):
        '''This returns the parser of the config.ini file'''
        parser = ConfigParser()
        log.debug('Load config.ini')
        parser.read('../config.ini')
        return parser

    def __send_get_request__(self,db,query):
        '''This method sends a get request with the appropriate query for SHOW and SELECT!'''
        log.info('Start get request: db=' + db + ' q=' + query )
        client = self.__conn_setup__()
        try:
            client.request("GET", "/query?db=" + db + "&q=" + query, headers=self.__get_header__())
            resp = client.getresponse()
            log.info('Get response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            return json.loads(str(resp.read().decode('utf-8'))[:-1])
        except json.JSONDecodeError:
            log.error('No JSON came back from the get request to influx DB')
            return None
        except Exception:
            log.error('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
            return None

    def __send_post_request__(self, db, query):
        '''This method sends a post request with the appropriate query for ALTER CREATE DELETE DROP GRANT KILL REVOKE!'''
        log.info('Start post request: db=' + db + ' q=' + query)
        client = self.__conn_setup__()
        try:
            client.request("POST","/query?db="+ db + "&q=" + query,headers=self.__get_header__())
            resp = client.getresponse()
            log.info('Post response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            iserror = str(resp.read().decode('utf-8'))
            log.debug(iserror)
            if iserror.find('error') >= 0:
                raise Exception
            return resp.status
        except json.JSONDecodeError:
            log.error('No JSON came back from the get request to influx DB')
            return 400
        except Exception:
            log.error('The POST Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
            return 400

    def __send_insert_request__(self, db, data):
        '''This method sends a write request with the appropriate data in influx command line syntax'''
        log.info('Start insert request: db=' + db + ' insert=' + data )
        client = self.__conn_setup__()
        try:
            client.request("POST","/write?db="+ db, data, headers=self.__get_header__())
            resp = client.getresponse()
            log.info('Insert response is: ' + str(resp.status))
            if resp.status >= 400:
                raise Exception
            return resp.status
        except Exception:
            log.error('The Insert Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
            return resp.status


    def __conn_setup__(self):
        '''This establishes a connection to influxDB which can be used to send requests to the influxdb instance'''
        log.info('Setup Connection')
        parser = self.__get_parser__()
        try:
            return http.client.HTTPSConnection(parser.get('influxdb','host') + ':' + parser.get('influxdb','port'))
        except Exception:
            log.error('The http connection to the influx instance could not be instanciated')
            return None

    def __get_header__(self):
        '''This returns the header with correct basic auth'''
        log.info('Create Header')
        parser = self.__get_parser__()
        userAndPass = base64.b64encode(bytes(parser.get('influxdb','user') + ':' + parser.get('influxdb','pass'),"utf-8")).decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass , "Content-type": "application/x-www-form-urlencoded"}
        log.info('header:' + str(headers))
        return headers



