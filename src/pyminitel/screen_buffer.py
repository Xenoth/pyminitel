from pyminitel.attributes import ZoneAttributes, TextAttributes, BackgroundColor, CharacterColor
from pyminitel.layout import Layout

from logging import *
from os import path, remove, open

class ScreenBuffer:

    zone_attributes_buf = []

    text_attributes_buf = []

    text_buf = []

    __screen_width = 0
    __screen_height = 0

    def __init__(self, screen_height: int, screen_width: int) -> None:
        
        self.__screen_width = screen_width
        self.__screen_height = screen_height

        self.zone_attributes_buf = [[0 for _ in range(self.__screen_width)] for _ in range(self.__screen_width)]
        self.text_attributes_buf = [[0 for _ in range(self.__screen_width)] for _ in range(self.__screen_height)]
        self.text_buf = [[0 for _ in range(self.__screen_width)] for _ in range(self.__screen_height)]

        for r in range(self.__screen_height):
            for c in range(self.__screen_width):
                self.zone_attributes_buf[r][c] = ZoneAttributes()
                self.text_attributes_buf[r][c] = TextAttributes()
                self.text_buf[r][c] = ''


    def toVideotex(self) -> bytes:
        data = b''

        previous_zone = ZoneAttributes()
        previous_text = TextAttributes()

        skip = False

        last_skip_r, last_skip_c = None, None

        for r in range(self.__screen_height):
            for c in range(self.__screen_width):

                print(self.zone_attributes_buf)

                zone = self.zone_attributes_buf[r][c]
                text = self.text_attributes_buf[r][c]
                char = self.text_buf[r][c]

                print(zone)
                print(type(zone))

                # Update Text only
                data += previous_text.diff(text)

                # Update Zone
                diff = previous_zone.diff(zone)

                if len(diff):
                    if char != ' ':
                        log(WARNING, "Minitel requires a withspace on zone's declaration, ignoring char")
                    char = ''
                
                # Write char or Zone updating
                if len(char) or len(diff):
                    if len(char) > 1:
                        char = char[0:1]
                    if skip:
                        # TODO - Optimize with last_skip_c and last_skip_r to move only vertically on horizontally if possible
                        data += Layout.setCursorPosition(r + 1, c + 1)
                        skip = False

                    data += diff + char

                # if nothing to do save the least coordonates
                if len(char) == 0 and diff:
                    skip = True
                    last_skip_c = c
                    last_skip_r = r

                previous_zone = zone
                previous_text = text

    def toVidetexFile(self, destination: str = '.', filename: str = 'PAGE'):
        filepath = path.join, destination, filename  + '.VDT'
        if path.exists(filepath):
            remove(filepath)
        with open(filepath, "wb") as binary_file:
            binary_file.write(self.toVideotex())

screen = ScreenBuffer(3, 6)

print(screen.zone_attributes_buf)

for i in range(4):
    screen.zone_attributes_buf[1][1 + i] = ZoneAttributes().setAttributes(color=BackgroundColor.WHITE)
    if i > 0:
        screen.text_buf[1][i + 1] = '0'

screen.text_buf[2][5] = '6'

print(screen.toVideotex().hex())