import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from influx import InfluxDBWrapper




################################## Tests for InfluxDBWrapper #############################
Wrapper = InfluxDBWrapper()


def test_influx1():
    assert Wrapper.create_db('testdb')

def test_influx2():
    assert Wrapper.insert_config('testdb', 'config', '123')
    assert Wrapper.get_config('testdb', '123') == 'config'

def test_influx3():
    assert Wrapper.create_user('testuser', 'testpw')
    assert not Wrapper.grant_privilege_user('testdb', 'testuse', 'all')
    assert Wrapper.grant_privilege_user('testdb', 'testuser', 'all')

def test_influx4():
    assert Wrapper.remove_db('testdb')
    assert Wrapper.remove_user('testuser')
    assert not Wrapper.remove_user('testuser')


