from pymongo import MongoClient
import uuid
from copy import copy
from pyformance import time_calls

client = None
coll = None

def initialize(mongo_uri):
  global client
  client = MongoClient(mongo_uri)

def _database():
  if client is None:
    print "ERROR: DB client is not initialized"
    return None
  else:
    return client['datanomad']

def _events_coll():
  db = _database()
  if db is None:
    return None
  else:
    return db['events']

@time_calls
def mongo_save_event(evt_in):
  """Inserts an event in the database, and returns the event with the generated id"""
  evt = copy(evt_in)
  evt['_id'] = str(uuid.uuid4())
  _events_coll().insert_one(evt)
  return evt

@time_calls
def mongo_get_event_by_id(user_key, id):
  return _events_coll().find_one({'_id': id, 'user.key': user_key})
