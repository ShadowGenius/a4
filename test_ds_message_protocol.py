import ds_protocol

json = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'
extracted = ds_protocol.extract_json(json)
if isinstance(extracted.messages, list):
    print(extracted.messages)
print(extracted)