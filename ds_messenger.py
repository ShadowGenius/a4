import json, socket, time
from ds_client import send_and_recv

PORT = 3021

class DirectMessage(dict):
    def __init__(self, recipient, message, timestamp = 0):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        if self.timestamp == 0:
            self.timestamp = time.time()
        dict.__init__(self, entry=self.message, recipient=self.recipient, timestamp=self.timestamp)

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.sent, self.recv, self.token = join_server(dsuserver, username, password)

    def send(self, message:str, recipient:str) -> bool:
        ''' returns true if message successfully sent, false if send failed. '''
        new_dm = DirectMessage(recipient, message)
        new_dm = json.dumps(new_dm)
        post_msg = f'{{"token":"{self.token}", "directmessage": {new_dm}}}'
        recv_msg = send_and_recv(self.sent, self.recv, post_msg)
        if recv_msg.type == "ok":
            return True
        return False

    def retrieve_new(self) -> list:
        ''' returns a list of DirectMessage objects containing all new messages '''
        retrieve_msg = f'{{"token":"{self.token}", "directmessage": "new"}}'
        return self.retrieve(retrieve_msg)

    def retrieve_all(self) -> list:
        ''' returns a list of DirectMessage objects containing all messages'''
        retrieve_msg = f'{{"token":"{self.token}", "directmessage": "all"}}'
        return self.retrieve(retrieve_msg)

    def retrieve(self, retrieve_msg):
        ''' returns a list of DirectMessage objects as specified '''
        recv_msg = send_and_recv(self.sent, self.recv, retrieve_msg)
        dm_list = []
        if recv_msg.type == "ok" and isinstance(recv_msg.messages, list):
            for msg in recv_msg.messages:
                dm = DirectMessage(msg["from"], msg["message"], msg["timestamp"])
                dm_list.append(dm)
        return dm_list

def join_server(dsuserver, username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sent, recv, token = (None, None, None)
    try:
        client.connect((dsuserver, PORT))

        sent = client.makefile('w')
        recv = client.makefile('r')

        join_msg = f'''{{"join": {{"username": "{username}",
                                    "password": "{password}",
                                    "token":""}}}}'''
        recv_msg = send_and_recv(sent, recv, join_msg)

        if recv_msg.type == 'ok':
            token = recv_msg.token

    except socket.gaierror:
        print("ERROR: Server address invalid.")
    return sent, recv, token
