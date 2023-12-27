# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8082  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(3)
    if data == b'\x1b\x39\x7b':
        print('Got Request Minitel Info')
        s.send(b'\x01\x43\x75\x3c\x04')
    else:
        print('unknown command - leaving...')
