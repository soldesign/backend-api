import os
import sys
import json

# import http.client
# import base64
# from log import log
import logging
import subprocess

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from influx import DBHTTPSetup
# from seed import user1
command = ['bash', './run.sh']
# process = subprocess.Popen(command)
# process.wait(timeout=None)
TestHTTP = DBHTTPSetup(db='test')
client = TestHTTP.__conn_setup__(ssl=False)
header = TestHTTP.__get_header__(content_type="application/json")

# http://127.0.0.1:8000/v1/users/new body='{"name":"Micha","role":"admin","email":"mica@all.de"}'


def test_create_user_and_karana():
    userdict = {'data': '{"name":"Micha","role":"admin","email":"mic@all.de"}'}
    user = json.dumps(userdict)
    client.request("POST", "/v1/users/new/", user, header)
    resp = client.getresponse()
    assert resp.status < 300
    tmp = resp.read().decode('utf-8')
    results = json.loads(json.loads(tmp))
    karanadict = {'data': '{"name":"Karana","owner":"' + results['results']['uuid'] + '"}'}
    karana = json.dumps(karanadict)
    print(karana)
    client.request("POST", "/v1/karanas/new/", karana, header)
    resp = client.getresponse()
    assert resp.status < 300


