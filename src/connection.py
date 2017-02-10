import http.client
import base64
import logging
import json
from configparser import SafeConfigParser


def get_parser():
    '''This returns the parser of the config.ini file'''
    parser = SafeConfigParser()
    logging.debug('Load config.ini')
    parser.read('../../config.ini')
    return parser


def send_get_request(db,query):
    '''This method sends a get request with the appropriate query for SHOW and SELECT!'''
    logging.info('Start get request: db=' + db + ' q=' + query ) 
    client = conn_setup()
    try:
        client.request("GET","/query?db="+ db + "&q=" + query,headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return json.loads(str(resp.read().decode('utf-8'))[:-1])
    except json.JSONDecodeError:
        logging.error('No JSON came back from the get request to influx DB')
        return None
    except Exception:
        logging.error('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None

def send_post_request(db,query):
    '''This method sends a post request with the appropriate query for ALTER CREATE DELETE DROP GRANT KILL REVOKE!'''
    logging.info('Start post request: db=' + db + ' q=' + query )
    client = conn_setup()
    try:
        client.request("POST","/query?db="+ db + "&q=" + query,headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return resp.status
    except json.JSONDecodeError:
        logging.error('No JSON came back from the get request to influx DB')
        return None
    except Exception:
        logging.error('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None


def send_insert_request(db,data):
    '''This method sends a write request with the appropriate data in influx command line syntax'''
    logging.info('Start insert request: db=' + db + ' insert=' + data )
    client = conn_setup()
    try:
        client.request("POST","/write?db="+ db, data, headers=get_header())
        resp = client.getresponse()
        if resp.status >= 400:
            raise Exception
        return resp.status
    except Exception:
        logging.error('The GET Request did not succeed, Status: ' + str(resp.status) + ' ' + resp.reason)
        return None


def conn_setup():
    '''This establishes a connection to influxDB which can be used to send requests to the influxdb instance'''
    logging.info('Setup Connection')
    parser = get_parser()
    try:
        return http.client.HTTPSConnection(parser.get('influxdb','host') + ':' + parser.get('influxdb','port'))
    except Exception:
        logging.error('The http connection to the influx instance could not be instanciated')
        return None

def get_header():
    '''This returns the header with correct basic auth'''
    logging.info('Create Header')
    parser = get_parser()
    userAndPass = base64.b64encode(bytes(parser.get('influxdb','user') + ':' + parser.get('influxdb','pass'),"utf-8")).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass , "Content-type": "application/x-www-form-urlencoded"}
    logging.info('header:' + str(headers))
    
    return headers

