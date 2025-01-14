from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.page import Page
from pyminitel.videotex import Videotex

from helldivers_refresher import HelldiversRefresher
from helldivers_api import WarStatus

from logging import log, ERROR
import time, os, re, pickle

from math import log, floor

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

class HelldiversPage(Page):

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)

        self.page = b''
        self.logo = b''

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'HELLDIVERS_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'HELLDIVERS_SG.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.logo = binary_file.read()
            binary_file.close()

    def draw_major_order(self, war_status: WarStatus):
        page = Videotex()

        if war_status is None or war_status.major_order is None:
            page.setText('NO MAJOR ORDER', 5, 16)
            self.minitel.send(page.toVideotex(self.minitel.getVisualizationModule()))
            return

        major_order = re.sub(CLEANR, '', war_status.major_order)

        page.setText("         ", 5, 16)
        page.setText(major_order[0: 24], 6, 1)
        page.setText(major_order[24 : 24 + 24], 7, 1)
        page.setText(major_order[24 + 24 : 24 + 24 + 24], 8, 1)

        self.minitel.send(page.toVideotex(self.minitel.getVisualizationModule()))

    def draw_planets_status(self, war_status: WarStatus):
        if war_status is None:
            return
        
        page = Videotex()

        for index in range(len(war_status.planets)):

            item_text_attr = TextAttributes()
            item_attr = ZoneAttributes()

            if index % 2:
                item_text_attr.setAttributes(CharacterColor.BLACK)
                item_attr.setAttributes(BackgroundColor.YELLOW)
            else:
                item_text_attr.setAttributes(CharacterColor.YELLOW)
                item_attr.setAttributes(BackgroundColor.BLACK)

            page.drawBox(12 + index, 1, 1, 40, item_attr)
            page.setText(text=war_status.planets[index].name, r=12 + index, c=2, attribute=item_text_attr)
            page.setText(text=str("%.2f" % war_status.planets[index].percentage) + '%', r=12 + index, c=16, attribute=item_text_attr)
            page.setText(text=str(human_format(war_status.planets[index].players)), r=12 + index, c=25, attribute=item_text_attr)
            page.setText(text=str(war_status.planets[index].owner), r=12 + index, c=34, attribute=item_text_attr)

        self.minitel.send(page.toVideotex(self.minitel.getVisualizationModule()))


    def print_page(self):
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.send(self.logo)
        war_status = pickle.loads(HelldiversRefresher().getWarStatus())
        self.draw_major_order(war_status=war_status)
        self.draw_planets_status(war_status=war_status)
        self.minitel.beep()
        self.minitel.getMinitelInfo()
        self.minitel.send(Layout.setCursorPosition(14.15))

        
    def callback_quit(self):
        self.minitel.clear()
        # self.minitel.send(Layout.setCursorPosition(5,3))
        # self.minitel.setZoneAttributes(highlight=True)
        # self.minitel.print('[MOTHER]')
        # self.minitel.setZoneAttributes(highlight=False)
        # self.minitel.print("- Logout from ship's")
        # self.minitel.send(Layout.setCursorPosition(6, 15)) 
        # self.minitel.print("terminal")
        # for i in range(3):
        #     time.sleep(1)
        #     self.minitel.beep()
        #     self.minitel.print('.')

        # self.minitel.send(Layout.setCursorPosition(9,12))
        # self.minitel.print('Fly safe Lieutenant.')
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def run(self):
        # Disable Keyboard as soon as possible to avoir communications errors
        self.minitel.disableKeyboard()
        # Echo mode is a debug mode if Modem not connected - Disable 'cause using DIN connector
        self.minitel.disableEcho()
        self.minitel.setConnectorBaudrate(Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800)
        self.print_page()

        self.minitel.clearBindings()

        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)

        self.minitel.hideCursor()
        self.minitel.enableKeyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.readKeyboard(0.1)
