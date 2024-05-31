# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# William Lay
# laywc@uci.edu
# 67168820

import json
from collections import namedtuple

LIST_OF_KEYS = ['join', 'post', 'response', 'directmessage']
LIST_OF_SUBKEYS = ['username', 'password', 'token', 'entry', 'timestamp', 'type', 'message', 'directmessage', 'recipient', 'messages']

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', LIST_OF_SUBKEYS)

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    try:
        usr, pwd, token, entry, timestamp, resp_type, msg, dm, rcp, msgs = (['' for i in LIST_OF_SUBKEYS])
        json_obj = json.loads(json_msg)

        for key in json_obj:
            if key == 'token':
                token = json_obj[key]
            elif key == 'directmessage' and json_obj[key] in ["new", "all"]:
                dm = json_obj[key]
            elif key in LIST_OF_KEYS:
                for subkey in json_obj[key]:
                    value = json_obj[key][subkey]
                    match subkey:
                        case 'username':
                            usr = value
                        case 'password':
                            pwd = value
                        case 'token':
                            token = value
                        case 'entry':
                            entry = value
                        case 'timestamp':
                            timestamp = value
                        case 'type':
                            resp_type = value
                        case 'message':
                            msg = value
                        case 'recipient':
                            rcp = value
                        case 'messages':
                            msgs = value
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(usr, pwd, token, entry, timestamp, resp_type, msg, dm, rcp, msgs)
