import boto3
from botocore.exceptions import ClientError
from pyformance import time_calls
from random import random
import uuid
from copy import copy

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

table = dynamodb.Table('nomad_events')
try:
  table.item_count
except ClientError as e:
  # if the table doesn't exist, create it
  error_code = e.response['Error']['Code']
  if error_code == 'ResourceNotFoundException':
    table = dynamodb.create_table(
      TableName='nomad_events',
      KeySchema=[
        {
            'AttributeName': '_id',
            'KeyType': 'HASH'
        }
      ],
      AttributeDefinitions=[
        {
            'AttributeName': '_id',
            'AttributeType': 'S'
        }

      ],
      ProvisionedThroughput={
        'ReadCapacityUnits': 75,
        'WriteCapacityUnits': 75
      }
    )
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='nomad_events')


@time_calls
def dynamo_save_event(evt_in):
  evt = copy(evt_in)
  evt['_id'] = str(uuid.uuid4())
  table.put_item(Item=evt)
  return evt

@time_calls
def dynamo_get_event_by_id(user_key, id):
  response = table.get_item(Key={'_id': id})
  ret = response.get('Item')
  if ret and ret['user']['key'] == user_key:
    return ret
  else:
    return None