from pyminitel.minitel import Minitel, MinitelException
from pyminitel.mode import Mode
from pyminitel.layout import Layout
from pyminitel.attributes import *
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
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_4800)
minitel.clear()

msg = "   __  _______ ________________"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "  / / / / ___// ___/ ____/ ___/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = " / / / /\\__ \\/ /   \\ __ \\\\__ \\ "
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "/ /_/ /___/ / /___ ___/ /__/ /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "\\____//____/\\____//____/____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorDown(1))
msg = "    _   ______  ___________"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "   / | / / __ \\/ ___/_  __/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "  /  |/ / / / /\\__ \\ / /_____"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = " / /|  / /_/ /___/ // //____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "/_/ |_/\\____//____//_/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorDown(1))
minitel.send(Layout.moveCursorRight(10))
msg = "    ____  ____  __  _______"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "   / __ \\/ __ \\/  |/  / __ \\"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "  / /_/ / / / / /|_/ / / / /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = " / _, _/ /_/ / /  / / /_/ /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "/_/ |_|\\____/_/  /_/\\____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorDown(2))

minitel.setZoneAttributes(color=BackgroundColor.BLUE)
minitel.send(Layout.fillLine())
minitel.send(Layout.cariageReturn())
minitel.send(Layout.moveCursorDown())
msg = "/// WEYLAND-YUTANI CORPORATION \\\\\\ "


minitel.setZoneAttributes(color=BackgroundColor.RED)
minitel.send(Layout.fillLine())

minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
minitel.setZoneAttributes(color= BackgroundColor.WHITE)
minitel.send(Layout.moveCursorRight(1))
minitel.print(msg)
minitel.resetTextAttributes()
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
minitel.hideCursor()
minitel.beep()
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_1200)
time.sleep(5)