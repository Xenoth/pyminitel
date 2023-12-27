from pyminitel.minitel import Minitel
from pyminitel.connector import get_connected_serial_minitel
from pyminitel.layout import Layout
from pyminitel.attributes import CharacterColor, BackgroundColor

minitel = None

minitel = get_connected_serial_minitel()
if minitel is None:
    exit()

minitel.disableKeyboard()
minitel.clear()

msg = "   __  _______ ________________"
minitel.print(text=msg)
minitel.newLine()
msg = "  / / / / ___// ___/ ____/ ___/"
minitel.print(text=msg)
minitel.newLine()
msg = " / / / /\\__ \\/ /   \\ __ \\\\__ \\ "
minitel.print(text=msg)
minitel.newLine()
msg = "/ /_/ /___/ / /___ ___/ /__/ /"
minitel.print(text=msg)
minitel.newLine()
msg = "\\____//____/\\____//____/____/"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorDown(1))
msg = "    _   ______  ___________"
minitel.print(text=msg)
minitel.newLine()
msg = "   / | / / __ \\/ ___/_  __/"
minitel.print(text=msg)
minitel.newLine()
msg = "  /  |/ / / / /\\__ \\ / /_____"
minitel.print(text=msg)
minitel.newLine()
msg = " / /|  / /_/ /___/ // //____/"
minitel.print(text=msg)
minitel.newLine()
msg = "/_/ |_/\\____//____//_/"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorDown(1))
minitel.send(Layout.moveCursorRight(10))
msg = "    ____  ____  __  _______"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "   / __ \\/ __ \\/  |/  / __ \\"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "  / /_/ / / / / /|_/ / / / /"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = " / _, _/ /_/ / /  / / /_/ /"
minitel.print(text=msg)
minitel.newLine()
minitel.send(Layout.moveCursorRight(10))
msg = "/_/ |_|\\____/_/  /_/\\____/"
minitel.print(text=msg)
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
minitel.getMinitelInfo()
del minitel