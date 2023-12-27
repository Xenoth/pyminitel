import sys, time, math

from enum import Enum
from logging import *

import pyminitel.alphanumerical as alphanumerical
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.mode import Mode, RESOLUTION
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import Mode
from pyminitel.keyboard import *
from pyminitel.din import DIN

class MinitelException(Exception):
    # Raised on object's instanciation
    pass

class Minitel:

    __port = None
    __baudrate = None
    __din = None

    __manufacturer = None
    __model = None
    __fw_version = None

    __keyboard_extended = None
    __keyboard_c0 = None
    __keyboard_caps_enabled = None
    __pce_enabled = None
    __roll_mode_enabled = None
    __mode = None
    __vm = None

    # TODO - Warning on insersion or suppression when double sizes
    __text_attribute = None
    __zone_attribute = None

    __filter_bindings = {
        FilterKeyboardCode.Any_Keys: None,
        FilterKeyboardCode.Printable_Keys: None,
        FilterKeyboardCode.Other_Keys: None,
        FilterKeyboardCode.No_Keys : None,
    }
    __bindings = None

    class Baudrate(Enum):
        BAUDS_300 = 2
        BAUDS_1200 = 4
        BAUDS_4800 = 6

        def to_int(self):
            if self.name == 'BAUDS_300':
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

    ETEN = b'\x41'
    C0 = b'\x43'

    GET_KEYBOARD_STATUS = b'\x72'
    REP_KEYBOARD_STATUS = b'\x73'

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


    def __init__(self, port, baudrate = Baudrate.BAUDS_1200, mode: Mode = Mode.VIDEOTEX, safe_writing: bool = False):
        try:
            self.__din = DIN(port=port, baudrate=baudrate.to_int(), safe_writing=safe_writing)
        except Exception as e:
            log(ERROR, 'Unable to open Serial - ' + str(e))
            raise MinitelException
        
        self.__din.start()
        self.__din.setTimeout(.5)
        self.__port = port
        self.__baudrate = baudrate

        self.__text_attribute = TextAttributes()
        self.__zone_attribute = ZoneAttributes()

        self.__bindings = {}

        try:
            self.getMinitelInfo()
        except Exception as e:
            log(ERROR, 'Unable to retreive Minitel Info - ' + str(e))
            raise MinitelException

        if self.__manufacturer is None:
            log(ERROR, 'Unable to communicate with the minitel, bad baudrate or com port.')
            raise MinitelException

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

        self.getKeyboardMode()

        self.__din.setTimeout(None)
    
    def __del__(self):
        if self.__din:
            if not self.__din.stopped():
                self.__din.stop()
                self.__din.join()
        
            self.__din.close()

    def read(self, n: bytes) -> bytes:
        return self.__din.read(n)
    
    def send(self, data: bytes) -> None:
        try:
            self.__din.put(data)
        except Exception as e:
            log(ERROR, 'Got Exception while attempting to send message - ' + str(e))

    def switchReceiverTransmitter(self, receiver: Module, transmitter: Module, on: bool = True) -> dict:
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
        command += self.IO_CODES[receiver][self.IO.IN] + self.IO_CODES[transmitter][self.IO.OUT]

        self.send(command)
        answer = self.read(5)

        if answer[0:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[receiver][self.IO.IN]:
            log(ERROR, "Response from getModuleIOStatus's Request is invalid (got :" + str(answer.hex()) + ")")
            return None
        
        return {
            self.Module.SCREEN: int.from_bytes(answer[4:5]) & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: int.from_bytes(answer[4:5]) & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: int.from_bytes(answer[4:5]) & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: int.from_bytes(answer[4:5]) & self.CONNECTOR_STATUS_BITFIELD,
        }

    def blockModule(self, module: Module):
        res = self.switchReceiverTransmitter(module, module, False)
        if res is not None:
            return res[module] == 1
        return None

    def unblockModule(self, module: Module):
        res = self.switchReceiverTransmitter(module, module, True)
        if res is not None:
            return res[module] == 1
        return None

    def getModuleIOStatus(self, module: Module, io: IO) -> dict:
        # TODO - TEST
        command = self.PRO2 + self.TO + self.IO_CODES[module][io]

        self.send(command)
        answer = self.read(5)

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
        # TODO  - FINISH
        command = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module][self.IO.IN]

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

        self.send(command)

        answer = self.read(4)

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

        self.send(command)

        answer = self.read(2)

        if answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            log(ERROR, "Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")")
            return False
        
        return True

    def getMinitelInfo(self) -> tuple:
        command = self.PRO1 + self.ENQROM

        self.send(command)

        answer = self.read(5)
        
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
            elif self.__manufacturer == self.Manufacturer.TELIC_MATRA and (self.__fw_version == '2' or self.__fw_version == '3' or self.__fw_version == '4'):
                self.__vm = VisualizationModule.VGP2
            else:
                log(ERROR, 'Unknown Visualization Mode')
        else:
            self.__vm = VisualizationModule.VGP2
            log(Warning, 'Not handling models other than ' + self.Model.MINITEL_1B + ' , Default Visualization Mode set ' + self.__vm.name)

        return self.__vm
    
    def getModuleOperatingModeStatus(self) -> tuple:
        command = self.PRO1 + self.OPERATING_STATUS

        self.send(command)

        answer = self.read(4)
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

        self.send(command)

        answer = self.read(2)

        if  mode == Mode.MIXED and answer[0:2] != self.SEP + b'\x70' or mode == Mode.VIDEOTEX and answer[0:2] != self.SEP + b'\x71':
            log(ERROR, "Response from setVideoMode's Request is invalid (got :" + str(answer.hex()) + ")")
            return False

        self.__mode = mode
        return True

    def getCursorPosition(self) -> tuple:
        command = self.ESC + b'\x61'

        self.send(command)

        answer = self.read(3)

        if answer[0:1] != self.US:
            log(ERROR, "Response from getCursorPosition's Request is invalid (got :" + str(answer.hex()) + ")")
            return -1, -1

        mask = 63

        return int.from_bytes(answer[1:2]) & mask, int.from_bytes(answer[2:3]) & mask

    def showCursor(self):
        command = b'\x11'
        self.send(command)

    def hideCursor(self):
        command = b'\x14'
        self.send(command)

    def connectModem(self):
        # TODO - TEST
        command = self.PRO1 + b'\x68'

        self.send(command)

    def disconnectModem(self) -> bool:
        # TODO - TEST
        command = self.PRO1 + b'\x67'

        self.send(command)

    def setECP(self, enable: bool = False) -> bool:
        log(ERROR, "Not Implemented Yet")
        pass 

    def reverseModem(self) -> bool:
        log(ERROR, "Not Implemented Yet")
        pass 

    def setConnectorBaudrate(self, emission_baudrate = Baudrate.BAUDS_1200, reception_baudrate = Baudrate.BAUDS_1200) -> tuple:
        if emission_baudrate != reception_baudrate and self.__model == self.Model.MINITEL_1B:
            log(ERROR, "Emission and Reception Baudrate must be symetrical for Minitel 1B Models")
            return None, None
        
        prog_byte = 1 << 6
        prog_byte |= emission_baudrate.value << 3
        prog_byte |= reception_baudrate.value
        
        command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        self.send(command)

        time.sleep(1)

        old_baudrate = self.__baudrate
        self.__din.setBaudrate(emission_baudrate.to_int())

        manufacturer, model, version = None, None, None
        manufacturer, model, version = self.getMinitelInfo()

        if manufacturer is None:
            
            log(ERROR, "setConnectorBaudrate failed, Restoring initial baudrate...")

            self.__din.close()
            self.__din.setBaudrate(emission_baudrate.to_int())
            self.__din.open()

            prog_byte = 1 << 6
            prog_byte |= old_baudrate.value << 3
            prog_byte |= old_baudrate.value

            command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

            self.send(command)
            
            time.sleep(1)

            answer = self.read(4)

            if answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
                log(ERROR, "Response from setConnectorBaudrate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old baudrate...")
                return None, None

            return old_baudrate, old_baudrate
        
        self.send(command)

        answer = self.read(4)

        if answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
            log(ERROR, "Response from setConnectorBaudrate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old baudrate...")
            return None, None

        new_emission_speed = int.from_bytes(answer[3:4], 'little') & (7 << 3)
        new_emission_speed = new_emission_speed >> 3
        new_reception_speed = int.from_bytes(answer[3:4], 'little') & 7

        if new_reception_speed != reception_baudrate.value or new_emission_speed != emission_baudrate.value:
            log(WARNING, "Baudrates not updated, old config returned")

            return old_baudrate, old_baudrate

        return self.Baudrate(new_emission_speed), self.Baudrate(new_reception_speed)

    def getConnectorBaudrate(self) -> Baudrate:
        print("Not Implemented Yet")
        pass

    def setKeyboardMode(self, extended: bool = True, c0: bool = False) -> tuple:
        self.getKeyboardMode()
        if self.__keyboard_extended != extended:
            action = self.START
            if not extended: 
                action = self.STOP
            self.send(self.PRO3 + action + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] + self.ETEN)

            answer = self.read(5)

            if answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
                log(ERROR, "Response from setKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
                return None, None
            
            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self.__keyboard_extended = status & extended_bitfield
            self.__keyboard_c0 = status &  c0_bitfield
            
        if self.__keyboard_c0 != c0:
            action = self.START
            if not c0: 
                action = self.STOP
            self.send(self.PRO3 + action + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] + self.C0)

            answer = self.read(5)

            if answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
                log(ERROR, "Response from setKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
                return None, None 
            
            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self.__keyboard_extended = status & extended_bitfield
            self.__keyboard_c0 = status &  c0_bitfield

        return self.__keyboard_extended, self.__keyboard_c0

    def getKeyboardMode(self) -> tuple:
        self.send(self.PRO2 + self.GET_KEYBOARD_STATUS + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN])
        answer = self.read(5)
        if answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
            log(ERROR, "Response from getKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
            return None, None
        
        c0_bitfield = 1 << 2
        extended_bitfield = 1

        status = int.from_bytes(answer[4:5])
        self.__keyboard_extended = status & extended_bitfield
        self.__keyboard_c0 = status &  c0_bitfield

        return self.__keyboard_extended, self.__keyboard_c0

    def enableKeyboard(self) -> bool:
        return self.unblockModule(self.Module.KEYBOARD)

    def disableKeyboard(self) -> bool:
        return self.blockModule(self.Module.KEYBOARD)

    def enableEcho(self) -> bool:
        return self.unblockModule(self.Module.MODEM)

    def disableEcho(self) -> bool:
        return self.blockModule(self.Module.MODEM)

    def setKeyCapsLock(self, enable: bool) -> bool: 
        print("Not Implemented Yet")
        pass

    def setScreenPageMode(self) -> bool:
        if not self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already disabled.')

        command = self.PRO2 + self.STOP + self.ROULEAU

        self.send(command)
        answer = self.read(4)

        if answer[0:2] !=  self.PRO2:
            log(ERROR, 'setScreenPageMode might have failed, excepted x13x56 but got ' + answer.hex())

        self.__roll_mode_enabled = False

        # TODO - Handle answer properly ?
        print(str(answer[2:4]))

    def setScreenRollMode(self) -> bool:
        if self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already enabled.')
        
        command = self.PRO2 + self.START + self.ROULEAU

        self.send(command)
        answer = self.read(4)

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
    

    def setTextAttributes(self, color: CharacterColor = None, blinking: bool = None, inverted = None, double_height: bool = None, double_width: bool = None):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        if double_height:
            r, c = self.getCursorPosition()
            if r == 1:
                self.newLine()

        self.send(self.__text_attribute.setAttributes(color=color, blinking=blinking, inverted=inverted, double_height=double_height, double_width=double_width))

    def resetTextAttributes(self):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        self.setTextAttributes(color=CharacterColor.WHITE, blinking=False, inverted=False, double_height=False, double_width=False)

    def setZoneAttributes(self, color: BackgroundColor = None, masking: bool = None, highlight: bool = None):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        self.send(self.__zone_attribute.setAttributes(color=color, masking=masking, highlight=highlight))

    def resetZoneAttributes(self):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')

        self.setZoneAttributes(color=BackgroundColor.BLACK, masking=False, highlight=False)

    def maskingFullScreen(self):
        # TODO - TEST
        byte_array = ESC + b'\x23\x20\x58'

        self.send(byte_array)

    def unmaskingFullScreen(self):
        # TODO - TEST
        bytes_array = ESC + b'\x23\x20\x5f'

        self.send(bytes_array)

    def invertText(self):
        print("Not Implemented Yet")
        pass

    def invertBackground(self):
        print("Not Implemented Yet")
        pass 

    def clear(self):
        if self.__mode == Mode.VIDEOTEX:
            self.send(Layout.clear())
        else:
            self.send(Layout.setCursorPosition() + Layout.eraseInDisplay())

    def newLine(self):
        self.send(Layout.cariageReturn() + Layout.moveCursorDown())
    
    def print(self, text: str):
        data = b''
        for c in text:
            data += alphanumerical.ascii_to_alphanumerical(c=c, vm=self.__vm)
        
        self.send(data)
        
    def bind(self, key: KeyboardCode, callback):

        if isinstance(key, FilterKeyboardCode):
            self.__filter_bindings[key] = callback
            return

        self.__bindings[key] = callback

    def clearBindings(self):
        for filter in self.__filter_bindings:
            self.__filter_bindings[filter] = None
        
        self.__bindings = {} 

    def readKeyboard(self, timeout: int = None):
        old_timeout = self.__din.getTimeout()
        self.__din.setTimeout(timeout)

        data = self.read(1)
        if data[0:1] == b'\x19' or data[0:1] == b'\x13' or data[0:1] == b'\x1b':
            data += self.read(1)
            if data[1:2] == b'\x4b' or data[1:2] == b'\x5b':
                data += self.read(1)
                if data[2:3] == b'\x34' or data[2:3] == b'\x32':
                    data += self.read(1)

        self.__din.setTimeout(old_timeout)

        callback_called = False

        if len(data):
            print(data.hex())

        if len(data) == 0:
            if self.__filter_bindings[FilterKeyboardCode.No_Keys] is not None:
                self.__filter_bindings[FilterKeyboardCode.No_Keys]()
            return
        
        if self.__filter_bindings[FilterKeyboardCode.Any_Keys] is not None:
            self.__filter_bindings[FilterKeyboardCode.Any_Keys]()
            callback_called = True

        try:
            char = VideotexKeyboardCode(data).char()
            if str.isprintable(char):
                if self.__filter_bindings[FilterKeyboardCode.Printable_Keys]:
                    self.__filter_bindings[FilterKeyboardCode.Printable_Keys](char)
                    callback_called = True
        except Exception as e:
            log(ERROR, e)
            pass


        if data in self.__bindings:
            callback = self.__bindings[data]
            callback()
            callback_called = True

        if not callback_called:
            if self.__filter_bindings[FilterKeyboardCode.Other_Keys]:
                self.__filter_bindings[FilterKeyboardCode.Other_Keys]()

    def beep(self):
        self.send(self.BEL)
