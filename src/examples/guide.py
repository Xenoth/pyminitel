from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.page import Page

from logging import log, ERROR

import os

class GuidePage(Page):

    def __init__(self, minitel=...) -> None:
        super().__init__(minitel)

        self.page = b''
        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'GUIDE_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()

    def print_page(self):
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.beep()
        self.minitel.getMinitelInfo()

    def callback_quit(self):
        self.minitel.beep()
        self.minitel.getMinitelInfo()
        self.stop()

    def callback_beep(self):
        self.minitel.beep()

    def run(self):
        self.minitel.disableKeyboard()
        self.minitel.disableEcho()
        self.minitel.setVideoMode(Mode.VIDEOTEX)
        self.print_page()

        self.minitel.clearBindings()
        
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)
        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_beep)
    
        self.minitel.hideCursor()
        self.minitel.enableKeyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.readKeyboard(0.1)


