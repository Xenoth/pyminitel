"""
layout.py

This module contains layout's methods to send Minitel display commands for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

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
    """Layout Class

    Contains static methods to construct Minitel's layout command.
    """

    class CSIJ(Enum):
        """CSI J Class.

        Define values for erase_in_display method.

        Args:
            Enum (Enum): Enumerator.
        """

        FROM_CURSOR_TO_EOS = 0
        FROM_SOS_TO_CURSOR = 1
        ALL_SCREEN = 2

    class CSIK(Enum):
        """CSI K Class.

        Define values for erase_in_line method.

        Args:
            Enum (Enum): Enumerator.
        """

        FROM_CURSOR_TO_EOL = 0
        FROM_SOL_TO_CURSOR = 1
        ALL_LINE = 2

    @staticmethod
    def carriage_return() -> bytes:
        """Return carriage command.

        Returns:
            bytes: Minitel command.
        """

        return CR

    @staticmethod
    def move_cursor_up(n: int = 1) -> bytes:
        """Move the cursor up.

        Args:
            n (int, optional): Number of rows to move up. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        command: bytes = b''
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
        """Move the cursor down.

        Args:
            n (int, optional): Number of rows to move down. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        command: bytes = b''

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
        """Move the cursor right.

        Args:
            n (int, optional): Number of rows to move right. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        command: bytes = b''

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
        """Move the cursor left.

        Args:
            n (int, optional): Number of rows to move left. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        command: bytes = b''

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
        """Set the cursor position.

        Args:
            r (int, optional): Row position. Defaults to 1.
            c (int, optional): Column position. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        return CSI + str.encode(str(r)) + b'\x3b' + str.encode(str(c)) + b'\x48'

    @staticmethod
    def reset_cursor() -> bytes:
        """Reset cursor position at row 1; column 1.

        Returns:
            bytes: Minitel command.
        """

        return RS

    @staticmethod
    def clear() -> bytes:
        """Clear the screen.

        Returns:
            bytes: Minitel command.
        """

        return FF

    @staticmethod
    def fill_line() -> bytes:
        """Fill the current line with the last zone attribute,
        from the cursor to the end of the line.

        Returns:
            bytes: Minitel command.
        """

        return CAN

    @staticmethod
    def erase_in_display(n: CSIJ = CSIJ.FROM_CURSOR_TO_EOS) -> bytes:
        """Erase the display from the cursor position.

        Args:
            n (CSIJ, optional): Clear method. Defaults to CSIJ.FROM_CURSOR_TO_EOS.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        return CSI + str.encode(str(n.value)) + b'\x4a'

    @staticmethod
    def erase_in_line(csi_k: CSIK = CSIK.ALL_LINE) -> bytes:
        """Erase the line from the cursor position.

        Args:
            csi_k (_type_, optional): Clear method. Defaults to CSIK.ALL_LINE.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        command: bytes = b''

        if  csi_k == Layout.CSIK.FROM_CURSOR_TO_EOL:
            command = b'\x4b'

        elif csi_k == Layout.CSIK.FROM_SOL_TO_CURSOR:
            command = b'\x31\x4b'

        else:
            command = b'\x32\x4b'

        return CSI + command

    @staticmethod
    def delete(n: int = 1) -> bytes:
        """Delete given number of character from the cursor position.

        Args:
            n (int, optional): number of characters to delete. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        return CSI + str.encode(str(n).zfill(2)) + b'\x50'

    @staticmethod
    def set_insert_mode() -> bytes:
        """Switch to inserting mode.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        return CSI + b'\x34\x68'

    @staticmethod
    def unset_insert_mode() -> bytes:
        """Unswitch from inserting mode.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        return CSI + b'\x34\x6c'

    @staticmethod
    def delete_next_lines(n: int = 1) -> bytes:
        """Delete the lines from the cursor position.

        Args:
            n (int, optional): Number of lines. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        return CSI + str.encode(str(n)) + b'\x4d'

    @staticmethod
    def insert_lines(n: int = 1) -> bytes:
        """Inset lines from the cursor position.

        Args:
            n (int, optional): Number of lines. Defaults to 1.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        return CSI + str.encode(str(n)) + b'\x4c'

    @staticmethod
    def add_sub_section(r: int, c: int, char: str | None = None) -> bytes:
        """Add a sub section.

        Args:
            r (int): Row position.
            c (int): Column position.
            char (str, optional): Character. Defaults to None.

        Returns:
            bytes: Minitel command.
        """

        # TODO - Try IRL
        if char is not None:
            if len(char) != 1:
                log(
                    ERROR,
                    "Invalid argument passed, expected one character but got" + str(char) + "."
                )

        mask: int = 1 << 6

        r |= mask
        c |= mask

        binary_r: bytes = r.to_bytes(1, 'little')
        binary_c: bytes = c.to_bytes(1, 'little')

        us = US + binary_r + binary_c

        if char is not None:
            us += ascii_to_alphanumerical(char, VisualizationModule.VGP5)

        return us
