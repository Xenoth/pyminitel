from pyminitel.alphanumerical import *
from pyminitel.visualization_module import VisualizationModule

from enum import Enum
from serial import Serial
from logging import *


BS = b'\x08'        # Backspace
HT = b'\x09'        # Horizontal Tab
LF = b'\x0a'        # Linefeed
VT = b'\x0b'        # Vertical Tab
CR = b'\x0d'        # Carriage Return 
CSI = b'\x1b\x5b'    # Control Sequence Introducer
RS = b'\x1e'        # Record Separator
FF = b'\x0c'        # Form Feed
US = b'\x1e'        # Unit Separator
CAN = b'\x18'       # Cancel

CUU = b'\x41'       # Cursor Up
CUD = b'\x42'       # Cursor Down
CUF = b'\x43'       # Cursor Forward
CUB = b'\x44'       # Cursor Backward

class Layout:

    class CSI_J(Enum):
        FROM_CURSOR_TO_EOS = 0
        FROM_SOS_TO_CURSOR = 1
        ALL_SCREEN = 2

    class CSI_K(Enum):
        FROM_CURSOR_TO_EOL = 0
        FROM_SOL_TO_CURSOR = 1
        ALL_LINE = 2

    def cariageReturn() -> bytes:
        return CR

    def moveCursorUp(n: int = 1) -> bytes:
        command = b''
        # TODO - CSI when cursor position is 1
        # if n < 4:
        i = 0
        while i < n:
            i += 1
            command += VT 
        # else:
        #     command += CSI + str.encode(str(n)) + CUU
        
        return command

    def moveCursorDown(n: int = 1) -> bytes:
        command = b''
        # TODO - CSI when cursor position is 40
        # if n < 4:
        i = 0
        while i < n:
            i += 1
            command += LF 

        # else:
        #     command += CSI + str.encode(str(n)) + CUD

        return command

    def moveCursorRight(n: int = 1) -> bytes:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += HT 
        else:
            command += CSI + str.encode(str(n)) + CUF

        return command

    def moveCursorLeft(n: int = 1) -> bytes:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += BS
        else:
            command += CSI + str.encode(str(n)) + CUB

        return command

    def setCursorPosition(r: int = 1, c: int = 1) -> bytes:
        return CSI + str.encode(str(r)) + b'\x3b' + str.encode(str(c)) + b'\x48'

    def resetCursor() -> bytes:
        return RS

    def clear() -> bytes:
        return FF

    def fillLine() -> bytes:
        return CAN

    def eraseInDisplay(n: CSI_J = CSI_J.FROM_CURSOR_TO_EOS) -> bytes:
        # TODO - Test
        return CSI + str.encode(str(n.value)) + b'\x4a'

    def eraseInLine(n: CSI_K = CSI_K.FROM_CURSOR_TO_EOL) -> bytes:
        # TODO - Test
        return CSI + str.encode(str(n.value)) + b'\x4b'

    def delete(n: int = 1) -> bytes:
        return CSI + str.encode(str(n).zfill(2)) + b'\x50'

    def setInsertMode() -> bytes:
        # TODO - Test
        return CSI + b'\x34\x68'

    def unsetInsertMode() -> bytes:
        # TODO - Test
        return CSI + b'\x34\x6c'
        
    def deleteNextLines(n: int = 1) -> bytes:
        # TODO - Test
        return CSI + str.encode(str(n)) + b'\x4d'

    def insertLines(n: int = 1) -> bytes:
        # TODO - Test
        return CSI + str.encode(str(n)) + b'\x4c'

    def addSubSection(r: int, c: int, char: str = None) -> bytes:
        # TODO - Test
        if str is not None:
            if len(char) != 1:
                log(ERROR, "Invalid argument passer, expected character but got" + char + ".")
        
        mask = 1 << 6

        r |= mask
        c |= mask

        binary_r = r.to_bytes(1, 'little')
        binary_c = c.to_bytes(1, 'little')

        us = US + binary_r + binary_c

        if char is not None:
            us += ascii_to_alphanumerical('A', VisualizationModule.VGP5)

        return us
