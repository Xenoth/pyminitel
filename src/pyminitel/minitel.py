import sys, time

from enum import Enum
from serial import Serial, SerialException
from logging import *

import pyminitel.alphanumerical as alphanumerical
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.mode import Mode
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import Mode

class Minitel:

    din = None

    layout = None

    __manufacturer = None
    __model = None
    __fw_version = None

    __keyboard_caps_enabled = None
    __pce_enabled = None
    __roll_mode_enabled = None
    __mode = None
    __vm = None

    __text_attribute = None
    __zone_attribute = None

    class Bauderate(Enum):
        BAUDS_75 = 1
        BAUDS_300 = 2
        BAUDS_1200 = 4
        BAUDS_4800 = 6

        def to_int(self):
            if self.name == 'BAUDS_75':
                return 75
            elif self.name == 'BAUDS_300':
                return 300
            elif self.name == 'BAUDS_1200':
                return 1200
            elif self.name == 'BAUDS_4800':
                return 4800
            
            return 0

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
    PROG = b'\x6b'

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
    
    SOH = b'\x01'
    EOT = b'\x04'
    ENQROM = b'\x7b'

    MIXTE1 = b'\x32\x7d'
    MIXTE2 = b'\x32\x7e'

    OPERATING_STATUS = b'\x72'
    OPERATING_STATUS_RES = b'\x73'

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

    class Manufacturer(Enum):
        TELIC_MATRA = 'C'
        TRT_PHILIPS = 'B'

    class Model(Enum):
        MINITEL_1_b = 'b'
        MINITEL_1_c = 'c'
        MINITEL_1_r = 'r'

        MINITEL_1_COLOR = 's'

        MINITEL_1_D = 'r'
        
        MINITEL_10_d = 'd'
        MINITEL_10_f = 'f'

        MINITEL_1B = 'u'

        MINITEL_10B = 'w'

        MINITEL_2 = 'v'

        MINITEL_12 = 'z'

        MINITEL_5 = 'y'


    def __init__(self, port, bauderate = Bauderate.BAUDS_1200, mode: Mode = Mode.VIDEOTEX):
        try:
            self.din = Serial(port=port, baudrate=bauderate.to_int(), bytesize=7, parity='E', stopbits=1)
        except SerialException:
            log(ERROR, 'Unable to open Serial.')
            exit()

        self.din.flush()

        self.din.timeout = 5

        self.layout = Layout(self.din)
        self.__text_attribute = TextAttributes()
        self.__zone_attribute = ZoneAttributes()

        self.getMinitelInfo()

        if self.__manufacturer is None:
            log(ERROR, 'Unable to communicate with the minitel, bad bauderate or com port.')
            exit()

        self.getVisualizationModule()

        print('[Minitel Info]')
        print('- ROM ID: "' + self.__manufacturer.value + self.__model.value + self.__fw_version + '"')
        print('* Manufacturer: ' + self.__manufacturer.name)
        print('* Model: ' + self.__model.name)
        print('* Firmware Version: ' + self.__fw_version)
        print('* Visualization Module: ' + self.__vm.name)

        if self.__model != self.Model.MINITEL_1B:
            log(WARNING, 'pyMinitel is supporting MINITEL 1B for now, try at your own risk.')

        self.getModuleOperatingModeStatus()

        print('[Modules Operating Mode Status]')
        print('* isKeyboadCapsLocked: ' + str(self.__keyboard_caps_enabled))
        print('* PCE: ' + str(self.__pce_enabled))
        print('* Roll Mode: ' + str(self.__roll_mode_enabled))
        print('* Screen Mode: ' + str(self.__mode.name))

        self.setVideoMode(mode)
        print('* New Video Mode:' + str(self.__mode.name))

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
            log(ERROR, 'Switching ' + transmitter.name + ' -> ' + receiver.name + 'is not possible')
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
            log(ERROR, "Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")")
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
            log(ERROR, "Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")")
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

        self.din.write(command)

        answer = self.din.read(4)

        if answer[0:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
            log(ERROR, "Response from getStatusProtocol's Request is invalid (got :" + str(answer.hex()) + ")")
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
            log(ERROR, "Invalid Argument, n should be between 1-127, got " + n + "")
            return False

        bit_n = n.to_bytes(1, 'little')
        bit_n |= (1<<7)

        command = self.PRO2 + b'\x66' + bit_n

        self.din.write(command)

        answer = self.din.read(2)

        if answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            log(ERROR, "Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")")
            return False
        
        return True

    def getMinitelInfo(self) -> tuple:
        command = self.PRO1 + self.ENQROM

        self.din.write(command)

        answer = self.din.read(5)
        
        if answer[0:1] != self.SOH or answer[4:5] != self.EOT:
            log(ERROR, "Response from getMinitelInfo's Request is invalid (got :" + str(answer.hex()) + ")")
            return None, None, None
        
        self.__manufacturer = self.Manufacturer(answer[1:2].decode())
        self.__model = self.Model(answer[2:3].decode())
        self.__fw_version = answer[3:4].decode()

        return self.__manufacturer, self.__model, self.__fw_version
    
    def getVisualizationModule(self):
        if self.__model == self.Model.MINITEL_1B:
            if self.__manufacturer == self.Manufacturer.TRT_PHILIPS or self.__fw_version == '5' or self.__fw_version == ';' or self.__fw_version == '<':
                self.__vm = VisualizationModule.VGP5
            if self.__manufacturer == self.Manufacturer.TELIC_MATRA and (self.__fw_version == '2' or self.__fw_version == '3' or self.__fw_version == '4'):
                self.__vm = VisualizationModule.VGP2
            else:
                log(ERROR, 'Unknown Visualization Mode')
        else:
            self.__vm = VisualizationModule.VGP2
            log(Warning, 'Not handling models other than ' + self.Model.MINITEL_1B + ' , Default Visualization Mode set ' + self.__vm.name)

        return self.__vm
    

    
    def getModuleOperatingModeStatus(self) -> tuple:
        command = self.PRO1 + self.OPERATING_STATUS

        self.din.write(command)

        answer = self.din.read(4)
        if answer[0:2] != self.PRO2 or answer[2:3] != self.OPERATING_STATUS_RES:
            log(ERROR, "Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")")
            return None, None, None, None

        status = int.from_bytes(answer[3:4])

        keyboard_caps_lock_bit = 1 << 3
        pce_bitfield_bit = 1 << 2
        roll_mode_bit = 1 << 1
        screen_format_bit = 1

        self.__keyboard_caps_enabled = status & keyboard_caps_lock_bit == 0
        self.__pce_enabled = status & pce_bitfield_bit == 1
        self.__roll_mode_enabled = status & roll_mode_bit == 1
        if status & screen_format_bit == 0:
            self.__mode = Mode.VIDEOTEX
        else:
            self.__mode = Mode.MIXED

        return self.__keyboard_caps_enabled, self.__pce_enabled, self.__roll_mode_enabled, self.__mode
    
    def setVideoMode(self, mode: Mode = Mode.VIDEOTEX) -> bool:
        if mode is None:
            log(ERROR, 'Invalid None Argument')
            return False
        if self.__mode == mode:
            log(INFO, 'Video Mode already set in ' + mode.name + ' mode')
            return False

        command = self.PRO2

        if mode == Mode.MIXED:
            command += self.MIXTE1
        else:
            command += self.MIXTE2

        self.din.write(command)

        answer = self.din.read(2)

        if  mode == Mode.MIXED and answer[0:2] != self.SEP + b'\x70' or mode == Mode.VIDEOTEX and answer[0:2] != self.SEP + b'\x71':
            log(ERROR, "Response from setVideoMode's Request is invalid (got :" + str(answer.hex()) + ")")
            return False

        self.__mode = mode
        return True

    def getCursorPosition(self) -> tuple:
        command = self.ESC + b'\x61'

        self.din.write(command)

        answer = self.din.read(3)

        if answer[0:1] != self.US:
            log(ERROR, "Response from getCursorPosition's Request is invalid (got :" + str(answer.hex()) + ")")
            return -1, -1

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
        log(ERROR, "Not Implemented Yet")
        pass 

    def reverseModem(self) -> bool:
        log(ERROR, "Not Implemented Yet")
        pass 

    def setConnectorBauderate(self, emission_bauderate = Bauderate.BAUDS_1200, reception_bauderate = Bauderate.BAUDS_1200) -> tuple:
        if emission_bauderate != reception_bauderate and self.__model == self.Model.MINITEL_1B:
            log(ERROR, "Emission and Reception Bauderate must be symetrical for Minitel 1B Models")
            return None, None
        
        prog_byte = 1 << 6
        prog_byte |= emission_bauderate.value << 3
        prog_byte |= reception_bauderate.value
        
        command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        self.din.write(command)

        time.sleep(1)
        
        self.din.close()

        old_bauderate = self.din.baudrate

        old_bauderate_enum = None
        if old_bauderate == 75:
            old_bauderate_enum = self.Bauderate.BAUDS_75
        elif old_bauderate == 300:
            old_bauderate_enum = self.Bauderate.BAUDS_300
        elif old_bauderate == 1200:
            old_bauderate_enum = self.Bauderate.BAUDS_1200
        elif old_bauderate == 4800:
            old_bauderate_enum = self.Bauderate.BAUDS_4800
        
        self.din.baudrate = emission_bauderate.to_int()

        manufacturer, model, version = None, None, None

        self.din.open()

        manufacturer, model, version = self.getMinitelInfo()


        if manufacturer is None:
            
            log(ERROR, "setConnectorBauderate failed, Restoring initial baudrate...")

            self.din.close()

            self.din.baudrate = old_bauderate

            self.din.open()

            prog_byte = 1 << 6
            prog_byte |= old_bauderate_enum.value << 3
            prog_byte |= old_bauderate_enum.value

            command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

            self.din.write(command)
            
            time.sleep(1)

            answer = self.din.read(4)

            if answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
                log(ERROR, "Response from setConnectorBauderate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old bauderate...")
                return None, None

            return old_bauderate_enum, old_bauderate_enum
        
        self.din.write(command)

        answer = self.din.read(4)

        if answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
            log(ERROR, "Response from setConnectorBauderate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old bauderate...")
            return None, None

        new_emission_speed = int.from_bytes(answer[3:4], 'little') & (7 << 3)
        new_emission_speed = new_emission_speed >> 3
        new_reception_speed = int.from_bytes(answer[3:4], 'little') & 7

        if new_reception_speed != reception_bauderate.value or new_emission_speed != emission_bauderate.value:
            log(WARNING, "Bauderates not updated, old config returned")

            return old_bauderate_enum, old_bauderate_enum

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
        if not self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already disabled.')

        command = self.PRO2 + self.STOP + self.ROULEAU

        self.din.write(command)
        answer = self.din.read(4)

        if answer[0:2] !=  self.PRO2:
            log(ERROR, 'setScreenPageMode might have failed, excepted x13x56 but got ' + answer.hex())

        self.__roll_mode_enabled = False

        # TODO - Handle answer properly ?
        print(str(answer[2:4]))

    def setScreenRollMode(self) -> bool:
        if self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already enabled.')
        
        command = self.PRO2 + self.START + self.ROULEAU

        self.din.write(command)
        answer = self.din.read(4)

        if answer[0:2] !=  self.PRO2:
            log(WARNING, 'setScreenRollMode might have failed, excepted x13x56 but got ' + answer.hex())

        self.__roll_mode_enabled = True

        # TODO - Handle answer properly ?
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
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        bytes_data = b''
        
        if color is not None:
            bytes_data += ESC + color.value
            self.__text_attribute.color = color

        if blinking is not None:
            if blinking:
                bytes_data += ESC + BLINKING
                self.__text_attribute.blinking = True
            else:
                bytes_data += ESC + FIXED
                self.__text_attribute.blinking = False

        if double_height is not None or double_width is not None:
            if double_width == double_height:
                if double_height:
                    bytes_data += ESC + DOUBLE_SIZE
                    self.__text_attribute.double_height = True
                    self.__text_attribute.double_width = True
                else:
                    bytes_data += ESC + NORMAL_SIZE
                    self.__text_attribute.double_height = False
                    self.__text_attribute.double_width = False
            else:
                if double_height:
                    bytes_data += ESC + DOUBLE_HEIGHT
                    self.__text_attribute.double_height = True
                elif double_width:
                    bytes_data += ESC + DOUBLE_WIDTH
                    self.__text_attribute.double_width = True

        self.din.write(bytes_data)

    def resetTextAttributes(self):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        bytes_data = ESC + CharacterColor.WHITE.value + ESC + FIXED + ESC + NORMAL_SIZE

        self.din.write(bytes_data)

    def setZoneAttributes(self, color: BackgroundColor = None, masking: bool = None, highlight: bool = None):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')
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
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')
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

    def clear(self):
        if self.__mode == Mode.VIDEOTEX:
            self.layout.clear()
        else:
            self.layout.setCursorPosition()
            self.layout.eraseInDisplay()

    def newLine(self):
        self.layout.cariageReturn()
        self.layout.moveCursorDown()

        if self.__mode == Mode.VIDEOTEX:
            if self.__text_attribute.double_height:
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

        if r == 1 and self.__mode == Mode.VIDEOTEX and self.__text_attribute.double_height:
            self.layout.moveCursorDown()
            r += 1

        factor = 1
        if self.__text_attribute.double_width and self.__mode == Mode.VIDEOTEX:
            factor = 2

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
                    if (len(word) * factor) + c >= Layout.resolution[self.__mode][1]:
                        self.newLine()
                        c = 1
                    while((len(word) * factor) >= Layout.resolution[self.__mode][1]):
                            for j in range(int(Layout.resolution[self.__mode][1] / factor) - 1):
                                self.din.write(
                                    alphanumerical.ascii_to_alphanumerical(text[j], vm=self.__vm)
                                    )
                            text = text[int(Layout.resolution[self.__mode][1] / factor):]
                            word = text.split()[0]
                            c = 1
                            if self.__mode == Mode.MIXED:
                                self.layout.cariageReturn()
                                self.layout.moveCursorDown()
                            continue
            elif break_word:
                offset = 0
                if factor == 2:
                    offset = 2
                if c >= Layout.resolution[self.__mode][1] - offset and text[0] != ' ' and text[1] != ' ' and text[0].isalnum():
                    self.din.write(
                        alphanumerical.ascii_to_alphanumerical('-', vm=self.__vm)
                    )
                    c = 1
                    if self.__mode == Mode.MIXED:
                        self.layout.cariageReturn()
                        self.layout.moveCursorDown()
            
            self.din.write(
                        alphanumerical.ascii_to_alphanumerical(text[0], vm=self.__vm)
                        )
            text = text[1:]
            
            c += 1 * factor
            if c > Layout.resolution[self.__mode][1]:
                c = 1
                if self.__mode == Mode.MIXED:
                        self.layout.cariageReturn()
                        self.layout.moveCursorDown() 

    def Beep(self):
        self.din.write(self.BEL)
