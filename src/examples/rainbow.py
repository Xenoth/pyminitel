from pyminitel.minitel import Minitel, MinitelException
from pyminitel.attributes import *
from pyminitel.layout import Layout

from logging import *

minitel = None
for bauds in [Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_300]:
    try:
        minitel = Minitel(port='/dev/tty.usbserial-3', baudrate=bauds)
        break
    except MinitelException:
        log(ERROR, 'Minitel not connected on ' + str(bauds.to_int()) + ' bauds.')

if minitel is None:
    log(ERROR, 'Unable to fin appropriate baudrate for the minitel, exiting...')
    exit()

minitel.disableKeyboard()
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_4800)
minitel.setScreenRollMode()
minitel.newLine()

minitel.beep()

while 1:
    minitel.setZoneAttributes(color=BackgroundColor.BLACK)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.CYAN)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.WHITE)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.CYAN)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)
    minitel.send(Layout.fillLine())
    minitel.send(Layout.cariageReturn())
    minitel.send(Layout.moveCursorDown())
