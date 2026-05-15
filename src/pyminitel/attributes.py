"""
attributes.py

This module contains the Text, Zone and SemiGraphics Attributes classes for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import copy

from enum import Enum
from dataclasses import dataclass
from typing import Final

ESC: Final[bytes] = b'\x1b'
DELIMITER: Final[bytes] = b'\x20'

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

BLINKING: Final[bytes] = b'\x48'
FIXED: Final[bytes] = b'\x49'
NORMAL_SIZE: Final[bytes] = b'\x4c'
DOUBLE_HEIGHT: Final[bytes] = b'\x4d'
DOUBLE_WIDTH: Final[bytes] = b'\x4e'
DOUBLE_SIZE: Final[bytes] = b'\x4f'

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

MASKING: Final[bytes] = b'\x58'
START_HIGHLIGHTING: Final[bytes] = b'\x5a'
END_HIGHLIGHTING: Final[bytes] = b'\x59'
NORMAL_BACKGROUND: Final[bytes] = b'\x5c'
INVERTED_BACKGROUND: Final[bytes] = b'\x5d'

START_LINEAGE: Final[bytes] = b'\x5a'
END_LINEAGE: Final[bytes] = b'\x59'

UNMASKING: Final[bytes] = b'\x5F'

@dataclass(slots=True)
class SemiGraphicsAttributesState():
    """ Minitel's SemiGraphics attributes state for api usage.
    """

    color: CharacterColor | None = None
    background: BackgroundColor | None = None
    blinking: bool | None = None
    disjointed: bool | None = None

class SemiGraphicsAttributes():
    """ Minitel's SemiGraphics attributes class.
    """

    def __init__(self) -> None:
        self.state: SemiGraphicsAttributesState = SemiGraphicsAttributesState(
            color = CharacterColor.WHITE,
            blinking = False,
            background = BackgroundColor.BLACK,
            disjointed = False
        )

    def set_attributes(self, state: SemiGraphicsAttributesState) -> bytes:
        """Update this instance's attributes and returns a command to send, applying for
        the next SemiGraphics written on the Minitel.

        Args:
            state (SemiGraphicsAttributesState):
                SemiGraphics's state, attributes are None by default.
        Returns:
            bytes: Minitel's command
        """

        data: bytes = b''

        if state.color is not None:
            data += ESC + state.color.value
            self.state.color = state.color

        if state.blinking is not None:
            if state.blinking:
                data += ESC + BLINKING
                self.state.blinking = True
            else:
                data += ESC + FIXED
                self.state.blinking = False

        if state.background is not None:
            data += ESC + state.background.value
            self.state.background = state.background

        if state.disjointed is not None:
            if state.disjointed:
                data += ESC + START_LINEAGE
                self.state.disjointed = True
            else:
                data += ESC + END_LINEAGE
                self.state.disjointed = False

        return data

    def diff(self, new: "SemiGraphicsAttributes") -> bytes:
        """ Return the command to update the difference between the current instance,
        and the new one given, editing only the necessary attributes for optimizations.

        Args:
            new (SemiGraphicsAttributes): new attribute update to send.

        Returns:
            bytes: Minitel's command
        """

        dump_state: SemiGraphicsAttributesState = SemiGraphicsAttributesState()

        if self.state.color != new.state.color:
            dump_state.color = new.state.color

        if self.state.blinking != new.state.blinking:
            dump_state.blinking = new.state.blinking

        if self.state.background != new.state.background:
            dump_state.background = new.state.background

        if self.state.disjointed != new.state.disjointed:
            dump_state.disjointed = new.state.disjointed

        dump_zone: SemiGraphicsAttributes = copy.deepcopy(self)
        return dump_zone.set_attributes(state=dump_state)

@dataclass(slots=True)
class TextAttributesState():
    """ Minitel's Text attributes state for api usage.
    """

    color: CharacterColor | None = None
    blinking: bool | None = None
    inverted: bool | None = None
    double_height: bool | None = None
    double_width: bool | None = None

class TextAttributes():
    """ Minitel's Text attributes class.
    """

    def __init__(self) -> None:
        self.state: TextAttributesState = TextAttributesState(
            color = CharacterColor.WHITE,
            blinking = False,
            inverted = False,
            double_height = False,
            double_width = False
        )

    def _set_height_width_attributes(self, state: TextAttributesState) -> bytes:
        """Private method to handle the height and width attributes

        Args:
            state (TextAttributesState): Text's attributes to set.

        Returns:
            bytes: Minitel's command for height and width update
        """

        data: bytes = b''

        if state.double_height is not None or state.double_width is not None:
            if state.double_width == state.double_height:
                if state.double_height:
                    data += ESC + DOUBLE_SIZE
                    self.state.double_height = True
                    self.state.double_width = True
                else:
                    data += ESC + NORMAL_SIZE
                    self.state.double_height = False
                    self.state.double_width = False
            else:
                if (
                    state.double_height is not None and not state.double_height or
                    state.double_width is not None and not state.double_width
                ):
                    data += ESC + NORMAL_SIZE
                    if state.double_width is not None and not state.double_width:
                        self.state.double_width = False
                    else:
                        self.state.double_height = False
                if state.double_height:
                    data += ESC + DOUBLE_HEIGHT
                    self.state.double_height = True
                if state.double_width:
                    data += ESC + DOUBLE_WIDTH
                    self.state.double_width = True

        return data

    def set_attributes(self, state: TextAttributesState) -> bytes:
        """Update this instance's attributes and returns a command to send, applying for
        the next Text written on the Minitel.

        Args:
            state TextAttributesState: Text's attributes state; Attributes are None by default.

        Returns:
            bytes: Minitel's command
        """

        data: bytes = b''

        if state.color is not None:
            data += ESC + state.color.value
            self.state.color = state.color

        if state.blinking is not None:
            if state.blinking:
                data += ESC + BLINKING
                self.state.blinking = True
            else:
                data += ESC + FIXED
                self.state.blinking = False

        if state.inverted is not None:
            if state.inverted:
                data += ESC + INVERTED_BACKGROUND
                self.state.inverted = True
            else:
                data += ESC + NORMAL_BACKGROUND
                self.state.inverted = False

        data += self._set_height_width_attributes(state=state)

        return data

    def diff(self, new: "TextAttributes") -> bytes:
        """ Return the command to update the difference between the current instance,
        and the new one given, editing only the necessary attributes for optimizations.

        Args:
            new (TextAttributes): new attribute update to send.

        Returns:
            bytes: Minitel's command
        """

        dump_state: TextAttributesState = TextAttributesState()

        if self.state.color != new.state.color:
            dump_state.color = new.state.color

        if self.state.blinking != new.state.blinking:
            dump_state.blinking = new.state.blinking

        if self.state.inverted != new.state.inverted:
            dump_state.inverted = new.state.inverted

        if self.state.double_height != new.state.double_height:
            dump_state.double_height = new.state.double_height

        if self.state.double_width != new.state.double_width:
            dump_state.double_width = new.state.double_width

        dump_zone: TextAttributes = copy.deepcopy(self)
        return dump_zone.set_attributes(state = dump_state)

@dataclass(slots=True)
class ZoneAttributesState():
    """ Minitel's Zone attributes state for api usage.
    """

    background: BackgroundColor | None = None
    masking: bool | None = None
    highlight: bool | None = None

class ZoneAttributes():
    """ Minitel's Zone attributes class.
    To apply a zone send a white space as delimiter
    until the end of the line or a new zone delimiter.
    """

    def __init__(self) -> None:
        self.state: ZoneAttributesState = ZoneAttributesState(
            background = BackgroundColor.BLACK,
            masking = False,
            highlight = False
        )

    def set_attributes(
        self,
        state: ZoneAttributesState
    ) -> bytes:
        """Update this instance's attributes and returns a command to send, containing
        zone delimiter and its attributes.

        Args:
            state TextAttributesState: Text's attributes state; Attributes are None by default.

        Returns:
            bytes: _description_
        """

        data: bytes = b''

        if state.background is not None:
            data += ESC + state.background.value
            self.state.background = state.background

        if state.masking is not None:
            if state.masking:
                data += ESC + MASKING
                self.state.masking = True
            else:
                data += ESC + UNMASKING
                self.state.masking = False

        if state.highlight is not None:
            if state.highlight:
                data += ESC + START_HIGHLIGHTING
                self.state.highlight = True
            else:
                data += ESC + END_HIGHLIGHTING
                self.state.highlight = False

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

        dump_state: ZoneAttributesState = ZoneAttributesState()

        if self.state.background != new.state.background:
            dump_state.background = new.state.background

        if self.state.highlight != new.state.highlight:
            dump_state.highlight = new.state.highlight

        if self.state.masking != new.state.masking:
            dump_state.masking = new.state.masking

        dump_zone = copy.deepcopy(self)
        return dump_zone.set_attributes(state = dump_state)
