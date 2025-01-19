from pyminitel.attributes import ZoneAttributes, TextAttributes
from pyminitel.layout import Layout
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import RESOLUTION, Mode

from logging import *
import os
import copy

class Videotex:

    def __init__(self) -> None:
        
        self._screen_height = RESOLUTION[Mode.VIDEOTEX][0] - 1
        self._screen_width = RESOLUTION[Mode.VIDEOTEX][1]

        self.zone_attributes_buf = [[ZoneAttributes() for _ in range(self._screen_width)] for _ in range(self._screen_height)]
        self.text_attributes_buf = [[TextAttributes() for _ in range(self._screen_width)] for _ in range(self._screen_height)]
        self.text_buf = [['' for _ in range(self._screen_width)] for _ in range(self._screen_height)]


    def toVideotex(self, vm: VisualizationModule) -> bytes:
        data = b''

        previous_zone = ZoneAttributes()
        previous_text = TextAttributes()

        skip = False

        char_double_w_inline = False;
        last_skip_r, last_skip_c = None, None

        for r in range(self._screen_height):
            for c in range(self._screen_width):
                zone = self.zone_attributes_buf[r][c]
                text = self.text_attributes_buf[r][c]
                char = self.text_buf[r][c]

                # Update Text only
                text_diff = previous_text.diff(text)
                if len(text_diff):
                    log(ERROR, 'r:' + str(r) + ' c:' +str(c) + ' diff:' + str(text_diff.hex()))
                data += text_diff
                if text.double_width:
                    char_double_w_inline = True
                

                # Update Zone
                diff = previous_zone.diff(zone)

                if len(diff):
                    if char != ' ' and char != '':
                        log(WARNING, "Minitel requires a withspace on zone's declaration, ignoring char (r=" + str(r) + " c=" + str(c) +")")
                    char = ''
                
                # Write char or Zone updating
                if len(char) or len(diff):
                    if len(char) > 1:
                        char = char[0:1]
                    if skip:
                        log(DEBUG, 'setCursorPostion(r=' + str(r) + ', c=' + str(c) +')')
                        if r == last_skip_r and not char_double_w_inline:
                            data += Layout.moveCursorRight(c - last_skip_c)
                        elif c == last_skip_c:
                            data += Layout.moveCursorDown(r - last_skip_r)
                        else:
                            data += Layout.setCursorPosition(r + 1, c + 1)
                        skip = False

                    log(DEBUG, 'diff=' + diff.hex() + ' ,char=' + char)
                    data += diff 
                    if len(diff):
                        data += Layout.fillLine()
                    if len(char):
                        data += ascii_to_alphanumerical(c=char, vm=vm)

                # if nothing to do save the least coordonates
                if not len(char) and not len(diff):
                    if not skip:
                        skip = True
                        last_skip_c = c
                        last_skip_r = r

                previous_zone = zone
                previous_text = text
            previous_zone = ZoneAttributes()
            char_double_w_inline = False

        reset_text = TextAttributes()
        data += previous_text.diff(reset_text)

        log(DEBUG, 'VDT generated:' + data.hex())
        return data
    
    def setText(self, text: str, r: int, c: int, attribute: TextAttributes = None):
        if r < 1 or c < 1 or r > self._screen_height or c > self._screen_width:
            log(ERROR, 'Invalid argument passed.')
            return
        while len(text):
            self.text_buf[r - 1][c - 1] = text[0:1]
            if attribute is not None:
                self.text_attributes_buf[r - 1][c - 1] = copy.deepcopy(attribute)
            c += 1
            if c > self._screen_width:
                c = 1
                if r < self._screen_height:
                    r += 1
            text = text[1:]

    def drawBox(self, r: int, c: int, h: int, w: int, zoneAttribute: ZoneAttributes = ZoneAttributes()):
        if r < 1 or c < 1 or r + h - 1 > self._screen_height or c + w - 1 > self._screen_width:
            log(ERROR, 'Invalid argument passed.')
            return
        
        for i in range(h):
            for j in range(w):
                self.zone_attributes_buf[r - 1 + i][c - 1 + j] = copy.deepcopy(zoneAttribute)
                self.text_buf[r - 1 + i][c - 1 + j] = ''

    def drawHR(self, r: int):
        if r < 1 or r > 24:
            log(ERROR, 'Invalid argument given.')
        for c in range(self._screen_width):
            self.text_buf[r - 1][c] = '–'
        
    def drawVR(self, c: int):
        if c < 1 or c > 40:
            log(ERROR, 'Invalid argument given.')
        for r in range(self._screen_height):
            self.text_buf[r][c - 1] = "|"

    def drawFrame(self, r: int, c: int, h: int, w: int):
        if r < 1 or c < 1 or r + h > self._screen_height or c + w > self._screen_width:
            log(ERROR, 'Invalid argument passed.')
            return
        
        for i in range(h):
            self.text_buf[i + r][c - 1] = '|'
            self.text_buf[i + r][c + w - 1] = '|'

        for i in range(w):
            self.text_buf[r - 1][i + c] = '–'
            self.text_buf[r + h - 1][i + c] = '–'

        self.text_buf[r - 1][c - 1] = '+'
        self.text_buf[r - 1 + h][c - 1] = '+'
        self.text_buf[r - 1][c - 1 + w] = '+'
        self.text_buf[r - 1 + h][c - 1 + w] = '+'

    def toVideotexFile(self, destination: str = '.', filename: str = 'PAGE'):
        
        for vm in VisualizationModule:
            vm_str = 'VGP5' if vm == VisualizationModule.VGP5 else 'VGP2'
            filepath = os.path.join(destination, filename + '_' +  vm_str  + '_.VDT')
            log(DEBUG, filepath)
            if os.path.exists(filepath):
                os.remove(filepath)
            with open(filepath, 'wb') as binary_file:
                binary_file.write(self.toVideotex(vm=vm))
                binary_file.close()


