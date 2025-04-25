"""
keyboard.py

This module contains keyboard's description table and filters for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

from aenum import NamedConstant # type: ignore

class KeyboardCode(NamedConstant):
    """KeyboardCode class.

    Abstract class for classes below and binding typing.
    Args:
        NamedConstant (_type_): NamedConstant
    """
    def char(self) -> str:
        raise NotImplementedError()

class FilterKeyboardCode(KeyboardCode):
    """FilterKeyboardCode class.

    Define general filters to bind a callback on keyboard event.

    Args:
        KeyboardCode (_type_): KeyboardCode NamedConstant
    """
    Any_Keys = 1
    Printable_Keys = 2
    Other_Keys = 3
    No_Keys = 4

    def char(self):
        """Unused method for this KeyboardCode.

        Returns:
            _type_: Empty str.
        """
        return ''

class FunctionKeyboardCode(KeyboardCode):
    """FunctionKeyboardCode class.

    Defines Minitel's Function specific keyboard sequences,
    allows to bind the function keys pressing.

    Args:
        KeyboardCode (_type_): KeyboardCode NamedConstant
    """
    Send = b'\x13\x41'
    Previous = b'\x13\x42'
    Repeat = b'\x13\x43'
    Guide = b'\x13\x44'
    Cancel = b'\x13\x45'
    Summary = b'\x13\x46'
    Correction = b'\x13\x47'
    Next = b'\x13\x48'
    Connection_Switch = b'\x13\x49' # To Modem
    TS_Connection_Switch = b'\x13\x49' # To Din
    # Ctrl_Connection_Switch = b'' # Break send to Din or Modem

    def char(self) -> str:
        """Unused method for FunctionKeyboardCode.

        Returns:
            _type_: Empty str.
        """
        return ''

class CursorKeyboardCode(KeyboardCode):
    """CursorKeyboardCode class.

    Defines Minitel's Cursor specific keyboard sequences,
    allows to bind the cursor keys pressing.

    Args:
        KeyboardCode (_type_): KeyboardCode NamedConstant
    """
    Up = b'\x1b\x5b\x41'
    TS_Up = b'\x1b\x5b\x4d' # Delete line
    Down = b'\x1b\x5b\x42'
    TS_Down = b'\x1b\x5b\x4c' # Insert line
    Right = b'\x1b\x5b\x43'
    TS_Right_Start = b'\x1b\x5b\x34\x68' # Start character insertion
    TS_Right_Stop = b'\x1b\x5b\x34\x6c' # Stop character insertion
    Left = b'\x1b\x5b\x44'
    TS_Left = b'\x1b\x5b\x50' # Delete character
    Ctrl_Left = b'\x7f' # DEL
    Enter = b'\x0d' # CR
    TS_Enter = b'\x1b\x5b\x48' # Home
    Ctrl_Enter = b'\x1b\x5b\x32\x4a' # Clear page

    def char(self) -> str:
        """Unused method for CursorKeyboardCode.

        Returns:
            _type_: Empty str.
        """
        return ''

class VideotexKeyboardCode(KeyboardCode):
    """VideotexKeyboardCode class.

    Defines Minitel's videotex specific keyboard sequences,
    allows to bind the alphanumerical keys pressing.

    Args:
        KeyboardCode (_type_): KeyboardCode NamedConstant
    """
    Ctrl_Apostrophe = b'\x00'
    Ctrl_A = b'\x01'
    Ctrl_B = b'\x02'
    Ctrl_C = b'\x03'
    Ctrl_D = b'\x04'
    Ctrl_E = b'\x05'
    Ctrl_F = b'\x06'
    Ctrl_G = b'\x07'
    Ctrl_H = b'\x08'
    Ctrl_I = b'\x09'
    Ctrl_J = b'\x0a'
    Ctrl_Colon = b'\x0a'
    Ctrl_K = b'\x0b'
    Ctrl_Semicolon = b'\x0b'
    Ctrl_L = b'\x0c'
    Ctrl_M = b'\x0d'
    Ctrl_Enter = b'\x0d'
    Ctrl_N = b'\x0e'
    Ctrl_O = b'\x0f'
    Ctrl_P = b'\x10'
    Ctrl_Q = b'\x11'
    Ctrl_R = b'\x12'
    Ctrl_S = b'\x13'
    Ctrl_T = b'\x14'
    Ctrl_U = b'\x15'
    Ctrl_V = b'\x16'
    Ctrl_W = b'\x17'
    Ctrl_X = b'\x18'
    Ctrl_Y = b'\x19'
    Ctrl_Z = b'\x1a'
    Esc = b'\x1b'
    Ctrl_Comma = b'\x1c'
    Ctrl_Minus = b'\x1d'
    Ctrl_Full_Stop = b'\x1e'
    Ctrl_Question_Mark = b'\x1f'
    SpaceBar = b'\x20'
    TS_1 = b'\x21'
    TS_2 = b'\x22'
    Hash = b'\x23'
    TS_3 = b'\x23'
    TS_4 = b'\x24'
    TS_5 = b'\x25'
    TS_6 = b'\x26'
    Apostrophe = b'\x27'
    TS_7 = b'\x27'
    TS_8 = b'\x28'
    TS_9 = b'\x29'
    Star = b'\x2a'
    TS_Colon = b'\x2a'
    TS_Semicolon = b'\x2b'
    Comma = b'\x2c'
    Minus = b'\x2d'
    Full_Stop = b'\x2e'
    TS_Question_Mark = b'\x2f'
    Num_0 = b'\x30'
    Num_1 = b'\x31'
    Num_2 = b'\x32'
    Num_3 = b'\x33'
    Num_4 = b'\x34'
    Num_5 = b'\x35'
    Num_6 = b'\x36'
    Num_7 = b'\x37'
    Num_8 = b'\x38'
    Num_9 = b'\x39'
    Colon = b'\x3a'
    Semicolon = b'\x3b'
    TS_Comma = b'\x3c'
    TS_Minus = b'\x3d'
    TS_Full_Stop = b'\x3e'
    Question_Mark = b'\x3f'
    TS_Apostrophe = b'\x40'
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
    TS_Star = b'\x5b'
    TS_CANCEL = b'\x5c'
    TS_Hash = b'\x5d'
    TS_0 = b'\x5e'
    Ctrl_6 = b'\x5f'
    Ctrl_5 = b'\x60'
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
    Ctrl_1 = b'\x7b'
    TS_Repeat = b'\x7b'
    Ctrl_2 = b'\x7c'
    Ctrl_3 = b'\x7d'
    TS_Send = b'\x7d'
    Ctrl_4 = b'\x7e'
    Ctrl_Left = b'\x7f'
    # Two and Three bytes Codes
    Ctrl_Cancel = b'\x19\x23'
    TS_Correction = b'\x19\x27'
    Ctrl_8 = b'\x19\x2c'
    Ctrl_9 = b'\x19\x2e'
    Ctrl_Hash = b'\x19\x2f'
    Ctrl_0 = b'\x19\x30'
    Ctrl_Star = b'\x19\x31'
    Ctrl_7 = b'\x19\x38'
    TS_Next = b'\x19\x41'
    TS_Previous = b'\x19\x42'
    TS_Summary = b'\x19\x43'
    TS_Guide = b'\x19\x48'
    Ctrl_Correction = b'\x19\x4b\x63'
    Ctrl_Return = b'\x19\x6a'
    Ctrl_Repeat = b'\x19\x7a'
    Ctrl_Next = b'\x19\x7b'

    videotext_to_unicode_table = {
        Ctrl_Apostrophe: '\u0000',
        Ctrl_A: '\u0001',
        Ctrl_B: '\u0002',
        Ctrl_C: '\u0003',
        Ctrl_D: '\u0004',
        Ctrl_E: '\u0005',
        Ctrl_F: '\u0006',
        Ctrl_G: '\u0007',
        Ctrl_H: '\u0008',
        Ctrl_I: '\u0009',
        Ctrl_J: '\u000a',
        Ctrl_Colon: '\u000a',
        Ctrl_K: '\u000b',
        Ctrl_Semicolon: '\u000b',
        Ctrl_L: '\u000c',
        Ctrl_M: '\u000d',
        Ctrl_Enter: '\u000d',
        Ctrl_N: '\u000e',
        Ctrl_O: '\u000f',
        Ctrl_P: '\u0010',
        Ctrl_Q: '\u0011', # DC1 = CURSOR_ON
        Ctrl_R: '\u0012', # DC2 = REP
        Ctrl_S: '\u0013', # DC3 = SEP
        Ctrl_T: '\u0014', # DC4 = CURSOR_OFF
        Ctrl_U: '\u0015',
        Ctrl_V: '\u0016',
        Ctrl_W: '\u0017',
        Ctrl_X: '\u0018',
        Ctrl_Y: '\u008e', # SS2
        Ctrl_Z: '\u001a',
        Esc: '\u001b',
        Ctrl_Comma: '\u001c',
        Ctrl_Minus: '\u008f', # SS3
        Ctrl_Full_Stop: '\u001e',
        Ctrl_Question_Mark: '\u001f',
        SpaceBar: ' ',
        TS_1: '!',
        TS_2: '"',
        Hash: '#',
        TS_3: '#',
        TS_4: '$',
        TS_5: '%',
        TS_6: '&',
        Apostrophe: "'",
        TS_7: "'",
        TS_8: '(',
        TS_9: ')',
        Star: '*',
        TS_Colon: '*',
        TS_Semicolon: '+',
        Comma: ',',
        Minus: '-',
        Full_Stop: '.',
        TS_Question_Mark: '/',
        Num_0: '0',
        Num_1: '1',
        Num_2: '2',
        Num_3: '3',
        Num_4: '4',
        Num_5: '5',
        Num_6: '6',
        Num_7: '7',
        Num_8: '8',
        Num_9: '9',
        Colon: ':',
        Semicolon: ';',
        TS_Comma: '<',
        TS_Minus: '=',
        TS_Full_Stop: '>',
        Question_Mark: '?',
        TS_Apostrophe: '@',
        A: 'A',
        B: 'B',
        C: 'C',
        D: 'D',
        E: 'E',
        F: 'F',
        G: 'G',
        H: 'H',
        I: 'I',
        J: 'J',
        K: 'K',
        L: 'L',
        M: 'M',
        N: 'N',
        O: 'O',
        P: 'P',
        Q: 'Q',
        R: 'R',
        S: 'S',
        T: 'T',
        U: 'U',
        V: 'V',
        W: 'W',
        X: 'X',
        Y: 'Y',
        Z: 'Z',
        TS_Star: '[',
        TS_CANCEL: '\\',
        TS_Hash: ']',
        TS_0: '↑',
        Ctrl_6: '_',
        Ctrl_5: '-',
        TS_A: 'a',
        TS_B: 'b',
        TS_C: 'c',
        TS_D: 'd',
        TS_E: 'e',
        TS_F: 'f',
        TS_G: 'g',
        TS_H: 'h',
        TS_I: 'i',
        TS_J: 'j',
        TS_K: 'k',
        TS_L: 'l',
        TS_M: 'm',
        TS_N: 'n',
        TS_O: 'o',
        TS_P: 'p',
        TS_Q: 'q',
        TS_R: 'r',
        TS_S: 's',
        TS_T: 't',
        TS_U: 'u',
        TS_V: 'v',
        TS_W: 'w',
        TS_X: 'x',
        TS_Y: 'y',
        TS_Z: 'z',
        Ctrl_1: '|',
        TS_Repeat: '|',
        Ctrl_2: '|',
        Ctrl_3: '|',
        TS_Send: '|',
        Ctrl_4: '_',
        Ctrl_Left: '█',
        # Two and Three bytes Codes
        Ctrl_Cancel: '£',
        TS_Correction: '§',
        Ctrl_8: '←',
        Ctrl_9: '→',
        Ctrl_Hash: '↓',
        Ctrl_0: '°',
        Ctrl_Star: '±',
        Ctrl_7: '÷',
        TS_Next: '`',
        TS_Previous: '´',
        TS_Summary: '^',
        TS_Guide: '¨',
        Ctrl_Correction: 'ç',
        Ctrl_Return: 'Œ',
        Ctrl_Repeat: 'œ',
        Ctrl_Next: 'β'
    }   

    def char(self) -> str:
        """Convert the value to modern Unicode.

        Returns:
            str: ASCII Unicode string.
        """

        if self in VideotexKeyboardCode.videotext_to_unicode_table:
            return VideotexKeyboardCode.videotext_to_unicode_table[self]
        return ''
