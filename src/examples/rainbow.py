from pyminitel.minitel import Minitel
from pyminitel.attributes import BackgroundColor, ZoneAttributesState
from pyminitel.layout import Layout
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.page import Page

class RainbowPage(Page):
    def __init__(self, minitel=...) -> None:
        super().__init__(minitel)

    def callback_quit(self) -> None:
        self.minitel.get_minitel_info()
        self.stop()

    def callback_beep(self) -> None:
        self.minitel.beep()

    def run(self) -> None:
        self.minitel.disable_keyboard()
        self.minitel.set_connector_baudrate(
            Minitel.ConnectorBaudrate.BAUDS_4800,
            Minitel.ConnectorBaudrate.BAUDS_4800
        )
        self.minitel.set_screen_roll_mode()
        self.minitel.new_line()

        self.minitel.bind(FunctionKeyboardCode.SUMMARY, callback=self.callback_quit)
        self.minitel.bind(FilterKeyboardCode.ANY_KEYS, callback=self.callback_beep)
        self.minitel.enable_keyboard()

        while not self.stopped():
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.BLACK))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.BLUE))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.RED))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.MAGENTA))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.GREEN))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.CYAN))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.YELLOW))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.WHITE))
            self.minitel.read_keyboard(.1)
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.YELLOW))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.CYAN))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.GREEN))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.MAGENTA))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.RED))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.BLUE))
            self.minitel.send(Layout.fill_line())
            self.minitel.send(Layout.carriage_return())
            self.minitel.send(Layout.move_cursor_down())
            self.minitel.read_keyboard(.1)
