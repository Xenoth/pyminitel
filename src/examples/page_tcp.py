import os
import sys

from logging import log, ERROR

from pyminitel.connector import get_connected_socket_minitel
from pyminitel.mode import Mode

def main():
    minitel = None

    minitel = get_connected_socket_minitel(host='0.0.0.0', port='8083')
    if minitel is None:
        sys.exit()

    minitel.disable_keyboard()
    minitel.clear()
    minitel.set_screen_page_mode()
    minitel.set_video_mode(Mode.VIDEOTEX)
    filepath = os.path.join('.', 'src', 'examples', 'resources', 'HELLDIVERS_SG.VDT')
    if not os.path.exists(filepath):
        log(ERROR, "File not found: " + str(filepath))
        sys.exit()
    with open(filepath, 'rb') as binary_file:
        minitel.send(binary_file.read())
        binary_file.close()
    minitel.beep()
    minitel.get_minitel_info()

if __name__ == '__main__':
    sys.exit(main())
