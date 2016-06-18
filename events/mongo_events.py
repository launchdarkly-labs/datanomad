from pymongo import MongoClient
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
def mongo_save_event(evt):
  _events_coll().insert_one(evt)
  return evt

@time_calls
def mongo_get_event_by_id(user_key, id):
  return _events_coll().find_one({'_id': id, 'user.key': user_key})
