import os
import sys
import socket

from typing import Final

HOST: Final[str] = "xenoth.fr"  # The server's hostname or IP address
PORT: Final[int] = 8083  # The port used by the server

def main() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.settimeout(10)
        data = b''
        try:
            data = s.recv(3)
        except ConnectionResetError as e:
            print(str(e))
        if data == b'\x1b\x39\x7b':
            print('Got Request Minitel Info')
            s.send(b'\x01\x43\x75\x3c\x04')
        else:
            print('unknown command - leaving...')

    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main())
