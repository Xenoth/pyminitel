import os

from logging import log, ERROR
from typing import LiteralString

from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.page import Page

class GuidePage(Page):

    def __init__(self, minitel=...) -> None:
        super().__init__(minitel)

        self.page: bytes = b''
        filepath: LiteralString = os.path.join('.', 'src', 'examples', 'resources', 'GUIDE_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()

    def print_page(self) -> None:
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.beep()
        self.minitel.get_minitel_info()

    def callback_quit(self) -> None:
        self.minitel.beep()
        self.minitel.get_minitel_info()
        self.stop()

    def callback_beep(self) -> None:
        self.minitel.beep()

    def run(self) -> None:
        self.minitel.disable_keyboard()
        self.minitel.disable_echo()
        self.minitel.set_video_mode(Mode.VIDEOTEX)
        self.print_page()

        self.minitel.clear_bindings()

        self.minitel.bind(FunctionKeyboardCode.REPEAT, callback=self.print_page)
        self.minitel.bind(FunctionKeyboardCode.SUMMARY, callback=self.callback_quit)
        self.minitel.bind(FilterKeyboardCode.ANY_KEYS, callback=self.callback_beep)

        self.minitel.hide_cursor()
        self.minitel.enable_keyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.read_keyboard(0.1)
