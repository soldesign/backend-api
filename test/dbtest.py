import os
import sys

# import http.client
# import base64
# from log import log
import logging
import subprocess

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from influx import DBHTTPSetup
# from seed import user1
body = '{"name":"Micha","role":"admin","email":"mica@all.de"}'
command = ['bash', './run.sh']
# process = subprocess.Popen(command)
# process.wait(timeout=None)
TestHTTP = DBHTTPSetup(db='test')
client = TestHTTP.__conn_setup__(ssl=False)
header = TestHTTP.__get_header__(content_type="application/json")

# http://127.0.0.1:8000/v1/users/new body='{"name":"Micha","role":"admin","email":"mica@all.de"}'

def test1():
    client.request("POST", "/v1/users/new/", body, header)
    resp = client.getresponse()
    assert resp.status < 300
