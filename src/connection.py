import http.client
import base64
from log import log
import json
from configparser import SafeConfigParser


def get_parser():
    '''This returns the parser of the config.ini file'''
    parser = SafeConfigParser()
    logdebug('Load config.ini')
    parser.read('../../config.ini')
    return parser


def send_get_request(db,query):
    '''This method sends a get request with the appropriate query for SHOW and SELECT!'''
    loginfo('Start get request: db=' + db + ' q=' + query )
    client = conn_setup()
    try:
        client.request("GET","/query?db="+ db + "&q=" + query,headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return json.loads(str(resp.read().decode('utf-8'))[:-1])
    except json.JSONDecodeError:
        logerror('No JSON came back from the get request to influx DB')
        return None
    except Exception:
        logerror('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None

def send_post_request(db,query):
    '''This method sends a post request with the appropriate query for ALTER CREATE DELETE DROP GRANT KILL REVOKE!'''
    loginfo('Start post request: db=' + db + ' q=' + query )
    client = conn_setup()
    try:
        client.request("POST","/query?db="+ db + "&q=" + query,headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return resp.status
    except json.JSONDecodeError:
        logerror('No JSON came back from the get request to influx DB')
        return None
    except Exception:
        logerror('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None


def send_insert_request(db,data):
    '''This method sends a write request with the appropriate data in influx command line syntax'''
    loginfo('Start insert request: db=' + db + ' insert=' + data )
    client = conn_setup()
    try:
        client.request("POST","/write?db="+ db, data, headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return resp.status
    except Exception:
        logerror('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None


def conn_setup():
    '''This establishes a connection to influxDB which can be used to send requests to the influxdb instance'''
    loginfo('Setup Connection')
    parser = get_parser()
    try:
        return http.client.HTTPSConnection(parser.get('influxdb','host') + ':' + parser.get('influxdb','port'))
    except Exception:
        logerror('The http connection to the influx instance could not be instanciated')
        return None

def get_header():
    '''This returns the header with correct basic auth'''
    loginfo('Create Header')
    parser = get_parser()
    userAndPass = base64.b64encode(bytes(parser.get('influxdb','user') + ':' + parser.get('influxdb','pass'),"utf-8")).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass , "Content-type": "application/x-www-form-urlencoded"}
    loginfo('header:' + str(headers))
    
    return headers

