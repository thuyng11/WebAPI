# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object

  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj.get('response').get('type', None)
    message = json_obj.get('response').get('message', None)
    token = json_obj.get('response').get('token', None)
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return [DataTuple(type, message, token), token]
