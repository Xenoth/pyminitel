import time
import socket

from enum import Enum
from logging import log, ERROR, WARNING, INFO, DEBUG

from pyminitel import alphanumerical
from pyminitel.layout import Layout
from pyminitel.mode import Mode
from pyminitel.visualization_module import VisualizationModule
from pyminitel.keyboard import FilterKeyboardCode, KeyboardCode, VideotexKeyboardCode
from pyminitel.comm import CommSerial, CommSocket, CommException
from pyminitel.attributes import (
    TextAttributes,
    ZoneAttributes,
    CharacterColor,
    BackgroundColor,
    ESC
)

class MinitelException(Exception):
    # Raised on object's instanciation
    pass

class Minitel:
    '''
    Pyminitel Minitel class
    '''

    class ConnectorBaudrate(Enum):
        BAUDS_300 = 2
        BAUDS_1200 = 4
        BAUDS_4800 = 6

        def to_int(self):
            if self.name == 'BAUDS_300':
                return 300
            if self.name == 'BAUDS_1200':
                return 1200
            if self.name == 'BAUDS_4800':
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

    OFF = b'\x60'
    ON = b'\x61'

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
        MINITEL_1_B = 'b'
        MINITEL_1_C = 'c'
        MINITEL_1_R = 'r'

        MINITEL_1_COLOR = 's'

        MINITEL_1_D = 'r'

        MINITEL_10_D = 'd'
        MINITEL_10_F = 'f'

        MINITEL_1B = 'u'

        MINITEL_10B = 'w'

        MINITEL_2 = 'v'

        MINITEL_12 = 'z'

        MINITEL_5 = 'y'


    def __init__(
            self,
            port: str,
            baudrate = ConnectorBaudrate.BAUDS_1200,
            ip: str = None,
            mode: Mode = Mode.VIDEOTEX,
            timeout: float = None,
            tcp: socket = None
    ):
        '''
        Minitel's constructor - This function is raising MinitelException if unable to retreive
        basic minitel's information. This object will instantiate a serial communication or a
        TCP socket (as server) depending if "ip" argument given is None or not.
        TCP Socket communication will block until client has been found.

            Parameters:
                port (str): Either Serial's port or IP's port (ex: '/dev/ttyUSB0' or '8080') -
                            The value has no effect on deciding the type of communication
                bauderate (Minitel.ConnectorBaudrate):  The bauderate of DIN's connector -
                                                        Default 1200
                ip (str):   IP for TCP Socket server - When not None the constructor will attempt to
                            use Socket - Default None
                mode (Mode): Minitel's Mode - Default is Videotex (standard mode)
                timeout (float): Set the comm timeout (default None)

            Returns:
                Minitel instantiated object if basics minitel info retreived
                else raises MinitelException

        '''

        self._port = None
        self._baudrate = None
        self._comm = None

        self._manufacturer = None
        self._model = None
        self._fw_version = None

        self._keyboard_extended = None
        self._keyboard_c0 = None
        self._keyboard_caps_enabled = None
        self._pce_enabled = None
        self._roll_mode_enabled = None
        self._mode = None
        self._vm = None

        # TODO - Warning on insersion or suppression when double sizes
        self._text_attribute = None
        self._zone_attribute = None

        self._filter_bindings = {
            FilterKeyboardCode.Any_Keys: None,
            FilterKeyboardCode.Printable_Keys: None,
            FilterKeyboardCode.Other_Keys: None,
            FilterKeyboardCode.No_Keys : None,
        }
        self._bindings = None

        if not ip and not tcp:
            try:
                self._comm = CommSerial(port=port, baudrate=baudrate.to_int(), timeout=timeout)
            except CommException as e:
                log(ERROR, 'Unable to open Serial - ' + str(e))
                raise MinitelException from e
        else:
            try:
                int_port = None
                if port:
                    int_port = int(port)
                self._comm = CommSocket(port=int_port, host=ip, timeout=timeout, tcp=tcp)
            except CommException as e:
                log(ERROR, 'Unable to create socket - ' + str(e))
                raise MinitelException from e

        log(level=DEBUG, msg='New Comm: id ' + str(id(self._comm)))

        try:
            self._comm.start()
        except RuntimeError:
            log(ERROR, 'Thread of Comm already started')

        if timeout is None:
            self._comm.set_timeout(10)

        self._port = port
        self._baudrate = baudrate

        self._text_attribute = TextAttributes()
        self._zone_attribute = ZoneAttributes()

        self._bindings = {}

        res = self.get_minitel_info()
        if res is None:
            log(ERROR, 'Unable to communicate with the minitel, bad baudrate or com port.')
            raise MinitelException


        print('[Minitel Info]')
        print('- ROM ID: "' + self._manufacturer.value + self._model.value + self._fw_version + '"')
        print('* Manufacturer: ' + self._manufacturer.name)
        print('* Model: ' + self._model.name)
        print('* Firmware Version: ' + self._fw_version)

        if self.get_visualization_module() is None:
            log(ERROR, 'Unable to retrive with the minitel visualization module')
        else:
            print('* Visualization Module: ' + self._vm.name)

        if self._model != self.Model.MINITEL_1B:
            log(WARNING, 'pyMinitel is supporting MINITEL 1B for now, try at your own risk.')

        if self.get_module_operating_mode_status() is None:
            log(ERROR, 'Unable to retrive with the minitel module operating mode status')
        else:
            print('[Modules Operating Mode Status]')
            print('* isKeyboadCapsLocked: ' + str(self._keyboard_caps_enabled))
            print('* PCE: ' + str(self._pce_enabled))
            print('* Roll Mode: ' + str(self._roll_mode_enabled))
            print('* Screen Mode: ' + str(self._mode.name))

        if self.set_video_mode(mode):
            log(ERROR, 'Unable to set video mode')
        else:
            print('* New Video Mode:' + str(self._mode.name))

        if self.get_keyboard_mode() is None:
            log(ERROR, 'Unable to retreive keyboard mode')
        else:
            print('* Keyboard Extended: ' + str(self._keyboard_extended))
            print('* Keyboard C0: ' + str(self._keyboard_c0))

        if timeout is None:
            self._comm.set_timeout(None)

    def __del__(self):
        if self._comm:
            if not self._comm.stopped():
                self._comm.stop()
                self._comm.join()

            self._comm.close()

    def read(self, n: bytes) -> bytes:
        try:
            return self._comm.read(n)
        except CommException as e:
            log(ERROR, 'Got Exception while attempting to send message - ' + str(e))
            return None


    def send(self, data: bytes) -> int:
        try:
            self._comm.put(data)
        except CommException as e:
            log(ERROR, 'Got Exception while attempting to send message - ' + str(e))
            return -1

        return 0

    def switch_receiver_transmitter(
            self, 
            receiver: Module, 
            transmitter: Module, 
            on: bool = True
    ) -> dict:
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

        command = self.PRO3
        command += self.ON if on else self.OFF
        command += self.IO_CODES[receiver][self.IO.IN] + self.IO_CODES[transmitter][self.IO.OUT]

        if self.send(command):
            log(ERROR, "Error while attempting to send switch_receiver_transmitter request")
            return None
        answer = self.read(5)
        if (
            answer is None or
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.FROM or
            answer[3:4] != self.IO_CODES[receiver][self.IO.IN]
        ):
            log(
                ERROR,
                "Response from switch_receiver_transmitter's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        return {
            self.Module.SCREEN: int.from_bytes(answer[4:5]) & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: int.from_bytes(answer[4:5]) & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: int.from_bytes(answer[4:5]) & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: int.from_bytes(answer[4:5]) & self.CONNECTOR_STATUS_BITFIELD,
        }

    def block_module(self, module: Module) -> bool:
        '''
        Block the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to block
            Returns:
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''
        res = self.switch_receiver_transmitter(module, module, False)
        return res[module] == 1 if res is not None else None

    def unblock_module(self, module: Module) -> bool:
        '''
        Unblock the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to unblock
            Returns:
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''
        res = self.switch_receiver_transmitter(module, module, True)
        return res[module] == 1 if res is not None else None

    def get_module_io_status(self, module: Module, io: IO) -> dict:
        # TODO - Try IRL
        command = self.PRO2 + self.TO + self.IO_CODES[module][io]

        if self.send(command):
            log(ERROR, "Error while attempting to send get_module_IO_status request")
            return None
        answer = self.read(5)
        if (
            answer is None or
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.FROM or
            answer[3:4] != self.IO_CODES[module.value][io.value]
        ):
            log(
                ERROR,
                "Response from get_module_IO_status's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        return {
            self.Module.SCREEN: answer[4:5] & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: answer[4:5] & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: answer[4:5] & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: answer[4:5] & self.CONNECTOR_STATUS_BITFIELD,
        }

    def set_module_diffusion(self, module: Module, activate: bool = True):
        # TODO  - FINISH
        command = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module][self.IO.IN]

        print(command.hex())

    def set_module_ack(self, module: Module, activate: bool = True):
        # TODO - Try IRL
        command = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module.value][self.IO.OUT]

        self.send(command)

    def get_protocol_status(self) -> dict:
        # TODO - Try IRL
        command = self.PRO1 + self.STATUS_PROTOCOL_REQUEST

        if self.send(command):
            log(ERROR, "Error while attempting to send get_protocol_status request")
            return None

        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
            log(
                ERROR,
                "Response from getStatusProtocol's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        return {
            'D1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D1,
            'D2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_D2,
            'A1': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A1,
            'A2': answer[3:4] & self.BITFIELD_STATUS_PROTOCOL_A2,
            'PAD_X3_COMPATIBLE': answer[4] & self.BITFIELD_STATUS_PROTOCOL_PAD,
        }

    def set_protocol_transparency(self, n: int) -> int:
        # TODO - Try IRL
        if n < 1 or n > 127:
            log(ERROR, "Invalid Argument, n should be between 1-127, got " + n + "")
            return -1

        bit_n = n.to_bytes(1, 'little')
        bit_n |= (1<<7)

        command = self.PRO2 + b'\x66' + bit_n

        if self.send(command):
            log(ERROR, "Error while attempting to send set_protocol_transparency request")
            return -1

        answer = self.read(2)
        if answer is None or answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            log(
                ERROR,
                "Response from set_protocol_transparency's Request is invalid (got : %s)",
                answer.hex()
            )
            return -1

        return 0

    def get_minitel_info(self) -> tuple:
        command = self.PRO1 + self.ENQROM

        if self.send(command):
            log(ERROR, "Error while attempting to send get_minitel_info request")
            return None

        answer = self.read(5)
        if answer is None or answer[0:1] != self.SOH or answer[4:5] != self.EOT:
            log(
                ERROR,
                "Response from get_minitel_info's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        self._manufacturer = self.Manufacturer(answer[1:2].decode())
        self._model = self.Model(answer[2:3].decode())
        self._fw_version = answer[3:4].decode()

        return self._manufacturer, self._model, self._fw_version

    def get_visualization_module(self) -> VisualizationModule:
        if self._model == self.Model.MINITEL_1B:
            if (
                self._manufacturer == self.Manufacturer.TRT_PHILIPS or
                self._fw_version == '5' or
                self._fw_version == ';' or
                self._fw_version == '<'
            ):
                self._vm = VisualizationModule.VGP5
            elif (
                self._manufacturer == self.Manufacturer.TELIC_MATRA and
                self._fw_version in ('2', '3', '4')
            ):
                self._vm = VisualizationModule.VGP2
            else:
                log(ERROR, 'Unknown Visualization Module - Default is ' + self._vm.name)
        else:
            self._vm = VisualizationModule.VGP2
            log(
                WARNING, 'Not handling models other than %s (got model: %s), Default is %s',
                str(self.Model.MINITEL_1B),
                str(self._model),
                str(self._vm.name)
            )
        return self._vm

    def get_module_operating_mode_status(self) -> tuple:
        command = self.PRO1 + self.OPERATING_STATUS

        if self.send(command):
            log(ERROR, "Error while attempting to send get_module_operating_mode_status request")
            return None

        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != self.OPERATING_STATUS_RES:
            log(
                ERROR,
                "Response from get_module_operating_mode_status's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        status = int.from_bytes(answer[3:4])

        keyboard_caps_lock_bit = 1 << 3
        pce_bitfield_bit = 1 << 2
        roll_mode_bit = 1 << 1
        screen_format_bit = 1

        self._keyboard_caps_enabled = status & keyboard_caps_lock_bit == 0
        self._pce_enabled = status & pce_bitfield_bit == 1
        self._roll_mode_enabled = status & roll_mode_bit == 1
        if status & screen_format_bit == 0:
            self._mode = Mode.VIDEOTEX
        else:
            self._mode = Mode.MIXED

        return self._keyboard_caps_enabled, self._pce_enabled, self._roll_mode_enabled, self._mode

    def set_video_mode(self, mode: Mode = Mode.VIDEOTEX) -> int:
        if mode is None:
            log(ERROR, 'Invalid None Argument')
            return -1
        if self._mode == mode:
            log(INFO, 'Video Mode already set in ' + mode.name + ' mode')
            return 0

        command = self.PRO2

        if mode == Mode.MIXED:
            command += self.MIXTE1
        else:
            command += self.MIXTE2

        if self.send(command):
            log(ERROR, "Error while attempting to send set_video_mode request")
            return -1

        answer = self.read(2)
        if  (
            answer is None or
            mode == Mode.MIXED and
            answer[0:2] != self.SEP + b'\x70' or
            mode == Mode.VIDEOTEX
            and answer[0:2] != self.SEP + b'\x71'
        ):
            log(
                ERROR,
                "Response from set_video_mode's Request is invalid (got : %s)",
                answer.hex()
            )
            return -1

        self._mode = mode
        return 0

    def get_cursor_position(self) -> tuple:
        command = self.ESC + b'\x61'

        if self.send(command):
            log(ERROR, "Error while attempting to send get_cursor_position request")
            return None

        answer = self.read(3)
        if answer is None or answer[0:1] != self.US:
            log(
                ERROR,
                "Response from get_cursor_position's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        mask = 63
        return int.from_bytes(answer[1:2]) & mask, int.from_bytes(answer[2:3]) & mask

    def show_cursor(self) -> int:
        if self.send(b'\x11'):
            log(ERROR, "Error while attempting to send show_cursor request")
            return -1
        return 0

    def hide_cursor(self) -> int:
        if self.send(b'\x14'):
            log(ERROR, "Error while attempting to send hide_cursor request")
            return -1
        return 0

    def connect_modem(self) -> int:
        # TODO - Try IRL
        if self.send(self.PRO1 + b'\x68'):
            log(ERROR, "Error while attempting to send connect_modem request")
            return -1
        return 0

    def disconnect_modem(self) -> int:
        # TODO - Try IRL
        if self.send(self.PRO1 + b'\x67'):
            log(ERROR, "Error while attempting to send disconnect_modem request")
            return -1
        return 0

    def set_ecp(self, enable: bool = False):
        # TODO - Implementation
        log(ERROR, "Not Implemented Yet")
        return -1

    def reverse_modem(self):
        # TODO - Implementation
        log(ERROR, "Not Implemented Yet")
        return -1

    def set_connector_baudrate(
            self,
            emission_baudrate = ConnectorBaudrate.BAUDS_1200,
            reception_baudrate = ConnectorBaudrate.BAUDS_1200
    ) -> tuple:
        if isinstance(self._comm, CommSocket):
            log(ERROR, "Baudrate not handled for socket comm")
            return None

        if emission_baudrate != reception_baudrate and self._model == self.Model.MINITEL_1B:
            log(ERROR, "Emission and Reception Baudrate must be symetrical for Minitel 1B Models")
            return None

        prog_byte = 1 << 6
        prog_byte |= emission_baudrate.value << 3
        prog_byte |= reception_baudrate.value

        command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        if self.send(command):
            log(ERROR, "Error while attempting to send set_connector_baudrate request")
            return None

        old_baudrate = self._baudrate
        if type(self._comm) == CommSerial:
            time.sleep(.5)
            try:
                self._comm.set_baudrate(emission_baudrate.to_int())
            except CommException:
                log(ERROR, "Error while attempting Comm::set_baudrate")
                return None

        if self.get_minitel_info() is None:
            log(ERROR, "set_connector_baudrate failed, Restoring initial baudrate...")

            if type(self._comm) == CommSerial:
                try:
                    self._comm.set_baudrate(emission_baudrate.to_int())
                except CommException:
                    log(ERROR, "Error while attempting Comm::set_baudrate")
                    return None, None

            prog_byte = 1 << 6
            prog_byte |= old_baudrate.value << 3
            prog_byte |= old_baudrate.value

            command = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

            if self.send(command):
                log(ERROR, "Error while attempting to send set_connector_baudrate request")
                return None, None
            time.sleep(.5)

            answer = self.read(4)
            if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
                log(
                    ERROR,
                    "Response from set_connector_baudrate's Request is invalid (got : %s), "
                    "Unable to restore old baudrate...",
                    answer.hex()
                )
                return None, None

            return old_baudrate, old_baudrate

        # Resending to check new bauderate from answer
        # TODO - Send GetConnectorBauderate when implemented
        if self.send(command):
            log(ERROR, "Error while attempting to send set_connector_baudrate request")
            return None, None

        answer = self.read(4)
        if answer is None or answer[0:2] != self.PRO2 or answer[2:3] != b'\x75':
            log(
                ERROR,
                "Response from set_connector_baudrate's Request is invalid (got : %s), "
                "Unable to restore old baudrate...",
                answer.hex()
            )
            return None, None

        new_emission_speed = int.from_bytes(answer[3:4], 'little') & (7 << 3)
        new_emission_speed = new_emission_speed >> 3
        new_reception_speed = int.from_bytes(answer[3:4], 'little') & 7

        if (
            new_reception_speed != reception_baudrate.value or
            new_emission_speed != emission_baudrate.value
        ):
            log(WARNING, "Baudrates not updated, old config returned")

            return old_baudrate, old_baudrate

        return (
            self.ConnectorBaudrate(new_emission_speed),
            self.ConnectorBaudrate(new_reception_speed)
        )

    def get_connector_baudrate(self) -> ConnectorBaudrate:
        # TODO - Implementation
        print("Not Implemented Yet")

    def set_keyboard_mode(self, extended: bool = True, c0: bool = False) -> tuple:
        self.get_keyboard_mode()
        if self._keyboard_extended != extended:
            action = self.START
            if not extended:
                action = self.STOP
            if self.send(
                self.PRO3 +
                action +
                self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] +
                self.ETEN
            ):
                log(ERROR, "Error while attempting to send set_keyboard_mode request")
                return None
            answer = self.read(5)
            if (
                answer is None or
                answer[0:2] != self.PRO3 or
                answer[2:3] != self.REP_KEYBOARD_STATUS or
                answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
            ):
                log(
                    ERROR,
                    "Response from set_keyboard_mode's Request is invalid (got : %s)",
                    answer.hex()
                )
                return None

            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self._keyboard_extended = status & extended_bitfield
            self._keyboard_c0 = status &  c0_bitfield

        if self._keyboard_c0 != c0:
            action = self.START
            if not c0:
                action = self.STOP
            if self.send(
                self.PRO3 +
                action +
                self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] +
                self.C0
            ):
                log(ERROR, "Error while attempting to send set_keyboard_mode request")
                return None
            answer = self.read(5)
            if (
                answer is None or
                answer[0:2] != self.PRO3 or
                answer[2:3] != self.REP_KEYBOARD_STATUS or
                answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
            ):
                log(
                    ERROR,
                    "Response from set_keyboard_mode's Request is invalid (got : %s)",
                    answer.hex()
                )
                return None

            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self._keyboard_extended = status & extended_bitfield
            self._keyboard_c0 = status &  c0_bitfield

        return self._keyboard_extended, self._keyboard_c0

    def get_keyboard_mode(self) -> tuple:
        if self.send(
            self.PRO2 +
            self.GET_KEYBOARD_STATUS +
            self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
        ):
            log(ERROR, "Error while attempting to send get_keyboard_mode request")
            return None
        answer = self.read(5)
        if (
            answer is None or
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.REP_KEYBOARD_STATUS or
            answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
        ):
            log(
                ERROR,
                "Response from get_keyboard_mode's Request is invalid (got : %s)",
                answer.hex()
            )
            return None

        c0_bitfield = 1 << 2
        extended_bitfield = 1

        status = int.from_bytes(answer[4:5])
        self._keyboard_extended = status & extended_bitfield
        self._keyboard_c0 = status &  c0_bitfield

        return self._keyboard_extended, self._keyboard_c0

    def enable_keyboard(self, update_cursor: bool = True) -> int:
        res = self.unblock_module(self.Module.KEYBOARD)
        if res is None:
            log(ERROR, 'unblock_module failed, keyboard not enabled')
            return -1
        if update_cursor:
            if self.show_cursor():
                log(WARNING, 'Unable to show cursor on enable_keyboard')
        return 0

    def disable_keyboard(self, update_cursor: bool = True) -> int:
        res = self.block_module(self.Module.KEYBOARD)
        if res is None:
            log(ERROR, 'block_module failed, keyboard not disabled')
            return -1
        if update_cursor:
            if self.hide_cursor():
                log(WARNING, 'Unable to hide cursor on disable_keyboard')
        return 0

    def enable_echo(self) -> int:
        return 0 if self.unblock_module(self.Module.MODEM) is not None else -1

    def disable_echo(self) -> int:
        return 0 if self.block_module(self.Module.MODEM) is not None else -1

    def set_key_caps_lock(self, enable: bool) -> int:
        # TODO - Implementation
        print("Not Implemented Yet")

    def set_screen_page_mode(self) -> int:
        if not self._roll_mode_enabled:
            log(INFO, 'Scroll Mode already disabled.')
            return 0

        command = self.PRO2 + self.STOP + self.ROULEAU

        if self.send(command):
            log(ERROR, "Error while attempting to send set_screen_page_mode request")
            return -1
        answer = self.read(4)
        if answer is None or answer[0:2] !=  self.PRO2:
            log(
                ERROR,
                "set_screen_page_mode might have failed, excepted x13x56 but got %s",
                answer.hex()
            )
            return -1

        self._roll_mode_enabled = False
        return 0

    def set_screen_roll_mode(self) -> int:
        if self._roll_mode_enabled:
            log(INFO, 'Scroll Mode already enabled.')
            return 0

        command = self.PRO2 + self.START + self.ROULEAU

        if self.send(command):
            log(ERROR, "Error while attempting to send set_screen_roll_mode request")
            return -1
        answer = self.read(4)
        if answer is None or answer[0:2] !=  self.PRO2:
            log(
                ERROR,
                "set_screen_roll_mode might have failed, excepted x13x56 but got %s",
                answer.hex()
            )
            return -1

        self._roll_mode_enabled = True
        return 0

    class CopyMode(Enum):
        FR = b'\x6a'
        USA = b'\x6b'

    def copy_screen_to_connector(self, mode: CopyMode = CopyMode.FR) -> int:
        # TODO - Implementation
        print("Not Implemented Yet")

    def get_modules_functional_states(self) -> int:
        # TODO - Implementation
        print("Not Implemented Yet")

    def set_text_attributes(
            self,
            color: CharacterColor = None,
            blinking: bool = None,
            inverted = None,
            double_height: bool = None,
            double_width: bool = None
    ) -> int:

        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        if double_height:
            r, _ = self.get_cursor_position()
            if r == 1:
                self.new_line()

        if self.send(
            self._text_attribute.set_attributes(
                color=color, blinking=blinking,
                inverted=inverted,
                double_height=double_height,
                double_width=double_width
            )
        ):
            log(ERROR, "Error while attempting to send TextAttributes")
            return -1
        return 0

    def reset_text_attributes(self) -> int:
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        return self.set_text_attributes(
            color=CharacterColor.WHITE,
            blinking=False,
            inverted=False,
            double_height=False,
            double_width=False
        )

    def set_zone_attributes(
            self,
            color: BackgroundColor = None,
            masking: bool = None,
            highlight: bool = None
    ):
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        if self.send(
            self._zone_attribute.set_attributes(color=color, masking=masking, highlight=highlight)
        ):
            log(ERROR, "Error while attempting to send ZoneAttributes")
            return -1
        return 0

    def reset_zone_attributes(self) -> int:
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        return self.set_zone_attributes(color=BackgroundColor.BLACK, masking=False, highlight=False)

    def masking_fullscreen(self) -> int:
        # TODO - Try IRL
        byte_array = ESC + b'\x23\x20\x58'

        if self.send(byte_array):
            log(ERROR, "Error while attempting to send masking_fullscreen request")
            return -1
        return 0

    def unmasking_fullscreen(self) -> int:
        # TODO - Try IRL
        bytes_array = ESC + b'\x23\x20\x5f'

        if self.send(bytes_array):
            log(ERROR, "Error while attempting to send unmasking_fullscreen request")
            return -1
        return 0

    def invert_text(self) -> int:
        # TODO - Implementation
        print("Not Implemented Yet")
        return -1

    def invert_background(self) -> int:
        # TODO - Implementation
        print("Not Implemented Yet")
        return -1

    def clear(self) -> int:
        res = 0
        if self._mode == Mode.VIDEOTEX:
            res = self.send(Layout.clear())
        else:
            res = self.send(Layout.set_cursor_position() + Layout.erase_in_display())
        if res:
            log(ERROR, "Error while attempting to send clear request")
            return -1
        return 0

    def new_line(self) -> int:
        if self.send(Layout.cariage_return() + Layout.move_cursor_down()):
            log(ERROR, "Error while attempting to send new_line request")
            return -1
        return 0

    def print(self, text: str) -> int:
        data = b''
        for c in text:
            data += alphanumerical.ascii_to_alphanumerical(c=c, vm=self._vm)

        if self.send(data):
            log(ERROR, "Error while attempting to send text")
            return -1
        return 0

    def bind(self, key: KeyboardCode, callback):
        if isinstance(key, FilterKeyboardCode):
            self._filter_bindings[key] = (callback)
            return

        self._bindings[key] = (callback)

    def clear_bindings(self):
        for filter_it in self._filter_bindings:
            self._filter_bindings[filter_it] = None

        self._bindings = {}

    def read_keyboard(self, timeout: int = None) -> int:
        old_timeout = self._comm.get_timeout()
        self._comm.set_timeout(timeout)

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

        self._comm.set_timeout(old_timeout)

        callback_called = False

        if len(data):
            print(data.hex())

        if len(data) == 0:
            if self._filter_bindings[FilterKeyboardCode.No_Keys] is not None:
                if callable(self._filter_bindings[FilterKeyboardCode.No_Keys]):
                    self._filter_bindings[FilterKeyboardCode.No_Keys]()
            return 0

        if self._filter_bindings[FilterKeyboardCode.Any_Keys] is not None:
            if callable(self._filter_bindings[FilterKeyboardCode.Any_Keys]):
                self._filter_bindings[FilterKeyboardCode.Any_Keys]()
                callback_called = True

        try:
            char = VideotexKeyboardCode(data).char()

            if str.isprintable(char):
                if self._filter_bindings[FilterKeyboardCode.Printable_Keys]:
                    if callable(self._filter_bindings[FilterKeyboardCode.Printable_Keys]):
                        self._filter_bindings[FilterKeyboardCode.Printable_Keys](char)
                        callback_called = True
        except ValueError:
            log(DEBUG, 'data is not a VideotexKeyboardCode')

        if data in self._bindings:
            callback = self._bindings[data]
            callback()
            callback_called = True

        if not callback_called:
            if self._filter_bindings[FilterKeyboardCode.Other_Keys]:
                if callable(self._filter_bindings[FilterKeyboardCode.Other_Keys]):
                    self._filter_bindings[FilterKeyboardCode.Other_Keys]()

        return 0

    def beep(self) -> int:
        if self.send(self.BEL):
            log(ERROR, "Error while attempting to send beep request")
            return -1
        return 0
