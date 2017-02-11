import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from influx import InfluxDBWrapper




################################## Tests for InfluxDBWrapper #############################
Wrapper = InfluxDBWrapper()


def test_influx_create_db():
    assert Wrapper.create_db('testdb')

def test_insert_as_admin():
    assert Wrapper.insert_timepoint('testdb', 'check', 'config', '123')
    assert Wrapper.get_last_timepoint('testdb', 'check', '123') == 'config'


def test_create_user():
    assert Wrapper.create_user('testuser', 'testpw')
    assert not Wrapper.grant_privilege_user('testdb', 'testuse', 'all')
    assert Wrapper.grant_privilege_user('testdb', 'testuser', 'all')


def test_inser_as_user():
    assert Wrapper.insert_timepoint('testdb', 'check', 'config', '123', 'testuser', 'testpw')
    assert not Wrapper.insert_timepoint('testdb', 'check', 'config', '123', 'testuser', 'testp')
    assert Wrapper.get_last_timepoint('testdb', 'check', '123', 'testuser', 'testpw') == 'config'
    assert not Wrapper.get_last_timepoint('testdb', 'check', '123', 'testuser', 'testp') == 'config'


def test_remove_all():
    assert Wrapper.remove_db('testdb')
    assert Wrapper.remove_user('testuser')
    assert not Wrapper.remove_user('testuser')


