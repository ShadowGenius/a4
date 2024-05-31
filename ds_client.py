# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# William Lay
# laywc@uci.edu
# 67168820

import socket
import json
from Profile import Post
import ds_protocol

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((server, port))

            sent = client.makefile('w')
            recv = client.makefile('r')

            recv_msg = join_sever(username, password, sent, recv)

            if recv_msg.type == 'ok':

                token = recv_msg.token

                recv_msg = send_post(message, sent, recv, token)

                if bio:
                    send_bio(bio, sent, recv, token)

                return True
        except socket.gaierror:
            print("ERROR: Server address invalid.")

        return False

def send_bio(bio, sent, recv, token):
    '''Sends the server the bio the user wants to create or update.'''
    bio_msg = f'{{"token":"{token}", "bio": {{"entry": "{bio}","timestamp": ""}}}}'
    return send_and_recv(sent, recv, bio_msg)

def send_post(message, sent, recv, token):
    '''Constructs and sends the server the post the user wants to send.'''
    new_post = Post(message)
    new_post = json.dumps(new_post)
    post_msg = f'{{"token":"{token}", "post": {new_post}}}'
    return send_and_recv(sent, recv, post_msg)

def join_sever(username, password, sent, recv):
    '''Sends the server the join message.'''
    join_msg = f'''{{"join": {{"username": "{username}",
                                "password": "{password}",
                                "token":""}}}}'''
    return send_and_recv(sent, recv, join_msg)

def send_and_recv(sent, recv, msg_to_send):
    """Sends a message to the connected server and returns the server's response."""
    sent.write(msg_to_send + '\r\n')
    sent.flush()

    resp = recv.readline()
    recv_msg = ds_protocol.extract_json(resp)
    print(recv_msg.message)
    return recv_msg
