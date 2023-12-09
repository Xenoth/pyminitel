from pyminitel.minitel import Minitel
from pyminitel.mode import Mode
from pyminitel.attributes import *

import time

minitel = Minitel(port='/dev/tty.usbserial-2', mode=Mode.VIDEOTEX, bauderate=Minitel.Bauderate.BAUDS_1200)
minitel.setConnectorBauderate(Minitel.Bauderate.BAUDS_4800, Minitel.Bauderate.BAUDS_4800)
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
minitel.layout.moveCursorDown(1)
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
minitel.layout.moveCursorRight(10)
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
minitel.layout.moveCursorDown(2)

minitel.setZoneAttributes(color=BackgroundColor.BLUE)
minitel.layout.fillLine()
minitel.layout.cariageReturn()
minitel.layout.moveCursorDown()
msg = "/// WEYLAND-YUTANI CORPORATION \\\\\\ "


minitel.setZoneAttributes(color=BackgroundColor.RED)
minitel.layout.fillLine()

minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
minitel.setZoneAttributes(color= BackgroundColor.WHITE)
minitel.layout.moveCursorRight(1)
minitel.print(msg)
minitel.resetTextAttributes()
minitel.setZoneAttributes(color=BackgroundColor.RED)
minitel.layout.fillLine()
minitel.layout.cariageReturn()
minitel.layout.moveCursorDown()
minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
minitel.layout.fillLine()
minitel.layout.cariageReturn()
minitel.layout.moveCursorDown()
minitel.setZoneAttributes(color=BackgroundColor.GREEN)
minitel.layout.fillLine()
minitel.layout.cariageReturn()
minitel.layout.moveCursorDown()
minitel.setZoneAttributes(color=BackgroundColor.CYAN)
minitel.layout.fillLine()
minitel.hideCursor()
minitel.Beep()
minitel.setConnectorBauderate(Minitel.Bauderate.BAUDS_1200, Minitel.Bauderate.BAUDS_1200)
time.sleep(5)