from serial import Serial
from mode import Mode
from attributs import Attributs
from enum import Enum
import sys

class Minitel:

    __serial = None

    __mode = Mode.VIDEOTEX

    def __init__(self, port, bauderate = 1200):
        # self.__serial = Serial(port=port, bauderate=bauderate)
        pass

    def set_mode(self, mode):
        self.__mode = mode

    class Bauderate(Enum):
        LOW = 2      # 300 Bauds
        MEDIUM = 4   # 1200 Bauds
        HIGH = 6     # 4800 Bauds


    ESC = b'\x1a'
    US = b'\x1e'

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
        Module.SCREEN: { IO.OUT: b'\x51', IO.IN: b'\x59' },
        Module.SCREEN: { IO.OUT: b'\x52', IO.IN: b'\x5a' },
        Module.SCREEN: { IO.OUT: b'\x53', IO.IN: b'\x5b' },
    }

    def switchReceiverTransmitter(self, receiver: Module, transmitter: Module, on: bool = True) -> dict:
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

        command = self.ESC + self.PRO3
        command += ON if on else OFF
        command += self.IO_CODES[receiver.value][self.IO.IN] + self.IO_CODES[transmitter.value][self.IO.OUT]


        # TODO - MOCKED
        status = b'\x48'
        answer = self.ESC + self.PRO2 + self.FROM + self.IO_CODES[receiver.value][self.IO.OUT] + status

        if answer[0:1] != self.ESC or answer[1:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[receiver.value][self.IO.OUT]:
            print("Error - Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None
        
        return {
            self.Module.SCREEN: answer[4:5] & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: answer[4:5] & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: answer[4:5] & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: answer[4:5] & self.CONNECTOR_STATUS_BITFIELD,
        }

    def blockModule(self, module: Module):
        self.switchReceiverTransmitter(module, module, False)

    def unblockModule(self, module: Module):
        self.switchReceiverTransmitter(module, module, True)

    def getModuleIOStatus(self, module: Module, io: IO) -> dict:
        command += self.ESC + self.PRO2 + self.TO + self.IO_CODES[module.value][io.value]

        print(command.hex())

        # TODO - MOCKED
        status = b'\x48'
        answer = self.ESC + self.PRO2 + self.FROM + self.IO_CODES[module.value][io.value] + status

        if answer[0:1] != self.ESC or answer[1:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[module.value][io.value]:
            print("Error - Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return None

        return {
            self.Module.SCREEN: answer[4:5] & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: answer[4:5] & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: answer[4:5] & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: answer[4:5] & self.CONNECTOR_STATUS_BITFIELD,
        }
    
    def setModuleDiffusion(self, module: Module, activate: bool = True):
        command = b'' + self.ESC + self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module.value][self.IO.IN]

        print(command.hex())

    def setModuleACK(self, module: Module, activate: bool = True):
        command = b'' + self.ESC + self.PRO2
        command += self.COMMAND_CODE_ENABLE_ if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module.value][self.IO.OUT]

        print(command.hex())

    def getProtocolStatus(self) -> dict:
        command = b'' + self.ESC + self.PRO1 + self.STATUS_PROTOCOL_REQUEST

        print(command.hex())

        # TODO - MOCKED
        status = b'\x4f'
        answer = self.ESC + self.PRO2 + self.STATUS_PROTOCOL_ANSWER + status

        if answer[0:1] != self.ESC or answer[1:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
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
        if n < 1 or n > 127:
            print("Error - Invalid Argument, n should be between 1-127, got " + n + "", file=sys.stderr)
            return False

        bit_n = n.to_bytes(1, 'little')
        bit_n |= (1<<7)

        # TODO - MOCKED
        answer = self.SEP + b'\x57'

        if answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            print("Error - Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return False
        
        return True

    def getMinitelInfo(self) -> tuple:
        pass

    def getCursorPosition(self) -> tuple:
        command = b'' + self.ESC + b'\x61'

        print(command.hex())

        #TODO - MOCKED 
        answer = self.US + b'\x05\x12'

        if answer[0:1] != self.US:
            print("Error - Response from getCursorPosition's Request is invalid (got :" + str(answer.hex()) + ")", file=sys.stderr)
            return -1, -1
        
        return int.from_bytes(answer[0:1]), int.from_bytes(answer[1:2])

    def connectModem(self) -> bool:
        pass

    def disconnectModem(self) -> bool:
        pass

    def setECP(self, enable: bool = False) -> bool:
        pass 

    def reverseModem(self) -> bool:
        pass


    def setConnectorBauderate(self, mode: Bauderate = Bauderate.MEDIUM) -> Bauderate:
        pass

    def getConnectorBauderate(self) -> Bauderate:
        pass

    class KeyboardMode(Enum):
        ETENDU = b'\x41'
        C0 = b'\x43'

    def setKeyboardMode(self, mode: KeyboardMode) -> KeyboardMode:
        pass

    def enableKeyboard(self) -> bool:
        pass

    def disableKeyboard(self) -> bool:
        pass

    def getKeyboardMode(self) -> KeyboardMode:
        pass

    def setKeyCapsLock(self, enable: bool) -> bool: 
        pass

    def setScreenPageMode(self) -> bool:
        pass

    def setScreenRollMode(self) -> bool:
        pass

    class CopyMode(Enum):
        FR = b'\x6a'
        USA = b'\x6b'

    def copyScreenToConnector(self, mode: CopyMode = CopyMode.FR) -> bool:
        pass

    def getModulesFunctionalStates(self) -> dict:
        pass
    

    def setTextAttributes(color : Attributs.CharacterColor, blinking: bool, double_height: bool, double_width: bool):
        
        bytes_data = b''
        
        if color is not None:
            bytes_data += Attributs.ESC + color.value

        if blinking is not None:
            if blinking:
                bytes_data += Attributs.ESC + Attributs.BLINKING
            else:
                bytes_data += Attributs.ESC + Attributs.FIXED

        if double_height is not None and double_width is not None:
            if double_width == double_height:
                if double_height:
                    bytes_data += Attributs.ESC + Attributs.DOUBLE_SIZE
                else:
                    bytes_data += Attributs.ESC + Attributs.DOUBLE_SIZE
            else:
                bytes_data += Attributs.ESC + Attributs.NORMAL_SIZE
                if double_height:
                    bytes_data += Attributs.ESC + Attributs.DOUBLE_HEIGHT
                elif double_width:
                    bytes_data += Attributs.ESC + Attributs.DOUBLE_WIDTH

        print(bytes_data)

    setTextAttributes(Attributs.CharacterColor.BLUE, True, True, False)

    def resetTextAttributes():
        
        bytes_data = Attributs.ESC + Attributs.CharacterColor.WHITE + Attributs.ESC + Attributs.FIXED + Attributs.ESC + Attributs.NORMAL_SIZE

        print(bytes_data)

    def setZoneAttributes(color: Attributs.BackgroundColor, masking: bool, highlight: bool):
        
        bytes_data = b''

        if color is not None:
            bytes_data += Attributs.ESC + color.value 

        if masking is not None:
            if masking:
                bytes_data += Attributs.MASKING
            else:
                bytes_data += Attributs.UNMASKING
        
        if highlight is not None:
            if highlight:
                bytes_data += Attributs.START_HIGHLIGHTING
            else:
                bytes_data+= Attributs.END_HIGHLIGHTING
    
        bytes_data += Attributs.DELIMETER

        print(bytes_data)

    setZoneAttributes(Attributs.BackgroundColor.RED, False, True)

    def resetZoneAttributes():
        
        bytes_array = Attributs.ESC + Attributs.BackgroundColor.BLACK + Attributs.UNMASKING + Attributs.END_HIGHLIGHTING + Attributs.DELIMETER

        print(bytes_array)

    def maskingFullScreen():
        
        byte_array = Attributs.ESC + b'\x23\x20\x58'

        print(byte_array)

    def unmaskingFullScreen():

        bytes_array = Attributs.ESC + b'\x23\x20\x5f'

        print(bytes_array)

    def invertText():
        pass

    def invertBackground():
        pass 

    

minitel = Minitel(port='c')
r, c = minitel.getCursorPosition()

print("r=" + str(r) + ", c=" + str(c) )