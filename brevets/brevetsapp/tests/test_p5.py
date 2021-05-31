from acp_times import open_time, close_time
import flask_brevets
from flask_brevets import insert
from flask_brevets import client
from flask_brevets import db
import nose
import logging
from pymongo import MongoClient
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_insert():
    db.controls.delete_many({})
    db.controls.insert({'km':100, 'open': '2021-01-01T02:56', 'close': '2021-01-01T06:40', 'test': 'yes'})
    assert db.controls.find_one({'km':100, 'test':'yes'}) != None
    db.controls.delete_many({})
    assert db.controls.find_one({'km':100, 'test':'yes'}) == None

def test_calc_open():
    assert open_time(100,200,'2021-01-01T00:00').format('YYYY-MM-DDTHH:mm') == '2021-01-01T02:56'
def test_calc_close():
    assert close_time(300,600,'2021-01-01T00:00').format('YYYY-MM-DDTHH:mm') == '2021-01-01T20:00'

