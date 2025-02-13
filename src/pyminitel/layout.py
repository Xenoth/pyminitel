from enum import Enum
from logging import log, ERROR

from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.visualization_module import VisualizationModule

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

    class CSIJ(Enum):
        FROM_CURSOR_TO_EOS = 0
        FROM_SOS_TO_CURSOR = 1
        ALL_SCREEN = 2

    class CSIK(Enum):
        FROM_CURSOR_TO_EOL = 0
        FROM_SOL_TO_CURSOR = 1
        ALL_LINE = 2

    @staticmethod
    def cariage_return() -> bytes:
        return CR

    @staticmethod
    def move_cursor_up(n: int = 1) -> bytes:
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

    @staticmethod
    def move_cursor_down(n: int = 1) -> bytes:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += LF

        else:
            command += CSI + str.encode(str(n)) + CUD

        return command

    @staticmethod
    def move_cursor_right(n: int = 1) -> bytes:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += HT
        else:
            command += CSI + str.encode(str(n)) + CUF

        return command

    @staticmethod
    def move_cursor_left(n: int = 1) -> bytes:
        command = b''
        if n < 4:
            i = 0
            while i < n:
                i += 1
                command += BS
        else:
            command += CSI + str.encode(str(n)) + CUB

        return command

    @staticmethod
    def set_cursor_position(r: int = 1, c: int = 1) -> bytes:
        return CSI + str.encode(str(r)) + b'\x3b' + str.encode(str(c)) + b'\x48'

    @staticmethod
    def reset_cursor() -> bytes:
        return RS

    @staticmethod
    def clear() -> bytes:
        return FF

    @staticmethod
    def fill_line() -> bytes:
        return CAN

    @staticmethod
    def erase_in_display(n: CSIJ = CSIJ.FROM_CURSOR_TO_EOS) -> bytes:
        # TODO - Try IRL
        return CSI + str.encode(str(n.value)) + b'\x4a'

    @staticmethod
    def erase_in_line(csi_k = CSIK.ALL_LINE) -> bytes:
        # TODO - Try IRL
        command = b''

        if  csi_k == Layout.CSIK.FROM_CURSOR_TO_EOL:
            command = b'\x4b'

        elif csi_k == Layout.CSIK.FROM_SOL_TO_CURSOR:
            command = b'\x31\x4b'

        else:
            command = b'\x32\x4b'

        return CSI + command

    @staticmethod
    def delete(n: int = 1) -> bytes:
        return CSI + str.encode(str(n).zfill(2)) + b'\x50'

    @staticmethod
    def set_insert_mode() -> bytes:
        # TODO - Try IRL
        return CSI + b'\x34\x68'

    @staticmethod
    def unset_insert_mode() -> bytes:
        # TODO - Try IRL
        return CSI + b'\x34\x6c'

    @staticmethod
    def delete_next_lines(n: int = 1) -> bytes:
        # TODO - Try IRL
        return CSI + str.encode(str(n)) + b'\x4d'

    @staticmethod
    def insert_lines(n: int = 1) -> bytes:
        # TODO - Try IRL
        return CSI + str.encode(str(n)) + b'\x4c'

    @staticmethod
    def add_sub_section(r: int, c: int, char: str = None) -> bytes:
        # TODO - Try IRL
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
