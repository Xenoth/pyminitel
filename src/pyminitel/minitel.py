import time, socket

from enum import Enum
from logging import log, ERROR, WARNING, INFO

import pyminitel.alphanumerical as alphanumerical
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.mode import Mode, RESOLUTION
from pyminitel.visualization_module import VisualizationModule
from pyminitel.mode import Mode
from pyminitel.keyboard import *
from pyminitel.comm import CommSerial, CommSocket, CommException

class MinitelException(Exception):
    # Raised on object's instanciation
    pass

class Minitel:
    '''
    Pyminitel Minitel class
    '''

    __port = None
    __baudrate = None
    __comm = None

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

    class ConnectorBaudrate(Enum):
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


    def __init__(self, port: str, baudrate = ConnectorBaudrate.BAUDS_1200, ip: str = None, mode: Mode = Mode.VIDEOTEX, timeout: float = None, tcp: socket = None):
        '''
        Minitel's constructor - This function is raising MinitelException if unable to retreive basic minitel's information.
        This object will instantiate a serial communication or a TCP socket (as server) depending if "ip" argument given is None or not.
        TCP Socket communication will block until client has been found.

            Parameters:
                port (str): Either Serial's port or IP's port (ex: '/dev/ttyUSB0' or '8080') - The value has no effect on deciding the type of communication
                bauderate (Minitel.ConnectorBaudrate): The bauderate of DIN's connector - Default 1200
                ip (str): IP for TCP Socket server - When not None the constructor will attempt to use Socket - Default None
                mode (Mode): Minitel's Mode - Default is Videotex (standard mode)
                timeout (float): Set the comm timeout (default None)

            Returns:
                Minitel instantiated object if basics minitel info retreived else raises MinitelException

        '''
        if not ip and not tcp:
            try:
                self.__comm = CommSerial(port=port, baudrate=baudrate.to_int(), timeout=timeout)
            except CommException as e:
                log(ERROR, 'Unable to open Serial - ' + str(e))
                raise MinitelException
        else:
            try:
                int_port = None
                if port:
                    int_port = int(port)
                self.__comm = CommSocket(port=int_port, host=ip, timeout=timeout, tcp=tcp)
            except CommException as e:
                log(ERROR, 'Unable to create socket - ' + str(e))
                raise MinitelException
        
        log(level=DEBUG, msg='New Comm: id ' + str(id(self.__comm)))

        try:
            self.__comm.start()
        except RuntimeError:
            log(ERROR, 'Thread of Comm already started')
        
        if timeout is None:
            self.__comm.setTimeout(10)

        self.__port = port
        self.__baudrate = baudrate

        self.__text_attribute = TextAttributes()
        self.__zone_attribute = ZoneAttributes()

        self.__bindings = {}

        res = self.getMinitelInfo()
        if res is None:
            log(ERROR, 'Unable to communicate with the minitel, bad baudrate or com port.')
            raise MinitelException

        
        print('[Minitel Info]')
        print('- ROM ID: "' + self.__manufacturer.value + self.__model.value + self.__fw_version + '"')
        print('* Manufacturer: ' + self.__manufacturer.name)
        print('* Model: ' + self.__model.name)
        print('* Firmware Version: ' + self.__fw_version)

        if self.getVisualizationModule() is None:
            log(ERROR, 'Unable to retrive with the minitel visualization module')
        else:
            print('* Visualization Module: ' + self.__vm.name)

        if self.__model != self.Model.MINITEL_1B:
            log(WARNING, 'pyMinitel is supporting MINITEL 1B for now, try at your own risk.')
        
        if self.getModuleOperatingModeStatus() is None:
            log(ERROR, 'Unable to retrive with the minitel module operating mode status')
        else:
            print('[Modules Operating Mode Status]')
            print('* isKeyboadCapsLocked: ' + str(self.__keyboard_caps_enabled))
            print('* PCE: ' + str(self.__pce_enabled))
            print('* Roll Mode: ' + str(self.__roll_mode_enabled))
            print('* Screen Mode: ' + str(self.__mode.name))

        if self.setVideoMode(mode):
            log(ERROR, 'Unable to set video mode')
        else:
            print('* New Video Mode:' + str(self.__mode.name))

        if self.getKeyboardMode() is None:
            log(ERROR, 'Unable to retreive keyboard mode')
        else:
            print('* Keyboard Extended: ' + str(self.__keyboard_extended))
            print('* Keyboard C0: ' + str(self.__keyboard_c0))

        if timeout is None:
            self.__comm.setTimeout(None)
    
    def __del__(self):
        if self.__comm:
            if not self.__comm.stopped():
                self.__comm.stop()
                self.__comm.join()
        
            self.__comm.close()

    def read(self, n: bytes) -> bytes:
        try:
            return self.__comm.read(n)
        except CommException as e:
            log(ERROR, 'Got Exception while attempting to send message - ' + str(e))
            return None

    
    def send(self, data: bytes) -> int:
        try:
            self.__comm.put(data)
        except CommException as e:
            log(ERROR, 'Got Exception while attempting to send message - ' + str(e))
            return -1
        
        return 0

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
            return None
        
        OFF = b'\x60'
        ON = b'\x61'

        command = self.PRO3
        command += ON if on else OFF
        command += self.IO_CODES[receiver][self.IO.IN] + self.IO_CODES[transmitter][self.IO.OUT]

        if self.send(command):
            log(ERROR, "Error while attempting to send switchReceiverTransmitter request")
            return None
        answer = self.read(5)
        if answer is None or answer[0:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[receiver][self.IO.IN]:
            log(ERROR, "Response from switchReceiverTransmitter's Request is invalid (got :" + str(answer.hex()) + ")")
            return None
        
        return {
            self.Module.SCREEN: int.from_bytes(answer[4:5]) & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: int.from_bytes(answer[4:5]) & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: int.from_bytes(answer[4:5]) & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: int.from_bytes(answer[4:5]) & self.CONNECTOR_STATUS_BITFIELD,
        }

    def blockModule(self, module: Module) -> bool:
        '''
        Block the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to block
            Returns: 
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''
        res = self.switchReceiverTransmitter(module, module, False)
        return res[module] == 1 if res is not None else None

    def unblockModule(self, module: Module) -> bool:
        '''
        Unblock the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to unblock
            Returns: 
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''
        res = self.switchReceiverTransmitter(module, module, True)
        return res[module] == 1 if res is not None else None

    def getModuleIOStatus(self, module: Module, io: IO) -> dict:
        # TODO - TEST
        command = self.PRO2 + self.TO + self.IO_CODES[module][io]

        if self.send(command):
            log(ERROR, "Error while attempting to send getModuleIOStatus request")
            return None
        answer = self.read(5)
        if answer is None or answer[0:2] != self.PRO3 or answer[2:3] != self.FROM or answer[3:4] != self.IO_CODES[module.value][io.value]:
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

        self.send(command)

    def getProtocolStatus(self) -> dict:
        # TODO - TEST
        command = self.PRO1 + self.STATUS_PROTOCOL_REQUEST

        if self.send(command):
            log(ERROR, "Error while attempting to send getProtocolStatus request")
            return None

        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
            log(ERROR, "Response from getStatusProtocol's Request is invalid (got :" + str(answer.hex()) + ")")
            return None
        
        return {
            'D1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D1,
            'D2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D2,
            'A1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A1,
            'A2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A2,
            'PAD_X3_COMPATIBLE': answer[4] & self.BITFIELD_STATUS_PROTOCOL_PAD,
        } 

    def setProtocolTransparency(self, n: int) -> int:
        # TODO - TEST
        if n < 1 or n > 127:
            log(ERROR, "Invalid Argument, n should be between 1-127, got " + n + "")
            return -1

        bit_n = n.to_bytes(1, 'little')
        bit_n |= (1<<7)

        command = self.PRO2 + b'\x66' + bit_n

        if self.send(command):
            log(ERROR, "Error while attempting to send setProtocolTransparency request")
            return -1

        answer = self.read(2)
        if answer is None or answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            log(ERROR, "Response from setProtocolTransparency's Request is invalid (got :" + str(answer.hex()) + ")")
            return -1
        
        return 0

    def getMinitelInfo(self) -> tuple:
        command = self.PRO1 + self.ENQROM

        if self.send(command):
            log(ERROR, "Error while attempting to send getMinitelInfo request")
            return None

        answer = self.read(5)
        if answer is None or answer[0:1] != self.SOH or answer[4:5] != self.EOT:
            log(ERROR, "Response from getMinitelInfo's Request is invalid (got :" + str(answer.hex()) + ")")
            return None
        
        self.__manufacturer = self.Manufacturer(answer[1:2].decode())
        self.__model = self.Model(answer[2:3].decode())
        self.__fw_version = answer[3:4].decode()

        return self.__manufacturer, self.__model, self.__fw_version
    
    def getVisualizationModule(self) -> VisualizationModule:
        if self.__model == self.Model.MINITEL_1B:
            if self.__manufacturer == self.Manufacturer.TRT_PHILIPS or self.__fw_version == '5' or self.__fw_version == ';' or self.__fw_version == '<':
                self.__vm = VisualizationModule.VGP5
            elif self.__manufacturer == self.Manufacturer.TELIC_MATRA and (self.__fw_version == '2' or self.__fw_version == '3' or self.__fw_version == '4'):
                self.__vm = VisualizationModule.VGP2
            else:
                log(ERROR, 'Unknown Visualization Module - Default is ' + self.__vm.name)
        else:
            self.__vm = VisualizationModule.VGP2
            log(Warning, 'Not handling models other than ' + str(self.Model.MINITEL_1B) + ' (got model: ' + str(self.__model) +'), Default is ' + self.__vm.name)

        return self.__vm
    
    def getModuleOperatingModeStatus(self) -> tuple:
        command = self.PRO1 + self.OPERATING_STATUS

        if self.send(command):
            log(ERROR, "Error while attempting to send getModuleOperatingModeStatus request")
            return None

        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != self.OPERATING_STATUS_RES:
            log(ERROR, "Response from getModuleOperatingModeStatus's Request is invalid (got :" + str(answer.hex()) + ")")
            return None

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
    
    def setVideoMode(self, mode: Mode = Mode.VIDEOTEX) -> int:
        if mode is None:
            log(ERROR, 'Invalid None Argument')
            return -1
        if self.__mode == mode:
            log(INFO, 'Video Mode already set in ' + mode.name + ' mode')
            return 0

        command = self.PRO2

        if mode == Mode.MIXED:
            command += self.MIXTE1
        else:
            command += self.MIXTE2

        if self.send(command):
            log(ERROR, "Error while attempting to send setVideoMode request")
            return -1

        answer = self.read(2)
        if  answer is None or mode == Mode.MIXED and answer[0:2] != self.SEP + b'\x70' or mode == Mode.VIDEOTEX and answer[0:2] != self.SEP + b'\x71':
            log(ERROR, "Response from setVideoMode's Request is invalid (got :" + str(answer.hex()) + ")")
            return -1

        self.__mode = mode
        return 0

    def getCursorPosition(self) -> tuple:
        command = self.ESC + b'\x61'

        if self.send(command):
            log(ERROR, "Error while attempting to send getCursorPosition request")
            return None

        answer = self.read(3)
        if answer is None or answer[0:1] != self.US:
            log(ERROR, "Response from getCursorPosition's Request is invalid (got :" + str(answer.hex()) + ")")
            return None

        mask = 63
        return int.from_bytes(answer[1:2]) & mask, int.from_bytes(answer[2:3]) & mask

    def showCursor(self) -> int:
        if self.send(b'\x11'):
            log(ERROR, "Error while attempting to send showCursor request")
            return -1
        return 0

    def hideCursor(self) -> int:
        if self.send(b'\x14'):
            log(ERROR, "Error while attempting to send hideCursor request")
            return -1
        return 0

    def connectModem(self) -> int:
        # TODO - TEST
        if self.send(self.PRO1 + b'\x68'):
            log(ERROR, "Error while attempting to send connectModem request")
            return -1
        return 0

    def disconnectModem(self) -> int:
        # TODO - TEST
        if self.send(self.PRO1 + b'\x67'):
            log(ERROR, "Error while attempting to send disconnectModem request")
            return -1
        return 0

    def setECP(self, enable: bool = False):
        log(ERROR, "Not Implemented Yet")
        return -1

    def reverseModem(self):
        log(ERROR, "Not Implemented Yet")
        return -1 

    def setConnectorBaudrate(self, emission_baudrate = ConnectorBaudrate.BAUDS_1200, reception_baudrate = ConnectorBaudrate.BAUDS_1200) -> tuple:
        if isinstance(self.__comm, CommSocket):
            log(ERROR, "Baudrate not handled for socket comm")
            return None
        
        if emission_baudrate != reception_baudrate and self.__model == self.Model.MINITEL_1B:
            log(ERROR, "Emission and Reception Baudrate must be symetrical for Minitel 1B Models")
            return None
        
        prog_byte = 1 << 6
        prog_byte |= emission_baudrate.value << 3
        prog_byte |= reception_baudrate.value
        
        command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        if self.send(command):
            log(ERROR, "Error while attempting to send setConnectorBaudrate request")
            return None

        old_baudrate = self.__baudrate
        if type(self.__comm) == CommSerial:
            time.sleep(.5)
            try:
                self.__comm.setBaudrate(emission_baudrate.to_int())
            except CommException:
                log(ERROR, "Error while attempting Comm::setBaudrate")
                return None

        if self.getMinitelInfo() is None:
            log(ERROR, "setConnectorBaudrate failed, Restoring initial baudrate...")

            if type(self.__comm) == CommSerial:
                try:
                    self.__comm.setBaudrate(emission_baudrate.to_int())
                except CommException:
                    log(ERROR, "Error while attempting Comm::setBaudrate")
                    return None

            prog_byte = 1 << 6
            prog_byte |= old_baudrate.value << 3
            prog_byte |= old_baudrate.value

            command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

            if self.send(command):
                log(ERROR, "Error while attempting to send setConnectorBaudrate request")
                return None
            time.sleep(.5)

            answer = self.read(4)
            if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
                log(ERROR, "Response from setConnectorBaudrate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old baudrate...")
                return None

            return old_baudrate, old_baudrate

        # Resending to check new bauderate from answer 
        # TODO - Send GetConnectorBauderate when implemented
        if self.send(command):
            log(ERROR, "Error while attempting to send setConnectorBaudrate request")
            return None
        
        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
            log(ERROR, "Response from setConnectorBaudrate's Request is invalid (got :" + str(answer.hex()) + "), Unable to restore old baudrate...")
            return None

        new_emission_speed = int.from_bytes(answer[3:4], 'little') & (7 << 3)
        new_emission_speed = new_emission_speed >> 3
        new_reception_speed = int.from_bytes(answer[3:4], 'little') & 7

        if new_reception_speed != reception_baudrate.value or new_emission_speed != emission_baudrate.value:
            log(WARNING, "Baudrates not updated, old config returned")

            return old_baudrate, old_baudrate

        return self.ConnectorBaudrate(new_emission_speed), self.ConnectorBaudrate(new_reception_speed)

    def getConnectorBaudrate(self) -> ConnectorBaudrate:
        print("Not Implemented Yet")
        return None

    def setKeyboardMode(self, extended: bool = True, c0: bool = False) -> tuple:
        self.getKeyboardMode()
        if self.__keyboard_extended != extended:
            action = self.START
            if not extended: 
                action = self.STOP
            if self.send(self.PRO3 + action + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] + self.ETEN):
                log(ERROR, "Error while attempting to send setKeyboardMode request")
                return None
            answer = self.read(5)
            if answer is None or answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
                log(ERROR, "Response from setKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
                return None
            
            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self.__keyboard_extended = status & extended_bitfield
            self.__keyboard_c0 = status &  c0_bitfield
            
        if self.__keyboard_c0 != c0:
            action = self.START
            if not c0: 
                action = self.STOP
            if self.send(self.PRO3 + action + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] + self.C0):
                log(ERROR, "Error while attempting to send setKeyboardMode request")
                return None
            answer = self.read(5)
            if answer is None or answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
                log(ERROR, "Response from setKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
                return None 
            
            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self.__keyboard_extended = status & extended_bitfield
            self.__keyboard_c0 = status &  c0_bitfield

        return self.__keyboard_extended, self.__keyboard_c0

    def getKeyboardMode(self) -> tuple:
        if self.send(self.PRO2 + self.GET_KEYBOARD_STATUS + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]):
            log(ERROR, "Error while attempting to send getKeyboardMode request")
            return None
        answer = self.read(5)
        if answer is None or answer[0:2] != self.PRO3 or answer[2:3] != self.REP_KEYBOARD_STATUS or answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]:
            log(ERROR, "Response from getKeyboardMode's Request is invalid (got :" + str(answer.hex()) + ")")
            return None
        
        c0_bitfield = 1 << 2
        extended_bitfield = 1

        status = int.from_bytes(answer[4:5])
        self.__keyboard_extended = status & extended_bitfield
        self.__keyboard_c0 = status &  c0_bitfield

        return self.__keyboard_extended, self.__keyboard_c0

    def enableKeyboard(self, update_cursor: bool = True) -> int:
        res = self.unblockModule(self.Module.KEYBOARD)
        if res is None:
            log(ERROR, 'unblockModule failed, keyboard not enabled')
            return -1
        if update_cursor:
            if self.showCursor():
                log(WARNING, 'Unable to show cursor on enableKeyboard')
        return 0

    def disableKeyboard(self, update_cursor: bool = True) -> int:
        res = self.blockModule(self.Module.KEYBOARD)
        if res is None:
            log(ERROR, 'blockModule failed, keyboard not disabled')
            return -1
        if update_cursor:
            if self.hideCursor():
                log(WARNING, 'Unable to hide cursor on disableKeyboard')
        return 0

    def enableEcho(self) -> int:
        return 0 if self.unblockModule(self.Module.MODEM) is not None else -1

    def disableEcho(self) -> int:
        return 0 if self.blockModule(self.Module.MODEM) is not None else -1

    def setKeyCapsLock(self, enable: bool) -> int: 
        print("Not Implemented Yet")
        return -1

    def setScreenPageMode(self) -> int:
        if not self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already disabled.')
            return 0

        command = self.PRO2 + self.STOP + self.ROULEAU

        if self.send(command):
            log(ERROR, "Error while attempting to send setScreenPageMode request")
            return -1
        answer = self.read(4)
        if answer is None or answer[0:2] !=  self.PRO2:
            log(ERROR, 'setScreenPageMode might have failed, excepted x13x56 but got ' + answer.hex())
            return -1

        self.__roll_mode_enabled = False
        return 0

    def setScreenRollMode(self) -> int:
        if self.__roll_mode_enabled:
            log(INFO, 'Scroll Mode already enabled.')
            return 0
        
        command = self.PRO2 + self.START + self.ROULEAU

        if self.send(command):
            log(ERROR, "Error while attempting to send setScreenRollMode request")
            return -1
        answer = self.read(4)
        if answer is None or answer[0:2] !=  self.PRO2:
            log(ERROR, 'setScreenRollMode might have failed, excepted x13x56 but got ' + answer.hex())
            return -1

        self.__roll_mode_enabled = True
        return 0

    class CopyMode(Enum):
        FR = b'\x6a'
        USA = b'\x6b'

    def copyScreenToConnector(self, mode: CopyMode = CopyMode.FR) -> int:
        print("Not Implemented Yet")
        return -1

    def getModulesFunctionalStates(self) -> int:
        print("Not Implemented Yet")
        return -1
    

    def setTextAttributes(self, color: CharacterColor = None, blinking: bool = None, inverted = None, double_height: bool = None, double_width: bool = None) -> int:
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        if double_height:
            r, c = self.getCursorPosition()
            if r == 1:
                self.newLine()

        if self.send(self.__text_attribute.setAttributes(color=color, blinking=blinking, inverted=inverted, double_height=double_height, double_width=double_width)):
            log(ERROR, "Error while attempting to send TextAttributes")
            return -1
        return 0

    def resetTextAttributes(self) -> int:
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        return self.setTextAttributes(color=CharacterColor.WHITE, blinking=False, inverted=False, double_height=False, double_width=False)

    def setZoneAttributes(self, color: BackgroundColor = None, masking: bool = None, highlight: bool = None):
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')
        
        if self.send(self.__zone_attribute.setAttributes(color=color, masking=masking, highlight=highlight)):
            log(ERROR, "Error while attempting to send ZoneAttributes")
            return -1
        return 0

    def resetZoneAttributes(self) -> int:
        if self.__mode == Mode.MIXED:
            log(WARNING, 'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.')

        return self.setZoneAttributes(color=BackgroundColor.BLACK, masking=False, highlight=False)

    def maskingFullScreen(self) -> int:
        # TODO - TEST
        byte_array = ESC + b'\x23\x20\x58'

        if self.send(byte_array):
            log(ERROR, "Error while attempting to send maskingFullScreen request")
            return -1
        return 0

    def unmaskingFullScreen(self) -> int:
        # TODO - TEST
        bytes_array = ESC + b'\x23\x20\x5f'

        if self.send(bytes_array):
            log(ERROR, "Error while attempting to send unmaskingFullScreen request")
            return -1
        return 0

    def invertText(self) -> int:
        print("Not Implemented Yet")
        return -1

    def invertBackground(self) -> int:
        print("Not Implemented Yet")
        return -1 

    def clear(self) -> int:
        res = 0
        if self.__mode == Mode.VIDEOTEX:
            res = self.send(Layout.clear())
        else:
            res = self.send(Layout.setCursorPosition() + Layout.eraseInDisplay())
        if res:
            log(ERROR, "Error while attempting to send clear request")
            return -1
        return 0

    def newLine(self) -> int:
        if self.send(Layout.cariageReturn() + Layout.moveCursorDown()):
            log(ERROR, "Error while attempting to send newLine request")
            return -1
        return 0
    
    def print(self, text: str) -> int:
        data = b''
        for c in text:
            data += alphanumerical.ascii_to_alphanumerical(c=c, vm=self.__vm)
        
        if self.send(data):
            log(ERROR, "Error while attempting to send text")
            return -1
        return 0
        
    def bind(self, key: KeyboardCode, callback):

        if isinstance(key, FilterKeyboardCode):
            self.__filter_bindings[key] = copy.copy(callback)
            return

        self.__bindings[key] = copy.copy(callback)

    def clearBindings(self):
        for filter in self.__filter_bindings:
            self.__filter_bindings[filter] = None
        
        self.__bindings = {} 

    def readKeyboard(self, timeout: int = None) -> int:
        old_timeout = self.__comm.getTimeout()
        self.__comm.setTimeout(timeout)

        data = self.read(1)
        if data is None:
            log(ERROR, "Error while attempting to read keyboard inputs")
            return -1
        if data[0:1] == b'\x19' or data[0:1] == b'\x13' or data[0:1] == b'\x1b':
            res = self.read(1)
            if res is None:
                log(ERROR, "Error while attempting to read keyboard inputs")
                return -1
            data += res
            if data[1:2] == b'\x4b' or data[1:2] == b'\x5b':
                res = self.read(1)
                if res is None:
                    log(ERROR, "Error while attempting to read keyboard inputs")
                    return -1
                data += res
                if data[2:3] == b'\x34' or data[2:3] == b'\x32':
                    res = self.read(1)
                    if res is None:
                        log(ERROR, "Error while attempting to read keyboard inputs")
                        return -1
                    data += res

        self.__comm.setTimeout(old_timeout)

        callback_called = False

        if len(data):
            print(data.hex())

        if len(data) == 0:
            if self.__filter_bindings[FilterKeyboardCode.No_Keys] is not None:
                self.__filter_bindings[FilterKeyboardCode.No_Keys]()
            return 0
        
        if self.__filter_bindings[FilterKeyboardCode.Any_Keys] is not None:
            self.__filter_bindings[FilterKeyboardCode.Any_Keys]()
            callback_called = True

            try:
                char = VideotexKeyboardCode(data).char()
                if str.isprintable(char):
                    if self.__filter_bindings[FilterKeyboardCode.Printable_Keys]:
                        self.__filter_bindings[FilterKeyboardCode.Printable_Keys](char)
                        callback_called = True
            except ValueError as e:
                log(DEBUG, 'data is not a VideotexKeyboardCode')
                pass
        

        if data in self.__bindings:
            callback = self.__bindings[data]
            callback()
            callback_called = True

        if not callback_called:
            if self.__filter_bindings[FilterKeyboardCode.Other_Keys]:
                self.__filter_bindings[FilterKeyboardCode.Other_Keys]()

        return 0

    def beep(self) -> int:
        if self.send(self.BEL):
            log(ERROR, "Error while attempting to send beep request")
            return -1
        return 0
