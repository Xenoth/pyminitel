import copy

from enum import Enum

ESC = b'\x1b'
DELIMETER = b'\x20'

class CharacterColor(Enum):
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
    def __init__(self) -> None:
        self.color = CharacterColor.WHITE
        self.blinking = False
        self.background = BackgroundColor.BLACK
        self.disjointed = False

    def set_attributes(
        self,
        color: CharacterColor = None,
        blinking: bool = None,
        background: BackgroundColor = None,
        disjointed: bool = None
    ) -> bytes:

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

    def __init__(self) -> None:
        self.color = CharacterColor.WHITE
        self.blinking = False
        self.inverted = False
        self.double_height = False
        self.double_width = False

    def set_attributes(
        self,
        color: CharacterColor = None,
        blinking: bool = None,
        inverted = None,
        double_height: bool = None,
        double_width: bool = None
    ) -> bytes:

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

    def __init__(self) -> None:
        self.background = BackgroundColor.BLACK
        self.masking = False
        self.highlight = False

    def set_attributes(
        self,
        color: BackgroundColor = None,
        masking: bool = None,
        highlight: bool = None
    ) -> bytes:

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
            data += DELIMETER

        return data

    def diff(self, new: "ZoneAttributes") -> bytes:
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
