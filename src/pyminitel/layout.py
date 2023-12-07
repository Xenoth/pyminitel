from pyminitel.alphanumerical import *
from pyminitel.mode import Mode

from enum import Enum
from sys import stderr
from serial import Serial

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
        Mode.VIDEOTEX: [
            25,
            40,
        ],
        Mode.MIXED: [
            25,
            80,
        ]
    }

    din: Serial = None

    class CSI_J(Enum):
        FROM_CURSOR_TO_EOS = 0
        FROM_SOS_TO_CURSOR = 1
        ALL_SCREEN = 2

    class CSI_K(Enum):
        FROM_CURSOR_TO_EOL = 0
        FROM_SOL_TO_CURSOR = 1
        ALL_LINE = 2

    def __init__(self, din = None) -> None:
        self.din = din

    def CariageReturn(self):
        cr = CR

        self.din.write(cr)

    def MoveCursorUp(self, n: int = 1) -> None:
        command = b''
        # TODO - CSI when cursor position is 1
        # if n < 4:
        i = 0
        while i < n:
            i += 1
            command += VT 
        # else:
        #     command += CSI + str.encode(str(n)) + CUU
        
        self.din.write(command)

    def MoveCursorDown(self, n: int = 1):
        command = b''
        # TODO - CSI when cursor position is 40
        # if n < 4:
        i = 0
        while i < n:
            i += 1
            command += LF 

        # else:
        #     command += CSI + str.encode(str(n)) + CUD

        self.din.write(command)

    def MoveCursorRight(self, n: int = 1):
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += HT 
        else:
            command += CSI + str.encode(str(n)) + CUF

        self.din.write(command)

    def MoveCursorLeft(self, n: int = 1):
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += BS
        else:
            command += CSI + str.encode(str(n)) + CUB

        self.din.write(command)

    def SetCursorPosition(self, r: int = 1, c: int = 1):
        csi = CSI + str.encode(str(r)) + b'\x3b' + str.encode(str(c)) + b'\x48'

        self.din.write(csi)

    def ResetCursor(self):
        rs = RS

        self.din.write(rs)

    def Clear(self):
        ff = FF

        self.din.write(ff)

    def FillLine(self):
        can = CAN
        
        self.din.write(can)

    def EraseInDisplay(self, n: CSI_J = CSI_J.FROM_CURSOR_TO_EOS):
        csi_j = CSI + str.encode(str(n.value)) + b'\x4a'

        self.din.write(csi_j)

    def EraseInLine(self, n: CSI_K = CSI_K.FROM_CURSOR_TO_EOL):
        csi_k = CSI + str.encode(str(n.value)) + b'\x4b'

        self.din.write(csi_k)

    def Delete(self, n: int = 1):
        csi_p = CSI + str.encode(str(n)) + b'\x50'

        self.din.write(csi_p)

    def SetInsertMode(self):
        csi_h = CSI + b'\x34\x68'

        self.din.write(csi_h)

    def UnsetInsertMode(self):
        csi_i = CSI + b'\x34\x6c'

        self.din.write(csi_i)
        
    def DeleteNextLines(self, n: int = 1):
        csi_m = CSI + str.encode(str(n)) + b'\x4d'

        self.din.write(csi_m)

    def InsertLines(self, n: int = 1):
        csi_l = CSI + str.encode(str(n)) + b'\x4c'

        self.din.write(csi_l)

    def AddSubSection(self, r: int, c: int, char: str = None):
        if str is not None:
            if len(char) != 1:
                print("Error - Invalid argument passer, expected character but got" + char + ".", file=stderr)
        
        mask = 1 << 6

        r |= mask
        c |= mask

        binary_r = r.to_bytes(1, 'little')
        binary_c = c.to_bytes(1, 'little')

        us = US + binary_r + binary_c

        if char is not None:
            us += ascii_to_alphanumerical('A', pyminitel.visualization_module.VisualizationModule.VGP5)

        self.din.write(us)
