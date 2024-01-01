from pyminitel.minitel import Minitel
from pyminitel.attributes import BackgroundColor
from pyminitel.layout import Layout
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.page import Page

from logging import log, ERROR

class RainbowPage(Page):

    def __init__(self, minitel=...) -> None:
        super().__init__(minitel)

    def callback_quit(self):
        self.minitel.getMinitelInfo()
        self.stop()

    def callback_beep(self):
        self.minitel.beep()

    def run(self):
        self.minitel.disableKeyboard()
        self.minitel.setConnectorBaudrate(Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800)
        self.minitel.setScreenRollMode()
        self.minitel.newLine()

        self.minitel.bind(FunctionKeyboardCode.TS_Connection_Switch, callback=self.callback_quit)
        self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_beep)
        self.minitel.enableKeyboard()

        while not self.stopped():
            self.minitel.setZoneAttributes(color=BackgroundColor.BLACK)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.BLUE)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.RED)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.GREEN)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.CYAN)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.WHITE)
            self.minitel.readKeyboard(.1)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.YELLOW)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.CYAN)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.GREEN)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.MAGENTA)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.RED)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.setZoneAttributes(color=BackgroundColor.BLUE)
            self.minitel.send(Layout.fillLine())
            self.minitel.send(Layout.cariageReturn())
            self.minitel.send(Layout.moveCursorDown())
            self.minitel.readKeyboard(.1)

