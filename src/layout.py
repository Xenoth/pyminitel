from enum import Enum
from aplhanumerical import *
from sys import stderr
from mode import Mode

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

    __r = 0 
    __c = 0

    resolution = {
        Mode.VIDEOTEX: {
            25,
            40,
        },
        Mode.MIXED: {
            25,
            80,
        }
    }



    class CSI_J(Enum):
        FROM_CURSOR_TO_EOS = 0
        FROM_SOS_TO_CURSOR = 1
        ALL_SCREEN = 2

    class CSI_K(Enum):
        FROM_CURSOR_TO_EOL = 0
        FROM_SOL_TO_CURSOR = 1
        ALL_LINE = 2

    def __init__(self) -> None:
        pass
        # TODO if r == 0, pas de CSI

    def CariageReturn(Void):
        cr = b'' + CR

    def MoveCursorUp(n: int = 1) -> None:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += VT 
        else:
            command += CSI + str.encode(str(n)) + CUU

    def MoveCursorDown(n: int = 1):
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += LF 
        else:
            command += CSI + str.encode(str(n)) + CUD

    def MoveCursorRight(n: int = 1):
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += HT 
        else:
            command += CSI + str.encode(str(n)) + CUF

    def MoveCursorLeft(n: int = 1):
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += BS
        else:
            command += CSI + str.encode(str(n)) + CUB

    def SetCursorPosition(r: int = 1, c: int = 1):
        csi = b'' + CSI + str.encode(str(r)) + b'\x3b' + str.encode(str(c)) + b'\x48'

    def ResetCursor(Void):
        rs = b'' + RS

    def Clear(Void):
        ff = b'' + FF

    def FillLine(Void):
        can = b'' + CAN

    def EraseInDisplay(n: CSI_J = CSI_J.FROM_CURSOR_TO_EOS):
        csi_j = b'' + CSI + str.encode(str(n.value)) + b'\x4a'

    def EraseInLine(n: CSI_K = CSI_K.FROM_CURSOR_TO_EOL):
        csi_k = b'' + CSI + str.encode(str(n.value)) + b'\x4b'

    def Delete(n: int = 1):
        csi_p = b'' + CSI + str.encode(str(n)) + b'\x50'

    def SetInsertMode(Void):
        csi_h = b'' + CSI + b'\x34\x68'

    def UnsetInsertMode(Void):
        csi_i = b'' + CSI + b'\x34\x6c'
        
    def DeleteNextLines(n: int = 1):
        csi_m = b'' + CSI + str.encode(str(n)) + b'\x4d'

    def InsertLines(n: int = 1):
        csi_l = b'' + CSI + str.encode(str(n)) + b'\x4c'

    def AddSubSection(r: int, c: int, char: str = None):
        if str is not None:
            if len(char) != 1:
                print("Error - Invalid argument passer, expected character but got" + char + ".", file=stderr)
        
        mask = 1 << 6

        r |= mask
        c |= mask

        binary_r = r.to_bytes(1, 'little')
        binary_c = c.to_bytes(1, 'little')

        us = b'' + US + binary_r + binary_c

        if char is not None:
            us += ascii_to_alphanumerical('A', visualization_module.VisualizationModule.VGP5)


        print(us.hex())

    AddSubSection(5, 25, 'A')