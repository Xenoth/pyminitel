"""
videotex.py

This module contains an utility class to draw and write and get an optimized videotex buffer,
see pyminitel/src/examples/ for usages.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import os
import copy

from typing import Optional
from logging import log, ERROR, WARNING, DEBUG

from pyminitel.attributes import ZoneAttributes, TextAttributes
from pyminitel.layout import Layout
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import RESOLUTION, Mode

class Videotex:
    """ Videotex class.

    Utility class that allows your to enqueue all the layout and content of your page
    in one optimized buffer.
    """
    def __init__(self) -> None:
        """Videotex's constructor.
        """
        self._screen_height = RESOLUTION[Mode.VIDEOTEX][0] - 1
        self._screen_width = RESOLUTION[Mode.VIDEOTEX][1]

        self.zone_attributes_buf = [
            [ZoneAttributes() for _ in range(self._screen_width)]
            for _ in range(self._screen_height)
        ]
        self.text_attributes_buf = [
            [TextAttributes() for _ in range(self._screen_width)]
            for _ in range(self._screen_height)
        ]
        self.text_buf = [
            ['' for _ in range(self._screen_width)]
            for _ in range(self._screen_height)
        ]

    def to_videotex(self, vm: VisualizationModule) -> bytes:
        """Generate a videotex buffer from the current state of the Videotex instance.

        Args:
            vm (VisualizationModule): Visualization module targeted.

        Returns:
            bytes: Videotex buffer.
        """
        data = b''

        previous_zone = ZoneAttributes()
        previous_text = TextAttributes()

        skip = False

        char_double_w_inline = False
        last_skip_r, last_skip_c = None, None

        for r in range(self._screen_height):
            for c in range(self._screen_width):
                zone = self.zone_attributes_buf[r][c]
                text = self.text_attributes_buf[r][c]
                char = self.text_buf[r][c]

                # Update Text only
                text_diff = previous_text.diff(text)
                if len(text_diff) > 0:
                    log(ERROR, 'r:' + str(r) + ' c:' +str(c) + ' diff:' + str(text_diff.hex()))
                data += text_diff
                if text.double_width:
                    char_double_w_inline = True


                # Update Zone
                diff = previous_zone.diff(zone)

                if len(diff) > 0:
                    if char not in (' ', ''):
                        log(
                            WARNING,
                            "Minitel requires a whitespace on zone's declaration, "
                            "ignoring char (r=%s c=%s)",
                            str(r),
                            str(c)
                        )
                    char = ''

                # Write char or Zone updating
                if len(char) > 0 or len(diff) > 0:
                    if len(char) > 1:
                        char = char[0:1]
                    if skip:
                        log(DEBUG, 'setCursorPosition(r=' + str(r) + ', c=' + str(c) +')')
                        if r == last_skip_r and not char_double_w_inline:
                            data += Layout.move_cursor_right(c - last_skip_c)
                        elif c == last_skip_c:
                            data += Layout.move_cursor_down(r - last_skip_r)
                        else:
                            data += Layout.set_cursor_position(r + 1, c + 1)
                        skip = False

                    log(DEBUG, 'diff=' + diff.hex() + ' ,char=' + char)
                    data += diff
                    if len(diff) > 0:
                        data += Layout.fill_line()
                    if len(char):
                        data += ascii_to_alphanumerical(c=char, vm=vm)

                # if nothing to do save the least coordinates
                if not len(char) > 0 and not len(diff) > 0:
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

    def set_text(self, text: str, r: int, c: int, attribute: Optional[TextAttributes] = None):
        """Write a text at a given position.

        Args:
            text (str): Text to print.
            r (int): Row position.
            c (int): Column position.
            attribute (TextAttributes, optional): Text's attribute. Defaults to None.
        """
        if r < 1 or c < 1 or r > self._screen_height or c > self._screen_width:
            log(ERROR, 'Invalid argument passed.')
            return
        while len(text) > 0:
            self.text_buf[r - 1][c - 1] = text[0:1]
            if attribute is not None:
                self.text_attributes_buf[r - 1][c - 1] = copy.deepcopy(attribute)
            c += 1
            if c > self._screen_width:
                c = 1
                if r < self._screen_height:
                    r += 1
            text = text[1:]

    def draw_box(
            self,
            r: int,
            c: int,
            h: int,
            w: int,
            zone_attribute: ZoneAttributes = ZoneAttributes()
    ):
        """Draw a filled box to display.

        Args:
            r (int): Row position.
            c (int): Column position.
            h (int): Height of the box.
            w (int): Width of the box.
            zone_attribute (ZoneAttributes, optional):  Zone attribute of the box.
                                                        Defaults to ZoneAttributes().
        """
        if r < 1 or c < 1 or r + h - 1 > self._screen_height or c + w - 1 > self._screen_width:
            log(ERROR, 'Invalid argument passed.')
            return

        for i in range(h):
            for j in range(w):
                self.zone_attributes_buf[r - 1 + i][c - 1 + j] = copy.deepcopy(zone_attribute)
                self.text_buf[r - 1 + i][c - 1 + j] = ''

    def draw_hr(self, r: int):
        """Draw an horizontal rule.

        Args:
            r (int): Row position.
        """
        if r < 1 or r > 24:
            log(ERROR, 'Invalid argument given.')
        for c in range(self._screen_width):
            self.text_buf[r - 1][c] = '–'

    def draw_vr(self, c: int):
        """Draw a vertical rule.

        Args:
            c (int): Column position.
        """
        if c < 1 or c > 40:
            log(ERROR, 'Invalid argument given.')
        for r in range(self._screen_height):
            self.text_buf[r][c - 1] = "|"

    def draw_frame(self, r: int, c: int, h: int, w: int):
        """Draw a frame:
            +––––+
            |    |
            +––––+

        Args:
            r (int): Row position.
            c (int): Column position.
            h (int): Height of the frame.
            w (int): Width of the frame.
        """
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

    def to_videotex_file(self, destination: str = '.', filename: str = 'PAGE'):
        """Generate a Videotex file from the current state of the instance.

        Args:
            destination (str, optional): Destination folder. Defaults to '.'.
            filename (str, optional): Output filename. Defaults to 'PAGE'.
        """
        for vm in VisualizationModule:
            vm_str = 'VGP5' if vm == VisualizationModule.VGP5 else 'VGP2'
            filepath = os.path.join(destination, filename + '_' +  vm_str  + '_.VDT')
            log(DEBUG, filepath)
            if os.path.exists(filepath):
                os.remove(filepath)
            with open(filepath, 'wb') as binary_file:
                binary_file.write(self.to_videotex(vm=vm))
                binary_file.close()
