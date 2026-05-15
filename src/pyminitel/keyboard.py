"""
keyboard.py

This module contains keyboard's description table and filters for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

from enum import Enum

class KeyboardCode(bytes, Enum):
    """KeyboardCode class.

    Class for binding and typing.
    """

class FilterKeyboardCode(KeyboardCode):
    """FilterKeyboardCode class.

    Define general filters to bind a callback on keyboard event.
    """

    ANY_KEYS = 1
    PRINTABLE_KEYS = 2
    OTHER_KEYS = 3
    NO_KEYS = 4

class FunctionKeyboardCode(KeyboardCode):
    """FunctionKeyboardCode class.

    Defines Minitel's Function specific keyboard sequences,
    allows to bind the function keys pressing.
    """

    SEND = b'\x13\x41'
    PREVIOUS = b'\x13\x42'
    REPEAT = b'\x13\x43'
    GUIDE = b'\x13\x44'
    CANCEL = b'\x13\x45'
    SUMMARY = b'\x13\x46'
    CORRECTION = b'\x13\x47'
    NEXT = b'\x13\x48'
    CONNECTION_SWITCH = b'\x13\x49' # To Modem
    TS_CONNECTION_SWITCH = b'\x13\x49' # To Din
    # CTRL_CONNECTION_SWITCH = b'' # Break send to Din or Modem

class CursorKeyboardCode(KeyboardCode):
    """CursorKeyboardCode class.

    Defines Minitel's Cursor specific keyboard sequences,
    allows to bind the cursor keys pressing.
    """

    UP = b'\x1b\x5b\x41'
    TS_UP = b'\x1b\x5b\x4d' # Delete line
    DOWN = b'\x1b\x5b\x42'
    TS_DOWN = b'\x1b\x5b\x4c' # Insert line
    RIGHT = b'\x1b\x5b\x43'
    TS_RIGHT_START = b'\x1b\x5b\x34\x68' # Start character insertion
    TS_RIGHT_STOP = b'\x1b\x5b\x34\x6c' # Stop character insertion
    LEFT = b'\x1b\x5b\x44'
    TS_LEFT = b'\x1b\x5b\x50' # Delete character
    CTRL_LEFT = b'\x7f' # DEL
    ENTER = b'\x0d' # CR
    TS_ENTER = b'\x1b\x5b\x48' # Home
    CTRL_ENTER = b'\x1b\x5b\x32\x4a' # Clear page

class VideotexKeyboardCode(KeyboardCode):
    """VideotexKeyboardCode class.

    Defines Minitel's videotex specific keyboard sequences,
    allows to bind the alphanumerical keys pressing.
    """

    CTRL_APOSTROPHE = b'\x00'
    CTRL_A = b'\x01'
    CTRL_B = b'\x02'
    CTRL_C = b'\x03'
    CTRL_D = b'\x04'
    CTRL_E = b'\x05'
    CTRL_F = b'\x06'
    CTRL_G = b'\x07'
    CTRL_H = b'\x08'
    CTRL_I = b'\x09'
    CTRL_J = b'\x0a'
    CTRL_COLON = b'\x0a'
    CTRL_K = b'\x0b'
    CTRL_SEMICOLON = b'\x0b'
    CTRL_L = b'\x0c'
    CTRL_M = b'\x0d'
    CTRL_ENTER = b'\x0d'
    CTRL_N = b'\x0e'
    CTRL_O = b'\x0f'
    CTRL_P = b'\x10'
    CTRL_Q = b'\x11'
    CTRL_R = b'\x12'
    CTRL_S = b'\x13'
    CTRL_T = b'\x14'
    CTRL_U = b'\x15'
    CTRL_V = b'\x16'
    CTRL_W = b'\x17'
    CTRL_X = b'\x18'
    CTRL_Y = b'\x19'
    CTRL_Z = b'\x1a'
    ESC = b'\x1b'
    CTRL_COMMA = b'\x1c'
    CTRL_MINUS = b'\x1d'
    CTRL_FULL_STOP = b'\x1e'
    CTRL_QUESTION_MARK = b'\x1f'
    SPACE_BAR = b'\x20'
    TS_1 = b'\x21'
    TS_2 = b'\x22'
    HASH = b'\x23'
    TS_3 = b'\x23'
    TS_4 = b'\x24'
    TS_5 = b'\x25'
    TS_6 = b'\x26'
    APOSTROPHE = b'\x27'
    TS_7 = b'\x27'
    TS_8 = b'\x28'
    TS_9 = b'\x29'
    STAR = b'\x2a'
    TS_COLON = b'\x2a'
    TS_SEMICOLON = b'\x2b'
    COMMA = b'\x2c'
    MINUS = b'\x2d'
    FULL_STOP = b'\x2e'
    TS_QUESTION_MARK = b'\x2f'
    NUM_0 = b'\x30'
    NUM_1 = b'\x31'
    NUM_2 = b'\x32'
    NUM_3 = b'\x33'
    NUM_4 = b'\x34'
    NUM_5 = b'\x35'
    NUM_6 = b'\x36'
    NUM_7 = b'\x37'
    NUM_8 = b'\x38'
    NUM_9 = b'\x39'
    COLON = b'\x3a'
    SEMICOLON = b'\x3b'
    TS_COMMA = b'\x3c'
    TS_MINUS = b'\x3d'
    TS_FULL_STOP = b'\x3e'
    QUESTION_MARK = b'\x3f'
    TS_APOSTROPHE = b'\x40'
    A = b'\x41'
    B = b'\x42'
    C = b'\x43'
    D = b'\x44'
    E = b'\x45'
    F = b'\x46'
    G = b'\x47'
    H = b'\x48'
    I = b'\x49'
    J = b'\x4a'
    K = b'\x4b'
    L = b'\x4c'
    M = b'\x4d'
    N = b'\x4e'
    O = b'\x4f'
    P = b'\x50'
    Q = b'\x51'
    R = b'\x52'
    S = b'\x53'
    T = b'\x54'
    U = b'\x55'
    V = b'\x56'
    W = b'\x57'
    X = b'\x58'
    Y = b'\x59'
    Z = b'\x5a'
    TS_STAR = b'\x5b'
    TS_CANCEL = b'\x5c'
    TS_HASH = b'\x5d'
    TS_0 = b'\x5e'
    CTRL_6 = b'\x5f'
    CTRL_5 = b'\x60'
    TS_A = b'\x61'
    TS_B = b'\x62'
    TS_C = b'\x63'
    TS_D = b'\x64'
    TS_E = b'\x65'
    TS_F = b'\x66'
    TS_G = b'\x67'
    TS_H = b'\x68'
    TS_I = b'\x69'
    TS_J = b'\x6a'
    TS_K = b'\x6b'
    TS_L = b'\x6c'
    TS_M = b'\x6d'
    TS_N = b'\x6e'
    TS_O = b'\x6f'
    TS_P = b'\x70'
    TS_Q = b'\x71'
    TS_R = b'\x72'
    TS_S = b'\x73'
    TS_T = b'\x74'
    TS_U = b'\x75'
    TS_V = b'\x76'
    TS_W = b'\x77'
    TS_X = b'\x78'
    TS_Y = b'\x79'
    TS_Z = b'\x7a'
    CTRL_1 = b'\x7b'
    TS_REPEAT = b'\x7b'
    CTRL_2 = b'\x7c'
    CTRL_3 = b'\x7d'
    TS_SEND = b'\x7d'
    CTRL_4 = b'\x7e'
    CTRL_LEFT = b'\x7f'
    # Two and Three bytes Codes
    CTRL_CANCEL = b'\x19\x23'
    TS_CORRECTION = b'\x19\x27'
    CTRL_8 = b'\x19\x2c'
    CTRL_9 = b'\x19\x2e'
    CTRL_HASH = b'\x19\x2f'
    CTRL_0 = b'\x19\x30'
    CTRL_STAR = b'\x19\x31'
    CTRL_7 = b'\x19\x38'
    TS_NEXT = b'\x19\x41'
    TS_PREVIOUS = b'\x19\x42'
    TS_SUMMARY = b'\x19\x43'
    TS_GUIDE = b'\x19\x48'
    CTRL_CORRECTION = b'\x19\x4b\x63'
    CTRL_RETURN = b'\x19\x6a'
    CTRL_REPEAT = b'\x19\x7a'
    CTRL_NEXT = b'\x19\x7b'

def char(code: VideotexKeyboardCode) -> str:
    """Convert the value to modern Unicode.

    Returns:
        str: ASCII Unicode string.
    """

    videotex_to_unicode_table: dict[VideotexKeyboardCode, str] = {
        VideotexKeyboardCode.CTRL_APOSTROPHE: '\u0000',
        VideotexKeyboardCode.CTRL_A: '\u0001',
        VideotexKeyboardCode.CTRL_B: '\u0002',
        VideotexKeyboardCode.CTRL_C: '\u0003',
        VideotexKeyboardCode.CTRL_D: '\u0004',
        VideotexKeyboardCode.CTRL_E: '\u0005',
        VideotexKeyboardCode.CTRL_F: '\u0006',
        VideotexKeyboardCode.CTRL_G: '\u0007',
        VideotexKeyboardCode.CTRL_H: '\u0008',
        VideotexKeyboardCode.CTRL_I: '\u0009',
        VideotexKeyboardCode.CTRL_J: '\u000a',
        VideotexKeyboardCode.CTRL_COLON: '\u000a',
        VideotexKeyboardCode.CTRL_K: '\u000b',
        VideotexKeyboardCode.CTRL_SEMICOLON: '\u000b',
        VideotexKeyboardCode.CTRL_L: '\u000c',
        VideotexKeyboardCode.CTRL_M: '\u000d',
        VideotexKeyboardCode.CTRL_ENTER: '\u000d',
        VideotexKeyboardCode.CTRL_N: '\u000e',
        VideotexKeyboardCode.CTRL_O: '\u000f',
        VideotexKeyboardCode.CTRL_P: '\u0010',
        VideotexKeyboardCode.CTRL_Q: '\u0011', # DC1 = CURSOR_ON
        VideotexKeyboardCode.CTRL_R: '\u0012', # DC2 = REP
        VideotexKeyboardCode.CTRL_S: '\u0013', # DC3 = SEP
        VideotexKeyboardCode.CTRL_T: '\u0014', # DC4 = CURSOR_OFF
        VideotexKeyboardCode.CTRL_U: '\u0015',
        VideotexKeyboardCode.CTRL_V: '\u0016',
        VideotexKeyboardCode.CTRL_W: '\u0017',
        VideotexKeyboardCode.CTRL_X: '\u0018',
        VideotexKeyboardCode.CTRL_Y: '\u008e', # SS2
        VideotexKeyboardCode.CTRL_Z: '\u001a',
        VideotexKeyboardCode.ESC: '\u001b',
        VideotexKeyboardCode.CTRL_COMMA: '\u001c',
        VideotexKeyboardCode.CTRL_MINUS: '\u008f', # SS3
        VideotexKeyboardCode.CTRL_FULL_STOP: '\u001e',
        VideotexKeyboardCode.CTRL_QUESTION_MARK: '\u001f',
        VideotexKeyboardCode.SPACE_BAR: ' ',
        VideotexKeyboardCode.TS_1: '!',
        VideotexKeyboardCode.TS_2: '"',
        VideotexKeyboardCode.HASH: '#',
        VideotexKeyboardCode.TS_3: '#',
        VideotexKeyboardCode.TS_4: '$',
        VideotexKeyboardCode.TS_5: '%',
        VideotexKeyboardCode.TS_6: '&',
        VideotexKeyboardCode.APOSTROPHE: "'",
        VideotexKeyboardCode.TS_7: "'",
        VideotexKeyboardCode.TS_8: '(',
        VideotexKeyboardCode.TS_9: ')',
        VideotexKeyboardCode.STAR: '*',
        VideotexKeyboardCode.TS_COLON: '*',
        VideotexKeyboardCode.TS_SEMICOLON: '+',
        VideotexKeyboardCode.COMMA: ',',
        VideotexKeyboardCode.MINUS: '-',
        VideotexKeyboardCode.FULL_STOP: '.',
        VideotexKeyboardCode.TS_QUESTION_MARK: '/',
        VideotexKeyboardCode.NUM_0: '0',
        VideotexKeyboardCode.NUM_1: '1',
        VideotexKeyboardCode.NUM_2: '2',
        VideotexKeyboardCode.NUM_3: '3',
        VideotexKeyboardCode.NUM_4: '4',
        VideotexKeyboardCode.NUM_5: '5',
        VideotexKeyboardCode.NUM_6: '6',
        VideotexKeyboardCode.NUM_7: '7',
        VideotexKeyboardCode.NUM_8: '8',
        VideotexKeyboardCode.NUM_9: '9',
        VideotexKeyboardCode.COLON: ':',
        VideotexKeyboardCode.SEMICOLON: ';',
        VideotexKeyboardCode.TS_COMMA: '<',
        VideotexKeyboardCode.TS_MINUS: '=',
        VideotexKeyboardCode.TS_FULL_STOP: '>',
        VideotexKeyboardCode.QUESTION_MARK: '?',
        VideotexKeyboardCode.TS_APOSTROPHE: '@',
        VideotexKeyboardCode.A: 'A',
        VideotexKeyboardCode.B: 'B',
        VideotexKeyboardCode.C: 'C',
        VideotexKeyboardCode.D: 'D',
        VideotexKeyboardCode.E: 'E',
        VideotexKeyboardCode.F: 'F',
        VideotexKeyboardCode.G: 'G',
        VideotexKeyboardCode.H: 'H',
        VideotexKeyboardCode.I: 'I',
        VideotexKeyboardCode.J: 'J',
        VideotexKeyboardCode.K: 'K',
        VideotexKeyboardCode.L: 'L',
        VideotexKeyboardCode.M: 'M',
        VideotexKeyboardCode.N: 'N',
        VideotexKeyboardCode.O: 'O',
        VideotexKeyboardCode.P: 'P',
        VideotexKeyboardCode.Q: 'Q',
        VideotexKeyboardCode.R: 'R',
        VideotexKeyboardCode.S: 'S',
        VideotexKeyboardCode.T: 'T',
        VideotexKeyboardCode.U: 'U',
        VideotexKeyboardCode.V: 'V',
        VideotexKeyboardCode.W: 'W',
        VideotexKeyboardCode.X: 'X',
        VideotexKeyboardCode.Y: 'Y',
        VideotexKeyboardCode.Z: 'Z',
        VideotexKeyboardCode.TS_STAR: '[',
        VideotexKeyboardCode.TS_CANCEL: '\\',
        VideotexKeyboardCode.TS_HASH: ']',
        VideotexKeyboardCode.TS_0: '↑',
        VideotexKeyboardCode.CTRL_6: '_',
        VideotexKeyboardCode.CTRL_5: '-',
        VideotexKeyboardCode.TS_A: 'a',
        VideotexKeyboardCode.TS_B: 'b',
        VideotexKeyboardCode.TS_C: 'c',
        VideotexKeyboardCode.TS_D: 'd',
        VideotexKeyboardCode.TS_E: 'e',
        VideotexKeyboardCode.TS_F: 'f',
        VideotexKeyboardCode.TS_G: 'g',
        VideotexKeyboardCode.TS_H: 'h',
        VideotexKeyboardCode.TS_I: 'i',
        VideotexKeyboardCode.TS_J: 'j',
        VideotexKeyboardCode.TS_K: 'k',
        VideotexKeyboardCode.TS_L: 'l',
        VideotexKeyboardCode.TS_M: 'm',
        VideotexKeyboardCode.TS_N: 'n',
        VideotexKeyboardCode.TS_O: 'o',
        VideotexKeyboardCode.TS_P: 'p',
        VideotexKeyboardCode.TS_Q: 'q',
        VideotexKeyboardCode.TS_R: 'r',
        VideotexKeyboardCode.TS_S: 's',
        VideotexKeyboardCode.TS_T: 't',
        VideotexKeyboardCode.TS_U: 'u',
        VideotexKeyboardCode.TS_V: 'v',
        VideotexKeyboardCode.TS_W: 'w',
        VideotexKeyboardCode.TS_X: 'x',
        VideotexKeyboardCode.TS_Y: 'y',
        VideotexKeyboardCode.TS_Z: 'z',
        VideotexKeyboardCode.CTRL_1: '|',
        VideotexKeyboardCode.TS_REPEAT: '|',
        VideotexKeyboardCode.CTRL_2: '|',
        VideotexKeyboardCode.CTRL_3: '|',
        VideotexKeyboardCode.TS_SEND: '|',
        VideotexKeyboardCode.CTRL_4: '_',
        VideotexKeyboardCode.CTRL_LEFT: '█',
        # Two and Three bytes Codes
        VideotexKeyboardCode.CTRL_CANCEL: '£',
        VideotexKeyboardCode.TS_CORRECTION: '§',
        VideotexKeyboardCode.CTRL_8: '←',
        VideotexKeyboardCode.CTRL_9: '→',
        VideotexKeyboardCode.CTRL_HASH: '↓',
        VideotexKeyboardCode.CTRL_0: '°',
        VideotexKeyboardCode.CTRL_STAR: '±',
        VideotexKeyboardCode.CTRL_7: '÷',
        VideotexKeyboardCode.TS_NEXT: '`',
        VideotexKeyboardCode.TS_PREVIOUS: '´',
        VideotexKeyboardCode.TS_SUMMARY: '^',
        VideotexKeyboardCode.TS_GUIDE: '¨',
        VideotexKeyboardCode.CTRL_CORRECTION: 'ç',
        VideotexKeyboardCode.CTRL_RETURN: 'Œ',
        VideotexKeyboardCode.CTRL_REPEAT: 'œ',
        VideotexKeyboardCode.CTRL_NEXT: 'β'
    }

    return videotex_to_unicode_table.get(code, '')
