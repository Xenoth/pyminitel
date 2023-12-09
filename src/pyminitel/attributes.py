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
NORMAL_BG = b'\x4c'
INVERSED_BG = b'\x4d'

UNMASKING = b'\x5F'    


class TextAttributes():

    color = CharacterColor.WHITE
    blinking = False
    double_height = False
    double_width = False

    def __init__(self) -> None:
        pass

class ZoneAttributes():

    background = BackgroundColor.BLACK
    masking = False
    highlight = False

    def __init__(self) -> None:
        pass


