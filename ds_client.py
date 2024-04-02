# THUY NGUYEN
# THUYN18
# 10087312

import socket
import json
from ds_protocol import extract_json
import time


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None):
    """
    The send function joins a ds server and sends a message, bio, or both.

    :param server: The IP address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.connect((server, port))

            join_msg = '{"join": {"username": "' + username + '", "password": "' + password + '", "token": ""}}'
            send = srv.makefile('w')
            recv = srv.makefile('r')

            send.write(join_msg + '\r\n')
            send.flush()

            resp = recv.readline()
            print('\nResponse from server: ',
                  json.loads(resp)['response']['message'])

            response_tuple = extract_json(resp)[0]

            if bio:
                bio_msg = '{"token": "' + response_tuple.token + '", "bio": {"entry": "' + bio + '", "timestamp": ' + str(int(time.time())) + '}}'
                send.write(bio_msg + '\r\n')
                send.flush()

                resp = recv.readline()

                response_tuple2 = extract_json(resp)[0]

                if response_tuple2.type == 'error':
                    print(response_tuple.message)
                    return False
                elif response_tuple2.type == 'ok':
                    print("\nResponses from server: ",
                          json.loads(resp)['response']['message'])

            if message:
                post_msg = '{"token": "' + response_tuple.token + '", "post": {"entry": "' + message + '", "timestamp": ' + str(int(time.time())) + '}}'
                send.write(post_msg + '\r\n')
                send.flush()

                resp = recv.readline()

                response_tuple3 = extract_json(resp)[0]

                if response_tuple3.type == 'error':
                    print(response_tuple.message)
                    return False
                elif response_tuple3.type == 'ok':
                    print("\nResponse from server: ",
                          json.loads(resp)['response']['message'])

            return True

    except Exception as e:
        print('An error occurred: ', str(e))
        return False


# Uncomment and replace with actual server IP address and port for testing
# server = "168.235.86.101"
# port = 3021
# send(server, port, "your_username", "your_password",
# "Your message", "Your bio")
