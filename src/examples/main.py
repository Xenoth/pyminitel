from pyminitel.minitel import Minitel
from pyminitel.layout import Layout
from pyminitel.attributs import *

import time

minitel = Minitel(port='/dev/tty.usbserial-2')

minitel.layout.clear()
# minitel.setScreenPageMode()
minitel.setScreenRollMode()

while 0:

    minitel.setZoneAttributes(color=BackgroundColor.BLACK)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
    minitel.layoutfillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.CYAN)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.WHITE)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.CYAN)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.GREEN)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.RED)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()
    minitel.setZoneAttributes(color=BackgroundColor.BLUE)
    minitel.layout.fillLine()
    minitel.layout.cariageReturn()
    minitel.layout.moveCursorDown()

minitel.Beep()

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
minitel.layout.moveCursorDown(3)
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
minitel.layout.moveCursorDown(1)
minitel.layout.oveCursorRight(10)
msg = "    ____  ____  __  _______"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.layout.moveCursorRight(10)
msg = "   / __ \\/ __ \\/  |/  / __ \\"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.layout.moveCursorRight(10)
msg = "  / /_/ / / / / /|_/ / / / /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.layout.moveCursorRight(10)
msg = " / _, _/ /_/ / /  / / /_/ /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.layout.moveCursorRight(10)
msg = "/_/ |_|\\____/_/  /_/\\____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
minitel.layout.moveCursorDown(3)
minitel.layout.moveCursorRight(3)

msg = "/// WEYLAND-YUTANI CORPORATION \\\\\\"

minitel.setTextAttributes(blinking=True)
minitel.print(msg)
minitel.Beep()

time.sleep(10)




# r, c = minitel.getCursorPosition()
# print("cursor info: r=" + str(r) + " c=" + str(c))

# res = minitel.getModuleIOStatus(Minitel.Module.CONNECTOR, Minitel.IO.IN)
# print("res: "+ res)