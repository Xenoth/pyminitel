from pyminitel.minitel import Minitel
from pyminitel.connector import get_connected_serial_minitel
from pyminitel.mode import Mode
from logging import *
import os


minitel = None


# minitel = get_connected_serial_minitel() # Serial comm
minitel = get_connected_serial_minitel(ip='0.0.0.0', port='8083') # TCP comm
if minitel is None:
    exit()

minitel.disableKeyboard()
minitel.clear()
minitel.setScreenPageMode()
minitel.setVideoMode(Mode.VIDEOTEX)
filepath = os.path.join('.', 'src', 'examples', 'ressources', 'PAGE_VGP5_.VDT')
if not os.path.exists(filepath):
    log(ERROR, "File not found: " + str(filepath))
    exit()
with open(filepath, 'rb') as binary_file:
    minitel.send(binary_file.read())
    binary_file.close()
minitel.beep()
minitel.getMinitelInfo()
del minitel