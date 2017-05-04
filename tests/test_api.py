import os
import sys
import json

# import http.client
# import base64
# from log import log
import logging
import subprocess
import time
import os
import signal

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from influx import DBHTTPSetup
from influx import InfluxDBWrapper

# from seed import user1
command = ['bash', './run.sh']
pro = subprocess.Popen(['./run.sh'], shell=True,  # stdout=subprocess.PIPE,
                       preexec_fn=os.setsid)
time.sleep(50)


TestHTTP = DBHTTPSetup(db='test')
client = TestHTTP.__conn_setup__(ssl=False)
header = TestHTTP.__get_header__(content_type="application/json")

# http://127.0.0.1:8000/v1/users/new body='{"name":"Micha","role":"admin","email":"mica@all.de"}'
uuid = "0"
uuid2 = "0"
token = ''


def test_create_user_without_token():
    userdict = {
        'data': '{"name":"Micha","role":"admin","email":"mic@all.de","credentials":{"login":"mic@all.de","password":"12345"}}'}
    user = json.dumps(userdict)
    client.request("POST", "/v1/users/new/", user, header)
    resp = client.getresponse()
    assert not resp.status < 300


def test_get_auth_token_with_wrong_pw():
    client.request("POST", "/v1/users/login", '{"user":"admin@example.com","password":"admin2"}', headers=header)
    resp = client.getresponse()
    assert resp.status >= 400


def test_get_auth_token():
    client.request("POST", "/v1/users/login", '{"user":"admin@example.com","password":"admin"}', headers=header)
    resp = client.getresponse()
    assert resp.status < 300
    tmp = resp.read().decode('utf-8')
    results = json.loads(json.loads(tmp))
    global token
    token = results['results'][0]['token']
    global header
    header = TestHTTP.__get_header__(auth='bearer', token=token, content_type="application/json")
    print(token)


def test_get_user_fail():
    client.request("GET", "/v1/users/" + str(uuid), headers=header)
    resp = client.getresponse()
    assert not resp.status < 300


def test_create_user_and_karana():
    userdict = {
        'data': '{"name":"Micha","role":"admin","email":"mic@all.de","credentials":{"login":"mic@all.de","password":"12345"}}'}
    user = json.dumps(userdict)
    client.request("POST", "/v1/users/new/", user, header)
    resp = client.getresponse()
    assert resp.status < 300
    tmp = resp.read().decode('utf-8')
    results = json.loads(json.loads(tmp))
    global uuid
    uuid = results['results'][0]['uuid']
    karanadict = {'data': '{"name":"Karana","owner":"' + uuid + '","config":{}}'}
    karana = json.dumps(karanadict)
    client.request("POST", "/v1/karanas/new/", karana, header)
    resp = client.getresponse()
    assert resp.status < 300
    tmp = resp.read().decode('utf-8')
    results = json.loads(json.loads(tmp))
    global uuid2
    uuid2 = results['results'][0]['uuid']


def test_check_if_karana_config_was_created():
    wrapper = InfluxDBWrapper()
    client.request("POST", "/v1/sync/db/all", '', header)
    resp = client.getresponse()
    assert resp.status < 300
    client.request("GET", "/v1/karanas/" + uuid2, headers=header)
    resp = client.getresponse()
    assert resp.status < 300
    tmp = resp.read().decode('utf-8')
    results = json.loads(json.loads(tmp))
    password = results['results'][0][uuid2]['config']['password']
    assert wrapper.get_last_timepoint(uuid, 'config', uuid2, uuid2, password) \
           == '%influxcluster2.me-soldesign.com:443%data%' + \
              uuid + '%' + password + \
              '%10%30%6%'


def test_update_user():
    user_data = json.dumps({'data': '{"name":"Michael","role":"client"}'})
    client.request("PUT", "/v1/users/" + uuid, user_data, header)
    resp = client.getresponse()
    assert resp.status < 300
    user_data = json.dumps({'data': '{"name":"Michael G"}'})
    client.request("PUT", "/v1/users/" + uuid, user_data, header)
    resp = client.getresponse()
    assert resp.status > 300


def test_modify_user():
    user_data = json.dumps({'data': '{"name":"Michael Gtt"}'})
    client.request("PATCH", "/v1/users/" + uuid, user_data, header)
    resp = client.getresponse()
    assert resp.status < 300
    user_data = json.dumps({'data': '{"name":"Michael","email":"micha@all.de"}'})
    client.request("PATCH", "/v1/users/" + uuid, user_data, header)
    resp = client.getresponse()
    assert resp.status > 300


def test_get_created_user():
    client.request("GET", "/v1/users/" + uuid, headers=header)
    resp = client.getresponse()
    assert resp.status < 300


def test_remove_created_user_and_karana():
    client.request("DELETE", "/v1/users/" + uuid, headers=header)
    resp = client.getresponse()
    assert resp.status < 300
    client.request("DELETE", "/v1/karanas/" + uuid2, headers=header)
    resp = client.getresponse()
    assert resp.status < 300
    global pro
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)



