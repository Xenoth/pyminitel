import os
import sys

from logging import log, ERROR

from pyminitel.connector import get_connected_socket_minitel, MinitelNotFoundException
from pyminitel.mode import Mode
from pyminitel.minitel import Minitel

def main() -> int:
    try:
        minitel: Minitel = get_connected_socket_minitel(host='0.0.0.0', port='8083')
    except MinitelNotFoundException:
        return os.EX_PROTOCOL

    minitel.disable_keyboard()
    minitel.clear()
    minitel.set_screen_page_mode()
    minitel.set_video_mode(Mode.VIDEOTEX)

    filepath = os.path.join('.', 'src', 'examples', 'resources', 'HELLDIVERS_SG.VDT')
    if not os.path.exists(filepath):
        log(ERROR, "File not found: " + str(filepath))
        return os.EX_NOINPUT

    with open(filepath, 'rb') as binary_file:
        minitel.send(binary_file.read())
        binary_file.close()

    minitel.beep()
    minitel.get_minitel_info()

    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main())
