import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))
from synch  import SynchInflux


################################## Tests for SynchInflux #############################
Synch = SynchInflux()


def test_user_synch():
    assert not Synch.check_user_read('abcdef', 'pw1234')
    assert Synch.register_user('abcdef', 'pw1234')
    assert Synch.check_user_read('abcdef', 'pw1234')
    assert Synch.remove_user('abcdef')