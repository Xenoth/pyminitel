"""
attributes.py

This module contains the Text, Zone and SemiGraphics Attributes classes for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import copy

from typing import Optional
from enum import Enum

ESC = b'\x1b'
DELIMITER = b'\x20'

class CharacterColor(Enum):
    """ Minitel's character colors enumeration
    """
    BLACK       = b'\x40'
    RED         = b'\x41'
    GREEN       = b'\x42'
    YELLOW      = b'\x43'
    BLUE        = b'\x44'
    MAGENTA     = b'\x45'
    CYAN        = b'\x46'
    WHITE       = b'\x47'

BLINKING = b'\x48'
FIXED = b'\x49'
NORMAL_SIZE = b'\x4c'
DOUBLE_HEIGHT = b'\x4d'
DOUBLE_WIDTH = b'\x4e'
DOUBLE_SIZE = b'\x4f'

class BackgroundColor(Enum):
    """ Minitel's background colors enumeration
    """
    BLACK       = b'\x50'
    RED         = b'\x51'
    GREEN       = b'\x52'
    YELLOW      = b'\x53'
    BLUE        = b'\x54'
    MAGENTA     = b'\x55'
    CYAN        = b'\x56'
    WHITE       = b'\x57'


MASKING = b'\x58'
START_HIGHLIGHTING = b'\x5a'
END_HIGHLIGHTING = b'\x59'
NORMAL_BACKGROUND = b'\x5c'
INVERTED_BACKGROUND = b'\x5d'

START_LINEAGE = b'\x5a'
END_LINEAGE = b'\x59'

UNMASKING = b'\x5F'


class SemiGraphicsAttributes():
    """ Minitel's SemiGraphics attributes class.
    """
    def __init__(self) -> None:
        self.color = CharacterColor.WHITE
        self.blinking = False
        self.background = BackgroundColor.BLACK
        self.disjointed = False

    def set_attributes(
        self,
        color: Optional[CharacterColor] = None,
        blinking: Optional[bool] = None,
        background: Optional[BackgroundColor] = None,
        disjointed: Optional[bool] = None
    ) -> bytes:
        """Update this instance's attributes and returns a command to send, applying for
        the next SemiGraphics written on the Minitel.

        Args:
            color (CharacterColor, optional): SemiGraphics's color. Defaults to None.
            blinking (bool, optional): SemiGraphics is blinking. Defaults to None.
            background (BackgroundColor, optional): SemiGraphics's background color.
                                                    Defaults to None.
            disjointed (bool, optional): SemiGraphic's is disjointed. Defaults to None.

        Returns:
            bytes: Minitel's command
        """

        data = b''

        if color is not None:
            data += ESC + color.value
            self.color = color

        if blinking is not None:
            if blinking:
                data += ESC + BLINKING
                self.blinking = True
            else:
                data += ESC + FIXED
                self.blinking = False

        if background is not None:
            data += ESC + background.value
            self.background = background

        if disjointed is not None:
            if disjointed:
                data += ESC + START_LINEAGE
                self.disjointed = True
            else:
                data += ESC + END_LINEAGE
                self.disjointed = False

        return data

    def diff(self, new: "SemiGraphicsAttributes") -> bytes:
        """ Return the command to update the difference between the current instance,
        and the new one given, editing only the necessary attributes for optimizations.

        Args:
            new (SemiGraphicsAttributes): new attribute update to send.

        Returns:
            bytes: Minitel's command
        """
        color = None
        blinking = None
        background = None
        disjointed = None

        if self.color != new.color:
            color = new.color

        if self.blinking != new.blinking:
            blinking = new.blinking

        if self.background != new.background:
            background = new.background

        if self.disjointed != new.disjointed:
            disjointed = new.disjointed

        dump_zone = copy.deepcopy(self)
        return dump_zone.set_attributes(
            color=color, blinking=blinking, background=background, disjointed=disjointed
        )

class TextAttributes():
    """ Minitel's Text attributes class.
    """
    def __init__(self) -> None:
        self.color = CharacterColor.WHITE
        self.blinking = False
        self.inverted = False
        self.double_height = False
        self.double_width = False

    def set_attributes(
        self,
        color: Optional[CharacterColor] = None,
        blinking: Optional[bool] = None,
        inverted: Optional[bool] = None,
        double_height: Optional[bool] = None,
        double_width: Optional[bool] = None
    ) -> bytes:
        """Update this instance's attributes and returns a command to send, applying for
        the next Text written on the Minitel.

        Args:
            color (CharacterColor, optional): Text's color. Defaults to None.
            blinking (bool, optional): Text is blinking. Defaults to None.
            inverted (_type_, optional): Text and background color's are inverted. Defaults to None.
            double_height (bool, optional): Text's height increased. Defaults to None.
            double_width (bool, optional):  Text's width increased. Defaults to None.

        Returns:
            bytes: Minitel's command
        """
        data = b''

        if color is not None:
            data += ESC + color.value
            self.color = color

        if blinking is not None:
            if blinking:
                data += ESC + BLINKING
                self.blinking = True
            else:
                data += ESC + FIXED
                self.blinking = False

        if inverted is not None:
            if inverted:
                data += ESC + INVERTED_BACKGROUND
                self.inverted = True
            else:
                data += ESC + NORMAL_BACKGROUND
                self.inverted = False

        if double_height is not None or double_width is not None:
            if double_width == double_height:
                if double_height:
                    data += ESC + DOUBLE_SIZE
                    self.double_height = True
                    self.double_width = True
                else:
                    data += ESC + NORMAL_SIZE
                    self.double_height = False
                    self.double_width = False
            else:
                if (
                    double_height is not None and not double_height or
                    double_width is not None and not double_width
                ):
                    data += ESC + NORMAL_SIZE
                    if double_width is not None and not double_width:
                        self.double_width = False
                    else:
                        self.double_height = False
                if double_height:
                    data += ESC + DOUBLE_HEIGHT
                    self.double_height = True
                if double_width:
                    data += ESC + DOUBLE_WIDTH
                    self.double_width = True

        return data

    def diff(self, new: "TextAttributes") -> bytes:
        """ Return the command to update the difference between the current instance,
        and the new one given, editing only the necessary attributes for optimizations.

        Args:
            new (TextAttributes): new attribute update to send.

        Returns:
            bytes: Minitel's command
        """
        color = None
        blinking = None
        inverted = None
        double_height = None
        double_width = None

        if self.color != new.color:
            color = new.color

        if self.blinking != new.blinking:
            blinking = new.blinking

        if self.inverted != new.inverted:
            inverted = new.inverted

        if self.double_height != new.double_height:
            print('HEIGHT DIFFERENT')
            double_height = new.double_height

        if self.double_width != new.double_width:
            double_width = new.double_width

        dump_zone = copy.deepcopy(self)
        return dump_zone.set_attributes(
            color=color,
            blinking=blinking,
            inverted=inverted,
            double_height=double_height,
            double_width=double_width
        )

class ZoneAttributes():
    """ Minitel's Zone attributes class.
    To apply a zone send a white space as delimiter
    until the end of the line or a new zone delimiter.
    """
    def __init__(self) -> None:
        self.background = BackgroundColor.BLACK
        self.masking = False
        self.highlight = False

    def set_attributes(
        self,
        color: Optional[BackgroundColor] = None,
        masking: Optional[bool] = None,
        highlight: Optional[bool] = None
    ) -> bytes:
        """Update this instance's attributes and returns a command to send, containing
        zone delimiter and its attributes.

        Args:
            color (BackgroundColor, optional): Zone (background) color. Defaults to None.
            masking (bool, optional): Zone is masking. Defaults to None.
            highlight (bool, optional): Zone highlighting the text. Defaults to None.

        Returns:
            bytes: _description_
        """
        data = b''

        if color is not None:
            data += ESC + color.value
            self.background = color

        if masking is not None:
            if masking:
                data += ESC + MASKING
                self.masking = True
            else:
                data += ESC + UNMASKING
                self.masking = False

        if highlight is not None:
            if highlight:
                data += ESC + START_HIGHLIGHTING
                self.highlight = True
            else:
                data += ESC + END_HIGHLIGHTING
                self.highlight = False

        if len(data):
            data += DELIMITER

        return data

    def diff(self, new: "ZoneAttributes") -> bytes:
        """ Return the command to update the difference between the current instance,
        and the new one given, editing only the necessary attributes for optimizations.
        This will send another delimiter.

        Args:
            new (ZoneAttributes): new attribute update to send.

        Returns:
            bytes: Minitel's command
        """
        background = None
        highlight = None
        masking = None

        if self.background != new.background:
            background = new.background

        if self.highlight != new.highlight:
            highlight = new.highlight

        if self.masking != new.masking:
            masking = new.masking

        dump_zone = copy.deepcopy(self)
        return dump_zone.set_attributes(color=background, masking=masking, highlight=highlight)
