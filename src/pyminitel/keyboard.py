from aenum import NamedConstant

class KeyboardCode(NamedConstant):
    def char(self) -> str:
        raise NotImplementedError()

class FilterKeyboardCode(KeyboardCode):
    Any_Keys = 1
    Printable_Keys = 2
    Other_Keys = 3
    No_Keys = 4

    def char(self):
        return ''

class FunctionKeyboardCode(KeyboardCode):
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
        return ''

class CursorKeyboardCode(KeyboardCode):
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
        return ''

class VideotexKeyboardCode(KeyboardCode):
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
    Spacebar = b'\x20'
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

    def char(self) -> str:
        """ Convert the value to modern Unicode """
        match self:
            case self.Ctrl_Apostrophe:
                return '\u0000'
            case self.Ctrl_A:
                return '\u0001'
            case self.Ctrl_B:
                return '\u0002'
            case self.Ctrl_C:
                return '\u0003'
            case self.Ctrl_D:
                return '\u0004'
            case self.Ctrl_E:
                return '\u0005'
            case self.Ctrl_F:
                return '\u0006'
            case self.Ctrl_G:
                return '\u0007'
            case self.Ctrl_H:
                return '\u0008'
            case self.Ctrl_I:
                return '\u0009'
            case self.Ctrl_J:
                return '\u000a'
            case self.Ctrl_Colon:
                return '\u000a'
            case self.Ctrl_K:
                return '\u000b'
            case self.Ctrl_Semicolon:
                return '\u000b'
            case self.Ctrl_L:
                return '\u000c'
            case self.Ctrl_M:
                return '\u000d'
            case self.Ctrl_Enter:
                return '\u000d'
            case self.Ctrl_N:
                return '\u000e'
            case self.Ctrl_O:
                return '\u000f'
            case self.Ctrl_P:
                return '\u0010'
            case self.Ctrl_Q:
                return '\u0011' # DC1 = CURSOR_ON
            case self.Ctrl_R:
                return '\u0012' # DC2 = REP
            case self.Ctrl_S:
                return '\u0013' # DC3 = SEP
            case self.Ctrl_T:
                return '\u0014' # DC4 = CURSOR_OFF
            case self.Ctrl_U:
                return '\u0015'
            case self.Ctrl_V:
                return '\u0016'
            case self.Ctrl_W:
                return '\u0017'
            case self.Ctrl_X:
                return '\u0018'
            case self.Ctrl_Y:
                return '\u008e' # SS2
            case self.Ctrl_Z:
                return '\u001a'
            case self.Esc:
                return '\u001b'
            case self.Ctrl_Comma:
                return '\u001c'
            case self.Ctrl_Minus:
                return '\u008f' # SS3
            case self.Ctrl_Full_Stop:
                return '\u001e'
            case self.Ctrl_Question_Mark:
                return '\u001f'
            case self.Spacebar:
                return ' '
            case self.TS_1:
                return '!'
            case self.TS_2:
                return '"'
            case self.Hash:
                return '#'
            case self.TS_3:
                return '#'
            case self.TS_4:
                return '$'
            case self.TS_5:
                return '%'
            case self.TS_6:
                return '&'
            case self.Apostrophe:
                return "'"
            case self.TS_7:
                return "'"
            case self.TS_8:
                return '('
            case self.TS_9:
                return ')'
            case self.Star:
                return '*'
            case self.TS_Colon:
                return '*'
            case self.TS_Semicolon:
                return '+'
            case self.Comma:
                return ','
            case self.Minus:
                return '-'
            case self.Full_Stop:
                return '.'
            case self.TS_Question_Mark:
                return '/'
            case self.Num_0:
                return '0'
            case self.Num_1:
                return '1'
            case self.Num_2:
                return '2'
            case self.Num_3:
                return '3'
            case self.Num_4:
                return '4'
            case self.Num_5:
                return '5'
            case self.Num_6:
                return '6'
            case self.Num_7:
                return '7'
            case self.Num_8:
                return '8'
            case self.Num_9:
                return '9'
            case self.Colon:
                return ':'
            case self.Semicolon:
                return ';'
            case self.TS_Comma:
                return '<'
            case self.TS_Minus:
                return '='
            case self.TS_Full_Stop:
                return '>'
            case self.Question_Mark:
                return '?'
            case self.TS_Apostrophe:
                return '@'
            case self.A:
                return 'A'
            case self.B:
                return 'B'
            case self.C:
                return 'C'
            case self.D:
                return 'D'
            case self.E:
                return 'E'
            case self.F:
                return 'F'
            case self.G:
                return 'G'
            case self.H:
                return 'H'
            case self.I:
                return 'I'
            case self.J:
                return 'J'
            case self.K:
                return 'K'
            case self.L:
                return 'L'
            case self.M:
                return 'M'
            case self.N:
                return 'N'
            case self.O:
                return 'O'
            case self.P:
                return 'P'
            case self.Q:
                return 'Q'
            case self.R:
                return 'R'
            case self.S:
                return 'S'
            case self.T:
                return 'T'
            case self.U:
                return 'U'
            case self.V:
                return 'V'
            case self.W:
                return 'W'
            case self.X:
                return 'X'
            case self.Y:
                return 'Y'
            case self.Z:
                return 'Z'
            case self.TS_Star:
                return '['
            case self.TS_CANCEL:
                return '\\'
            case self.TS_Hash:
                return ']'
            case self.TS_0:
                return '↑'
            case self.Ctrl_6:
                return '_'
            case self.Ctrl_5:
                return '-'
            case self.TS_A:
                return 'a'
            case self.TS_B:
                return 'b'
            case self.TS_C:
                return 'c'
            case self.TS_D:
                return 'd'
            case self.TS_E:
                return 'e'
            case self.TS_F:
                return 'f'
            case self.TS_G:
                return 'g'
            case self.TS_H:
                return 'h'
            case self.TS_I:
                return 'i'
            case self.TS_J:
                return 'j'
            case self.TS_K:
                return 'k'
            case self.TS_L:
                return 'l'
            case self.TS_M:
                return 'm'
            case self.TS_N:
                return 'n'
            case self.TS_O:
                return 'o'
            case self.TS_P:
                return 'p'
            case self.TS_Q:
                return 'q'
            case self.TS_R:
                return 'r'
            case self.TS_S:
                return 's'
            case self.TS_T:
                return 't'
            case self.TS_U:
                return 'u'
            case self.TS_V:
                return 'v'
            case self.TS_W:
                return 'w'
            case self.TS_X:
                return 'x'
            case self.TS_Y:
                return 'y'
            case self.TS_Z:
                return 'z'
            case self.Ctrl_1:
                return '|'
            case self.TS_Repeat:
                return '|'
            case self.Ctrl_2:
                return '|'
            case self.Ctrl_3:
                return '|'
            case self.TS_Send:
                return '|'
            case self.Ctrl_4:
                return '_'
            case self.Ctrl_Left:
                return '█'
            # Two and Three bytes Codes
            case self.Ctrl_Cancel:
                return '£'
            case self.TS_Correction:
                return '§'
            case self.Ctrl_8:
                return '←'
            case self.Ctrl_9:
                return '→'
            case self.Ctrl_Hash:
                return '↓'
            case self.Ctrl_0:
                return '°'
            case self.Ctrl_Star:
                return '±'
            case self.Ctrl_7:
                return '÷'
            case self.TS_Next:
                return '`'
            case self.TS_Previous:
                return '´'
            case self.TS_Summary:
                return '^'
            case self.TS_Guide:
                return '¨'
            case self.Ctrl_Correction:
                return 'ç'
            case self.Ctrl_Return:
                return 'Œ'
            case self.Ctrl_Repeat:
                return 'œ'
            case self.Ctrl_Next:
                return 'β'

        return ''
