from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.page import Page
from pyminitel.mode import RESOLUTION, Mode

from iss_refresher import ISSRefresher
from iss_api import ISS

import os, datetime, time

class ISSPage(Page):

    MAP_WIDTH = 80
    MAP_HEIGHT = 48

    CELL_WIDTH = 2
    CELL_HEIGHT = 3

    LATITUDE_RANGE = (-90, 90)
    LONGITUDE_RANGE = (-180, 180)

    MAX_POINTS = 13

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)

        self.page = b''
        self.map = b''

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'ISS_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'EARTH_MAP.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.logo = binary_file.read()
            binary_file.close()

    def geo_to_map(self, lat, lon):
        x = int((lon - ISSPage.LONGITUDE_RANGE[0]) / (ISSPage.LONGITUDE_RANGE[1] - ISSPage.LONGITUDE_RANGE[0]) * (ISSPage.MAP_WIDTH - 1))
        y = int((lat - ISSPage.LATITUDE_RANGE[0]) / (ISSPage.LATITUDE_RANGE[1] - ISSPage.LATITUDE_RANGE[0]) * (ISSPage.MAP_HEIGHT - 1))
        return x, y

    def get_cell_indices_and_position(self, x, y):
    
        cell_x = int(x // ISSPage.CELL_WIDTH)
        cell_y = int(y // ISSPage.CELL_HEIGHT)

        rel_x = int(x % ISSPage.CELL_WIDTH)
        rel_y = int(y % ISSPage.CELL_HEIGHT)

        return cell_x, cell_y, rel_x, rel_y
    
    def render_cell(self, rel_x, rel_y):
        cell = [0 for _ in range(ISSPage.CELL_WIDTH * ISSPage.CELL_HEIGHT)]
        index = rel_y * ISSPage.CELL_WIDTH + rel_x
        cell[index] = 1

        return cell
    
    def semi_graphic_to_hex(self, semi_graphic) -> bytes:
        byte = 0
        byte += semi_graphic[0]
        byte += semi_graphic[1] << 1
        byte += semi_graphic[2] << 2
        byte += semi_graphic[3] << 3
        byte += semi_graphic[4] << 4
        byte += semi_graphic[5] << 5

        byte += int('20', 16)
        
        if byte > int('3f', 16) and byte < int('5f', 16):
            byte += int('20', 16)

        return byte.to_bytes()

    def print_iss_positions(self):

        positions = ISSRefresher().getISSPositions()
        max_points = ISSPage.MAX_POINTS
        
        if len(positions) < ISSPage.MAX_POINTS:
            max_points = len(positions)

        printable_position = positions[:max_points]

        self.minitel.send(Layout.setCursorPosition(5))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(5, 10))
        self.minitel.print(str(datetime.datetime.fromtimestamp(positions[0].timestamp)))
        self.minitel.send(Layout.setCursorPosition(5, 22))
        self.minitel.print(str(positions[0].latitude))
        self.minitel.send(Layout.setCursorPosition(5, 32))
        self.minitel.print(str(positions[0].longitude))
        blinking = True

        for iss in printable_position:
            x, y = self.geo_to_map(iss.latitude, iss.longitude)
            cell_x, cell_y, rel_x, rel_y = self.get_cell_indices_and_position(x, y)

            if (cell_x) != 1 and (cell_x) != RESOLUTION[Mode.VIDEOTEX][1]:
                semi_graphic = self.render_cell(rel_x, rel_y)
                data = Layout.setCursorPosition(RESOLUTION[Mode.VIDEOTEX][0] - cell_y - 3, cell_x)
                data += b'\x0e'
                data += SemiGraphicsAttributes().setAttributes(color=CharacterColor.RED, blinking=blinking, background=BackgroundColor.BLUE, disjointed=True)
                data += self.semi_graphic_to_hex(semi_graphic)
                data += b'\x0f'

                self.minitel.send(data)
                blinking = False


    def print_page(self):
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.send(self.logo)
        self.print_iss_positions()
        self.minitel.beep()
        self.minitel.getMinitelInfo()

        
    def callback_quit(self):
        self.minitel.clear()
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def run(self):
        self.minitel.disableKeyboard()
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
