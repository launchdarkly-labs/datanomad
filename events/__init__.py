import os
import simplejson as json
import uuid
from copy import copy
from ldclient import LDClient
from .mongo_events import mongo_save_event, mongo_get_event_by_id
from .dynamo_events import dynamo_save_event, dynamo_get_event_by_id


ld_client = LDClient(os.getenv('LD_SDK_KEY'))

def save_event(evt_in):
  """Inserts an event in the database, and returns the event with the generated id"""
  evt = copy(evt_in)
  evt['_id'] = str(uuid.uuid4())
  mongo_evt = None
  dynamo_evt = None
  if ld_client.variation('write-events-mongo', evt['user'], True):
    mongo_evt = mongo_save_event(evt)
  if ld_client.variation('write-events-dynamo', evt['user'], False):
    dynamo_evt = dynamo_save_event(evt)
  return mongo_evt or dynamo_evt

def get_event_by_id(user_key, id):
  read_mongo = ld_client.variation('read-events-mongo', {'key': user_key}, True)
  read_dynamo = ld_client.variation('read-events-dynamo', {'key': user_key}, False)
  mongo_evt = None
  dynamo_evt = None
  if read_mongo:
    mongo_evt = mongo_get_event_by_id(user_key, id)
  if read_dynamo:
    dynamo_evt = dynamo_get_event_by_id(user_key, id)
  if read_mongo and read_dynamo: # if both read flags are on, compare the results
    if mongo_evt != dynamo_evt:
      print "ERROR: Events do not match from mongo & dynamo. mongo: {}, dynamo: {}".format(json.dumps(mongo_evt), json.dumps(dynamo_evt))
  return mongo_evt or dynamo_evt