from pyminitel.minitel import Minitel
from pyminitel.layout import Layout
from pyminitel.attributs import *

import time

minitel = Minitel(port='/dev/tty.usbserial-2')
l = Layout(minitel.din)

minitel.layout.Clear()
msg = "   ________________"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "  / ____/ ___/ ____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = " / /    \\__ \\\\__ \\"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "/ /___ ___/ /__/ /"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "\\____//____/____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()

msg = "    __  ___ ___   ____   _   __ __ ____"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "   /  |/  //   | / __ \\ / | / // // __/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "  / /|_/ // /| |/ /_/ //  |/ // // _/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = " / /  / // /_| / _, _// /|  // // /__"
minitel.print(break_word=True, text=msg)
minitel.newLine()
msg = "/_/  /_//_/  |/_/ |_|/_/ |_//_//____/"
minitel.print(break_word=True, text=msg)
minitel.newLine()
l.MoveCursorDown(4)
l.MoveCursorRight(5)

minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
minitel.setZoneAttributes(BackgroundColor.WHITE, masking=False)
msg = "/// HIRAGINI CORPORATION \\\\\\ "
minitel.print(msg)
minitel.setZoneAttributes(color=BackgroundColor.BLACK)
minitel.resetTextAttributes()
minitel.newLine()
l.MoveCursorDown(3)

minitel.setZoneAttributes(color=BackgroundColor.BLACK, highlight=True)
msg = "[MOTHER]"
minitel.print(msg)
minitel.setZoneAttributes(highlight=False)
msg = "- Good Morning, Lieutenant."
minitel.print(msg)
minitel.newLine()
l.MoveCursorDown(2)
msg = "XENOTH_VAL[Lieut.]$> "
minitel.print(msg)

minitel.showCursor()

minitel.Beep()

time.sleep(10)