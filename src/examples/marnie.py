from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.page import Page

from logging import log, ERROR
import time

class MarniePage(Page):

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)
        self.prompt = ''

    def print_page(self):
        self.minitel.clear()
        msg = "   ________________"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "  / ____/ ___/ ____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = " / /    \\__ \\\\__ \\"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "/ /___ ___/ /__/ /"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "\\____//____/____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()

        msg = "    __  ___ ___   ____   _   __ __ ____"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "   /  |/  //   | / __ \\ / | / // // __/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "  / /|_/ // /| |/ /_/ //  |/ // // _/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = " / /  / // /_| / _, _// /|  // // /__"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "/_/  /_//_/  |/_/ |_|/_/ |_//_//____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(4))
        self.minitel.send(Layout.moveCursorRight(5))

        self.minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
        self.minitel.setZoneAttributes(BackgroundColor.WHITE, masking=False)
        msg = "/// HIRAGINI CORPORATION \\\\\\ "
        self.minitel.print(msg)
        self.minitel.setZoneAttributes(color=BackgroundColor.BLACK)
        self.minitel.resetTextAttributes()
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(3))

        self.minitel.setZoneAttributes(color=BackgroundColor.BLACK, highlight=True)
        msg = "[MOTHER]"
        self.minitel.print(msg)
        self.minitel.setZoneAttributes(highlight=False)
        msg = "- Good Morning, Lieutenant."
        self.minitel.print(msg)
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(2))

        msg = "XENOTH_VAL[Lieut.]$> .................."
        self.minitel.print(msg)
        self.minitel.showCursor()

        self.minitel.send(Layout.setCursorPosition(24, 29))
        msg = "Send: "
        self.minitel.print(msg)
        self.minitel.setTextAttributes(color=CharacterColor.GREEN, inverted=True)
        msg = "Envoi"
        self.minitel.print(msg)

        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.resetTextAttributes()
        if len(self.prompt):
            self.minitel.print(self.prompt)

        
    def callback_quit(self):
        self.minitel.clear()
        self.minitel.send(Layout.setCursorPosition(5,3))
        self.minitel.setZoneAttributes(highlight=True)
        self.minitel.print('[MOTHER]')
        self.minitel.setZoneAttributes(highlight=False)
        self.minitel.print("- Logout from ship's")
        self.minitel.send(Layout.setCursorPosition(6, 15)) 
        self.minitel.print("terminal")
        for i in range(3):
            time.sleep(1)
            self.minitel.beep()
            self.minitel.print('.')

        self.minitel.send(Layout.setCursorPosition(9,12))
        self.minitel.print('Fly safe Lieutenant.')
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def callback_send(self):
        self.minitel.disableKeyboard()
        self.minitel.send(Layout.setCursorPosition(19, 13))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        if 'quoi' in self.prompt.lower():
            self.prompt = "Quoicoubeeeeh"
        msg = 'You said:' + self.prompt + '?'
        self.minitel.print(msg)
        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.print('..................')
        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.beep()
        self.prompt = ''
        self.minitel.enableKeyboard()

    def callback_any(self):
        self.minitel.beep()

    def callback_printable(self, c: str = None):
        if c is not None:
            if len(self.prompt) < 18:
                self.prompt += c
                self.minitel.send(ascii_to_alphanumerical(c=c, vm=VisualizationModule.VGP5))

    def callback_erease(self):
        if len(self.prompt):
            self.minitel.send(Layout.moveCursorLeft(1))
            self.minitel.print('.')
            self.minitel.send(Layout.moveCursorLeft(1))
            self.prompt = self.prompt[:-1]

    def callback_cancel(self):
        if len(self.prompt):
            self.minitel.disableKeyboard()
            self.minitel.send(Layout.setCursorPosition(22, 22))
            self.minitel.print('..................')
            self.minitel.send(Layout.setCursorPosition(22, 22))
            self.minitel.enableKeyboard()
            self.prompt = ''

    def run(self):
        try:
            # Disable Keyboard as soon as possible to avoir communications errors
            self.minitel.disableKeyboard()
            # Echo mode is a debug mode if Modem not connected - Disable 'cause using DIN connector
            self.minitel.disableEcho()
            self.minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_4800)
            self.print_page()
            self.minitel.getMinitelInfo()
            self.minitel.beep()

            self.minitel.clearBindings()


            self.minitel.bind(FunctionKeyboardCode.Connection_Switch, callback=self.callback_quit)
            self.minitel.bind(FunctionKeyboardCode.Send, callback=self.callback_send)
            self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)
            self.minitel.bind(FunctionKeyboardCode.Correction, callback=self.callback_erease)
            self.minitel.bind(FunctionKeyboardCode.Cancel, callback=self.callback_cancel)

            self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_any)
            self.minitel.bind(FilterKeyboardCode.Printable_Keys, callback=self.callback_printable)


            self.minitel.setKeyboardMode(extended=False)
            self.minitel.enableKeyboard()

            while not self.stopped():
                self.minitel.readKeyboard(0.1)
        except Exception as e:
            log(ERROR, e)
            self.stop()
