'''Module for testing ds_protocol.py'''

import ds_protocol

def test_ds_protocol():
    '''Function for testing ds_protocol.py'''
    # Send a directmessage to another DS user (in the example bellow, ohhimark)
    json = '''{"token":"user_token",
               "directmessage": {"entry": "Hello World!",
                                 "recipient":"ohhimark", 
                                 "timestamp": "1603167689.3928561"}}'''
    extracted = ds_protocol.extract_json(json)
    assert extracted.token == 'user_token'
    assert extracted.entry == "Hello World!"
    assert extracted.recipient == "ohhimark"
    assert extracted.timestamp == "1603167689.3928561"

    # Request unread messages from the DS server
    json = '''{"token":"user_token", "directmessage": "new"}'''
    extracted = ds_protocol.extract_json(json)
    assert extracted.token == 'user_token'
    assert extracted.directmessage == "new"

    # Request all messages from the DS server
    json = '''{"token":"user_token", "directmessage": "all"}'''
    extracted = ds_protocol.extract_json(json)
    assert extracted.token == 'user_token'
    assert extracted.directmessage == "all"

    # Sending of direct message was successful
    json = '''{"response": {"type": "ok", "message": "Direct message sent"}}'''
    extracted = ds_protocol.extract_json(json)
    assert extracted.type == 'ok'
    assert extracted.message == "Direct message sent"

    # Response to request for **`all`** and **`new`** messages. Timestamp is time in seconds
    # of when the message was originally sent.
    json = '''{"response": {"type": "ok",
                            "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},
                                         {"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}
                                         ]}}'''
    extracted = ds_protocol.extract_json(json)
    assert extracted.type == 'ok'
    assert isinstance(extracted.messages, list)
