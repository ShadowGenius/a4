import json, socket, time
import ds_protocol
#from ds_client import send_and_recv

PORT = 3021

class DirectMessage(dict):
    def __init__(self, recipient, message, timestamp = 0, sender = None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        self.sender = sender
        if self.timestamp == 0:
            self.timestamp = time.time()
        dict.__init__(self, entry=self.message,
                      recipient=self.recipient,
                      timestamp=self.timestamp,
                      sender=self.sender)

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.dms_out = []
        if self.dsuserver is None:
            self.sent = None
            self.recv = None
            self.token = None
        else:
            self.sent, self.recv, self.token = join_server(self.dsuserver, self.username, self.password)
    
    def get_token(self):
        self.sent, self.recv, self.token = join_server(self.dsuserver, self.username, self.password)

    def send(self, message:str, recipient:str) -> bool:
        ''' returns true if message successfully sent, false if send failed. '''
        if self.sent and self.recv:
            new_dm = DirectMessage(recipient, message, 0, self.username)
            self.dms_out.append(new_dm)
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
        dm_list = []
        if self.sent and self.recv:
            recv_msg = send_and_recv(self.sent, self.recv, retrieve_msg)
            if recv_msg.type == "ok" and isinstance(recv_msg.messages, list):
                for msg in recv_msg.messages:
                    dm = DirectMessage(self.username, msg["message"], msg["timestamp"], msg["from"])
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
    except OSError:
        print("ERROR: No internet")
    return sent, recv, token

def send_and_recv(sent, recv, msg_to_send):
    """Sends a message to the connected server and returns the server's response."""
    sent.write(msg_to_send + '\r\n')
    sent.flush()

    resp = recv.readline()
    recv_msg = ds_protocol.extract_json(resp)
    if recv_msg.message:
        print(recv_msg.message)
    return recv_msg
