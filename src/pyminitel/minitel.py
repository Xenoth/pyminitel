import sys, time

from enum import Enum
from serial import Serial

import pyminitel.alphanumerical as alphanumerical
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.mode import Mode
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import Mode

class Minitel:

    din = None

    layout = None

    __mode = None
    __vm = None

    __zone_attribute = None

    class Bauderate(Enum):
        MINIMAL = 75  # 75 Bauds
        LOW = 300      # 300 Bauds
        MEDIUM = 1200   # 1200 Bauds
        HIGH = 4800     # 4800 Bauds

    ESC = b'\x1b'
    US = b'\x1F'
    
    START = b'\x69'
    STOP = b'\x6a'

    ROULEAU = b'\x43'
    PROCEDURE = b'\x44'
    MINUSCULE = b'\x45'

    BEL = b'\x07'

    SEP = b'\x13'
    PRO1 = ESC + b'\x39'
    PRO2 = ESC + b'\x3a'
    PRO3 = ESC + b'\x3b'
    PROG = b'\x6B'

    TO = b'\x62'
    FROM = b'\x63'

    SCREEN_STATUS_BITFIELD = 1 << 0
    KEYBOARD_STATUS_BITFIELD = 1 << 1
    MODEM_STATUS_BITFIELD = 1 << 2
    CONNECTOR_STATUS_BITFIELD = 1 << 3

    COMMAND_CODE_ENABLE = b'\x64'
    COMMAND_CODE_DISABLE = b'\x65'

    STATUS_PROTOCOL_REQUEST = b'\x76'
    STATUS_PROTOCOL_ANSWER = b'\x77'

    BITFIELD_STATUS_PROTOCOL_D1 = 1 << 0
    BITFIELD_STATUS_PROTOCOL_D2 = 1 << 1
    BITFIELD_STATUS_PROTOCOL_A1 = 1 << 2
    BITFIELD_STATUS_PROTOCOL_A2 = 1 << 3
    BITFIELD_STATUS_PROTOCOL_PAD = 1 << 4

    class Module(Enum):
        SCREEN = 1
        KEYBOARD = 2
        MODEM = 3
        CONNECTOR = 4

    class IO(Enum):
        IN = 1
        OUT = 2

    IO_CODES = {
        Module.SCREEN: { IO.OUT: b'\x50', IO.IN: b'\x58' },
        Module.KEYBOARD: { IO.OUT: b'\x51', IO.IN: b'\x59' },
        Module.MODEM: { IO.OUT: b'\x52', IO.IN: b'\x5a' },
        Module.CONNECTOR: { IO.OUT: b'\x53', IO.IN: b'\x5b' },
    }

    class KeyboardMode(Enum):
        ETENDU = b'\x41'
        C0 = b'\x43'


    class TextAlign(Enum):
        LEFT = 1
        CENTER = 2
        RIGHT = 3

    def __init__(self, port, bauderate = Bauderate.MEDIUM, mode: Mode = Mode.VIDEOTEX, vm: VisualizationModule = VisualizationModule.VGP5):
        
        self.din = Serial(port=port, baudrate=bauderate.value, bytesize=7, parity='E', stopbits=1)
        self.layout = Layout(self.din)
        self.__mode = mode
        self.__vm = vm
        self.__zone_attribute = ZoneAttributes()

    def switchReceiverTransmitter(self, receiver: Module, transmitter: Module, on: bool = True) -> dict:
        # TODO - TEST
        if (
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.CONNECTOR) or
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.MODEM) or
            (receiver == self.Module.CONNECTOR and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.CONNECTOR and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.MODEM and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.SCREEN)
        ):
            print('Error - Switching ' + transmitter.name + ' -> ' + receiver.name + 'is not possible', file=sys.stderr)
            pass
        
        OFF = b'\x60'
        ON = b'\x61'

        command = self.PRO3
        command += ON if on else OFF
        command += self.IO_CODES[receiver.value][self.IO.IN] + self.IO_CODES[transmitter.value][self.IO.OUT]


        self.din.flush()
        self.din.write(command)
        self.din.read()
        status = b'\x48'
        answer = self.PRO2 + self.FROM + self.IO_CODES[receiver.value][self.IO.OUT] + status

        answer = self.din.read(5)

        if answer[0:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[receiver.value][self.IO.OUT]:
            print("Error - Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None
        
        return {
            self.Module.SCREEN: answer[4:5] & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: answer[4:5] & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: answer[4:5] & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: answer[4:5] & self.CONNECTOR_STATUS_BITFIELD,
        }

    def blockModule(self, module: Module):
        # TODO - TEST
        self.switchReceiverTransmitter(module, module, False)

    def unblockModule(self, module: Module):
        # TODO - TEST
        self.switchReceiverTransmitter(module, module, True)

    def getModuleIOStatus(self, module: Module, io: IO) -> dict:
        # TODO - TEST
        command = self.PRO2 + self.TO + self.IO_CODES[module][io]

        self.din.write(command)
        answer = self.din.read(5)

        if answer[0:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[module.value][io.value]:
            print("Error - Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None

        return {
            self.Module.SCREEN: answer[4:5] & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: answer[4:5] & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: answer[4:5] & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: answer[4:5] & self.CONNECTOR_STATUS_BITFIELD,
        }
    
    def setModuleDiffusion(self, module: Module, activate: bool = True):
        # TODO - TEST
        command = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module.value][self.IO.IN]

        print(command.hex())

    def setModuleACK(self, module: Module, activate: bool = True):
        # TODO - TEST
        command = self.PRO2
        command += self.COMMAND_CODE_ENABLE_ if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module.value][self.IO.OUT]

        print(command.hex())

    def getProtocolStatus(self) -> dict:
        # TODO - TEST
        command = self.PRO1 + self.STATUS_PROTOCOL_REQUEST

        print(command.hex())

        # TODO - MOCKED
        status = b'\x4f'
        answer = self.PRO2 + self.STATUS_PROTOCOL_ANSWER + status

        if answer[0:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
            print("Error - Response from getStatusProtocol's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None
        
        return {
            'D1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D1,
            'D2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D2,
            'A1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A1,
            'A2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A2,
            'PAD_X3_COMPATIBLE': answer[4] & self.BITFIELD_STATUS_PROTOCOL_PAD,
        } 

    def setProtocolTransparency(self, n: int) -> bool:
        # TODO - TEST
        if n < 1 or n > 127:
            print("Error - Invalid Argument, n should be between 1-127, got " + n + "", file=sys.stderr)
            return False

        bit_n = n.to_bytes(1, 'little')
        bit_n |= (1<<7)

        command = self.PRO2 + b'\x66' + bit_n

        # TODO - MOCKED
        answer = self.SEP + b'\x57'

        if answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            print("Error - Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return False
        
        return True

    def getMinitelInfo(self) -> tuple:
        print("Not Implemented Yet")
        pass

    def getCursorPosition(self) -> tuple:
        command = self.ESC + b'\x61'

        self.din.write(command)

        answer = self.din.read(3)

        if answer[0:1] != self.US:
            print("Error - Response from getCursorPosition's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return -1, -1
        
        print('answer: ' + answer.hex())

        mask = 63

        return int.from_bytes(answer[1:2]) & mask, int.from_bytes(answer[2:3]) & mask

    def showCursor(self):
        command = b'\x11'
        self.din.write(command)

    def hideCursor(self):
        command = b'\x14'
        self.din.write(command)

    def connectModem(self):
        # TODO - TEST
        command = self.PRO1 + b'\x68'

        self.din.write(command)

    def disconnectModem(self) -> bool:
        # TODO - TEST
        command = self.PRO1 + b'\x67'

        self.din.write(command)

    def setECP(self, enable: bool = False) -> bool:
        print("Not Implemented Yet")
        pass 

    def reverseModem(self) -> bool:
        print("Not Implemented Yet")
        pass 

    def setConnectorBauderate(self, emission_bauderate = Bauderate.MEDIUM, reception_bauderate = Bauderate.MEDIUM) -> tuple:
        # TODO - MINIBEL1B MODEL
        if emission_bauderate != reception_bauderate:
            print("Warning - Emission and Reception Bauderate should be symetrical for Minitel 1B Models", file=sys.stderr)
        
        prog_byte = 3 << 6
        prog_byte |= emission_bauderate.value << 3
        prog_byte |= reception_bauderate.value
        
        command = b'' + self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        print(command.hex())

        # TODO - MOCKED
        status = b'\xe4'
        answer = b'' + self.PRO2 + b'\x75' + status

        if answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
            print("Error - Response from setConnectorBauderate's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None, None

        new_emission_speed = int.from_bytes(answer[3:4], 'little') & (7 << 3)
        new_emission_speed = new_emission_speed >> 3
        new_reception_speed = int.from_bytes(answer[3:4], 'little') & 7

        if new_reception_speed != reception_bauderate.value or new_emission_speed != emission_bauderate.value:
            print("Warning - Bauderates not updated, old config returned", file=sys.stderr)

        return self.Bauderate(new_emission_speed), self.Bauderate(new_reception_speed)


    def getConnectorBauderate(self) -> Bauderate:
        print("Not Implemented Yet")
        pass

    def setKeyboardMode(self, mode: KeyboardMode) -> KeyboardMode:
        print("Not Implemented Yet")
        pass

    def enableKeyboard(self) -> bool:
        print("Not Implemented Yet")
        pass

    def disableKeyboard(self) -> bool:
        print("Not Implemented Yet")
        pass

    def getKeyboardMode(self) -> KeyboardMode:
        print("Not Implemented Yet")
        pass

    def setKeyCapsLock(self, enable: bool) -> bool: 
        print("Not Implemented Yet")
        pass

    def setScreenPageMode(self) -> bool:
        command = self.PRO2 + self.STOP + self.ROULEAU

        self.din.write(command)
        answer = self.din.read(4)

        if answer[0:2] !=  self.PRO2:
            print('Warning - setScreenPageMode might have failed, excepted x13x56 but got ' + answer.hex())

        print(str(answer[2:4]))

    def setScreenRollMode(self) -> bool:
        command = self.PRO2 + self.START + self.ROULEAU

        self.din.write(command)
        answer = self.din.read(4)

        if answer[0:2] !=  self.PRO2:
            print('Warning - setScreenRollMode might have failed, excepted x13x56 but got ' + answer.hex())

        print(str(answer[2:4]))

    class CopyMode(Enum):
        FR = b'\x6a'
        USA = b'\x6b'

    def copyScreenToConnector(self, mode: CopyMode = CopyMode.FR) -> bool:
        print("Not Implemented Yet")
        pass

    def getModulesFunctionalStates(self) -> dict:
        print("Not Implemented Yet")
        pass
    

    def setTextAttributes(self, color: CharacterColor = None, blinking: bool = None, double_height: bool = None, double_width: bool = None):
        
        bytes_data = b''
        
        if color is not None:
            bytes_data += ESC + color.value

        if blinking is not None:
            if blinking:
                bytes_data += ESC + BLINKING
            else:
                bytes_data += ESC + FIXED

        if double_height is not None or double_width is not None:
            if double_width == double_height:
                if double_height:
                    bytes_data += ESC + DOUBLE_SIZE
                else:
                    bytes_data += ESC + NORMAL_SIZE
            else:
                if double_height:
                    bytes_data += ESC + DOUBLE_HEIGHT
                elif double_width:
                    bytes_data += ESC + DOUBLE_WIDTH

        self.din.write(bytes_data)

    def resetTextAttributes(self):
        bytes_data = ESC + CharacterColor.WHITE.value + ESC + FIXED + ESC + NORMAL_SIZE

        self.din.write(bytes_data)

    def setZoneAttributes(self, color: BackgroundColor = None, masking: bool = None, highlight: bool = None):
        bytes_data = b''

        if color is not None:
            bytes_data += ESC + color.value 
            self.__zone_attribute.background = color

        if masking is not None:
            if masking:
                bytes_data += ESC + MASKING
                self.__zone_attribute.masking = True
            else:
                bytes_data += ESC + UNMASKING
                self.__zone_attribute.masking = False
        
        if highlight is not None:
            if highlight:
                bytes_data += ESC + START_HIGHLIGHTING
                self.__zone_attribute.highlight = True
            else:
                bytes_data += ESC + END_HIGHLIGHTING
                self.__zone_attribute.highlight = False
    
        bytes_data += DELIMETER

        self.din.write(bytes_data)

    def resetZoneAttributes(self):
        bytes_array = ESC + BackgroundColor.BLACK.value + ESC + UNMASKING + ESC + END_HIGHLIGHTING + DELIMETER
        self.__zone_attribute = ZoneAttributes()

        self.din.write(bytes_array)

    def maskingFullScreen(self):
        # TODO - TEST
        byte_array = ESC + b'\x23\x20\x58'

        self.din.write(byte_array)

    def unmaskingFullScreen(self):
        # TODO - TEST
        bytes_array = ESC + b'\x23\x20\x5f'

        self.din.write(bytes_array)

    def invertText(self):
        print("Not Implemented Yet")
        pass

    def invertBackground(self):
        print("Not Implemented Yet")
        pass 

    def newLine(self):
        self.layout.cariageReturn()
        self.layout.moveCursorDown()

        color = None
        highlight = None
        masking = None

        if self.__zone_attribute.background != BackgroundColor.BLACK:
            color = self.__zone_attribute.background

        if self.__zone_attribute.highlight:
            highlight = self.__zone_attribute.highlight

        if self.__zone_attribute.masking:
            masking = self.__zone_attribute.masking

        if color is not None or highlight is not None or masking is not None:
            self.setZoneAttributes(color=color, masking=masking, highlight=highlight)

    def print(self, text: str, text_align : TextAlign = TextAlign.LEFT, break_word: bool = False):
        # TODO - text alignment
        r, c = self.getCursorPosition()
        if c == -1:
            self.newLine()
            c = 1

        while len(text) > 0:
            if text[0] == '\n':
                self.newLine()
                c = 1
                text = text[1:]
                continue
            if text[0] == '\r':
                self.layout.cariageReturn()
                c = 1
                text = text[1:]
                continue
            if break_word is False:
                if text[0] != ' ':
                    word = text.split()[0]
                    if len(word) + c >= Layout.resolution[Mode.VIDEOTEX][1]:
                        self.newLine()
                        c = 1
                        if(len(word) >= Layout.resolution[Mode.VIDEOTEX][1]):
                            for j in range(Layout.resolution[Mode.VIDEOTEX][1] - 1):
                                self.din.write(
                                    alphanumerical.ascii_to_alphanumerical(text[j], vm=VisualizationModule.VGP5)
                                    )
                            text = text[Layout.resolution[Mode.VIDEOTEX][1]:]
                            continue
            elif break_word:
                if c >= Layout.resolution[Mode.VIDEOTEX][1] and text[0] != ' ' and text[1] != ' ' and text[1].isalnum():
                    self.din.write(
                        alphanumerical.ascii_to_alphanumerical('-', vm=VisualizationModule.VGP5)
                    )
                    c = 1
            
            self.din.write(
                        alphanumerical.ascii_to_alphanumerical(text[0], vm=VisualizationModule.VGP5)
                        )
            text = text[1:]
            
            c += 1
            if c > Layout.resolution[Mode.VIDEOTEX][1]:
                c = 1

    def Beep(self):
        self.din.write(self.BEL)
