from pyminitel.minitel import Minitel, MinitelException
from pyminitel.mode import Mode
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.visualization_module import VisualizationModule
from logging import *
import time
minitel = None
for bauds in [Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_300]:
    try:
        minitel = Minitel(port='/dev/tty.usbserial-2', baudrate=bauds)
        break
    except MinitelException:
        log(ERROR, 'Minitel not connected on ' + str(bauds.to_int()) + ' bauds.')

if minitel is None:
    log(ERROR, 'Unable to fin appropriate baudrate for the minitel, exiting...')
    exit()

minitel.disableKeyboard()
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800,Minitel.Baudrate.BAUDS_4800)

minitel.clear()
minitel.send(Layout.setCursorPosition(1, 5))

minitel.setZoneAttributes(color=BackgroundColor.GREEN)
minitel.send(Layout.fillLine())
minitel.send(Layout.setCursorPosition(1, 20))

minitel.setZoneAttributes(color=BackgroundColor.CYAN)
minitel.send(Layout.fillLine())

minitel.send(Layout.setCursorPosition(1, 5))
minitel.setTextAttributes(color=CharacterColor.GREEN, inverted=True)
minitel.print("YIFF ME PLENTY.")
minitel.resetTextAttributes()

for i in range(22):
    minitel.send(Layout.setCursorPosition(i + 2, 2))
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)
    minitel.print('                                   ')


for i in range(20):
    minitel.send(Layout.setCursorPosition(i + 3, 3))
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)
    minitel.print('                                 ')
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)

for i in range(6):
    minitel.send(Layout.setCursorPosition(i + 4, 4))
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.print('                               ')
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)

for i in range(3):
    minitel.send(Layout.setCursorPosition(i + 19, 7))
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.print('                        ')
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)

minitel.send(Layout.setCursorPosition(6, 6))
minitel.setTextAttributes(double_height=True, double_width=True, color=CharacterColor.BLACK)
minitel.print("Merci pour")
minitel.send(Layout.setCursorPosition(8, 10))
minitel.print("la Vente!")

minitel.send(Layout.setCursorPosition(12, 4))
minitel.resetTextAttributes()
minitel.setTextAttributes(CharacterColor.WHITE)
minitel.send(Layout.setCursorPosition(14, 6))
msg = "Je vous remercie pour l'envoi"
for c in msg:
    minitel.din.write(ascii_to_alphanumerical(c, vm=VisualizationModule.VGP5))
minitel.send(Layout.setCursorPosition(15, 4))
msg = "soigné, et l'excellent état de"
for c in msg:
    minitel.din.write(ascii_to_alphanumerical(c, vm=VisualizationModule.VGP5))
minitel.send(Layout.setCursorPosition(16, 4))
msg = 'ce Minitel!'
for c in msg:
    minitel.din.write(ascii_to_alphanumerical(c, vm=VisualizationModule.VGP5))

minitel.setTextAttributes(CharacterColor.WHITE, blinking=True)
minitel.send(Layout.setCursorPosition(20, 12))
msg = 'Bonne journée!'
for c in msg:
    minitel.din.write(ascii_to_alphanumerical(c, vm=VisualizationModule.VGP5))

time.sleep(2)

minitel.setConnectorBaudrate()

