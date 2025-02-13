from pyminitel.minitel import Minitel
from pyminitel.attributes import BackgroundColor
from pyminitel.layout import Layout
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.page import Page

class RainbowPage(Page):

    def __init__(self, minitel=...) -> None:
        super().__init__(minitel)

    def callback_quit(self):
        self.minitel.get_minitel_info()
        self.stop()

    def callback_beep(self):
        self.minitel.beep()

    def run(self):
        self.minitel.disable_keyboard()
        self.minitel.set_connector_baudrate(
            Minitel.ConnectorBaudrate.BAUDS_4800,
            Minitel.ConnectorBaudrate.BAUDS_4800
        )
        self.minitel.set_screen_roll_mode()
        self.minitel.new_line()

        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_beep)
        self.minitel.enable_keyboard()

        while not self.stopped():
            self.minitel.set_zone_attributes(color=BackgroundColor.BLACK)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.BLUE)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.RED)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.MAGENTA)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.GREEN)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.CYAN)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.YELLOW)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.WHITE)
            self.minitel.read_keyboard(.1)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.YELLOW)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.CYAN)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.GREEN)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.MAGENTA)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.RED)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(color=BackgroundColor.BLUE)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.cariage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.read_keyboard(.1)

