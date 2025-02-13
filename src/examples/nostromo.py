import sys

from pyminitel.connector import get_connected_serial_minitel
from pyminitel.layout import Layout
from pyminitel.attributes import CharacterColor, BackgroundColor

def main():
    minitel = None

    minitel = get_connected_serial_minitel()
    if minitel is None:
        sys.exit()

    minitel.disable_keyboard()
    minitel.clear()

    msg = "   __  _______ ________________"
    minitel.print(text=msg)
    minitel.new_line()
    msg = "  / / / / ___// ___/ ____/ ___/"
    minitel.print(text=msg)
    minitel.new_line()
    msg = " / / / /\\__ \\/ /   \\ __ \\\\__ \\ "
    minitel.print(text=msg)
    minitel.new_line()
    msg = "/ /_/ /___/ / /___ ___/ /__/ /"
    minitel.print(text=msg)
    minitel.new_line()
    msg = "\\____//____/\\____//____/____/"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_down(1))
    msg = "    _   ______  ___________"
    minitel.print(text=msg)
    minitel.new_line()
    msg = "   / | / / __ \\/ ___/_  __/"
    minitel.print(text=msg)
    minitel.new_line()
    msg = "  /  |/ / / / /\\__ \\ / /_____"
    minitel.print(text=msg)
    minitel.new_line()
    msg = " / /|  / /_/ /___/ // //____/"
    minitel.print(text=msg)
    minitel.new_line()
    msg = "/_/ |_/\\____//____//_/"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_down(1))
    minitel.send(Layout.move_cursor_right(10))
    msg = "    ____  ____  __  _______"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_right(10))
    msg = "   / __ \\/ __ \\/  |/  / __ \\"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_right(10))
    msg = "  / /_/ / / / / /|_/ / / / /"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_right(10))
    msg = " / _, _/ /_/ / /  / / /_/ /"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_right(10))
    msg = "/_/ |_|\\____/_/  /_/\\____/"
    minitel.print(text=msg)
    minitel.new_line()
    minitel.send(Layout.move_cursor_down(2))

    minitel.set_zone_attributes(color=BackgroundColor.BLUE)
    minitel.send(Layout.fill_line())
    minitel.send(Layout.cariage_return())
    minitel.send(Layout.move_cursor_down())
    msg = "/// WEYLAND-YUTANI CORPORATION \\\\\\ "


    minitel.set_zone_attributes(color=BackgroundColor.RED)
    minitel.send(Layout.fill_line())

    minitel.set_text_attributes(blinking=True, color=CharacterColor.BLACK)
    minitel.set_zone_attributes(color= BackgroundColor.WHITE)
    minitel.send(Layout.move_cursor_right(1))
    minitel.print(msg)
    minitel.reset_text_attributes()
    minitel.set_zone_attributes(color=BackgroundColor.RED)
    minitel.send(Layout.fill_line())
    minitel.send(Layout.cariage_return())
    minitel.send(Layout.move_cursor_down())
    minitel.set_zone_attributes(color=BackgroundColor.MAGENTA)
    minitel.send(Layout.fill_line())
    minitel.send(Layout.cariage_return())
    minitel.send(Layout.move_cursor_down())
    minitel.set_zone_attributes(color=BackgroundColor.GREEN)
    minitel.send(Layout.fill_line())
    minitel.send(Layout.cariage_return())
    minitel.send(Layout.move_cursor_down())
    minitel.set_zone_attributes(color=BackgroundColor.CYAN)
    minitel.send(Layout.fill_line())
    minitel.hide_cursor()
    minitel.beep()
    minitel.get_minitel_info()

if __name__ == '__main__':
    sys.exit(main())
