"""
minitel.py

This module contains the main class of pyminitel library,
allowing to drive a distant Minitel device.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import time
from socket import socket

from typing import Callable, Final
from enum import Enum
from logging import log, WARNING

from pyminitel import alphanumerical
from pyminitel.layout import Layout
from pyminitel.mode import Mode
from pyminitel.visualization_module import VisualizationModule
from pyminitel.keyboard import FilterKeyboardCode, KeyboardCode, VideotexKeyboardCode, char
from pyminitel.comm import Comm, CommSerial, CommSocket, CommException
from pyminitel.attributes import (
    TextAttributes,
    ZoneAttributes,
    CharacterColor,
    BackgroundColor,
    TextAttributesState,
    ZoneAttributesState,
    ESC
)

class MinitelException(Exception):
    pass

class MinitelConnectionException(MinitelException):
    pass

class MinitelNotConnectedException(MinitelConnectionException):
    pass

class MinitelSocketConnectionException(MinitelConnectionException):
    pass

class MinitelSerialConnectionException(MinitelConnectionException):
    pass

class MinitelSendException(MinitelException):
    def __init__(self, data: str):
        super().__init__(f"Error while attempting to put {data}")

class MinitelReadException(MinitelException):
    def __init__(self, n: int):
        super().__init__(f"Error while attempting to read {n} bytes")

class MinitelRequestException(MinitelException):
    def __init__(self, func_name: str):
        super().__init__(f"Error while attempting to send {func_name} request")

class MinitelResponseException(MinitelException):
    def __init__(self, func_name: str):
        super().__init__(f"Error while attempting to read {func_name} response")

class MinitelInvalidResponseException(MinitelException):
    def __init__(self, func_name: str, expected: str, actual: str):
        super().__init__(f"Error parsing {func_name}'s response: Expected {expected} but got {actual}")

class MinitelInvalidArgumentException(MinitelException):
    pass

class MinitelKeyboardException(MinitelException):
    pass

class MinitelNotImplementedException(MinitelException):
    pass

class Minitel:
    '''
    Pyminitel Minitel class
    '''

    class ConnectorBaudrate(Enum):
        BAUDS_300 = 2
        BAUDS_1200 = 4
        BAUDS_4800 = 6

        def __int__(self) -> int:
            if self.name == 'BAUDS_300':
                return 300
            if self.name == 'BAUDS_1200':
                return 1200
            if self.name == 'BAUDS_4800':
                return 4800

            return 0

        def __str__(self) -> str:
            if self.name == 'BAUDS_300':
                return '300'
            if self.name == 'BAUDS_1200':
                return '1200'
            if self.name == 'BAUDS_4800':
                return '4800'

            return '0'

    ESC: Final[bytes] = b'\x1b'
    US: Final[bytes] = b'\x1F'

    START: Final[bytes] = b'\x69'
    STOP: Final[bytes] = b'\x6a'

    ROULEAU: Final[bytes] = b'\x43'
    PROCEDURE: Final[bytes] = b'\x44'
    MINUSCULE: Final[bytes] = b'\x45'

    BEL: Final[bytes] = b'\x07'

    SEP: Final[bytes] = b'\x13'
    PRO1: Final[bytes] = ESC + b'\x39'
    PRO2: Final[bytes] = ESC + b'\x3a'
    PRO3: Final[bytes] = ESC + b'\x3b'
    PROG: Final[bytes] = b'\x6b'

    TO: Final[bytes] = b'\x62'
    FROM: Final[bytes] = b'\x63'

    SCREEN_STATUS_BITFIELD: Final[int] = 1 << 0
    KEYBOARD_STATUS_BITFIELD: Final[int] = 1 << 1
    MODEM_STATUS_BITFIELD: Final[int] = 1 << 2
    CONNECTOR_STATUS_BITFIELD: Final[int] = 1 << 3

    COMMAND_CODE_ENABLE: Final[bytes] = b'\x64'
    COMMAND_CODE_DISABLE: Final[bytes] = b'\x65'

    STATUS_PROTOCOL_REQUEST: Final[bytes] = b'\x76'
    STATUS_PROTOCOL_ANSWER: Final[bytes] = b'\x77'

    BITFIELD_STATUS_PROTOCOL_D1: Final[int] = 1 << 0
    BITFIELD_STATUS_PROTOCOL_D2: Final[int] = 1 << 1
    BITFIELD_STATUS_PROTOCOL_A1: Final[int] = 1 << 2
    BITFIELD_STATUS_PROTOCOL_A2: Final[int] = 1 << 3
    BITFIELD_STATUS_PROTOCOL_PAD: Final[int] = 1 << 4

    SOH: Final[bytes] = b'\x01'
    EOT: Final[bytes] = b'\x04'
    ENQROM: Final[bytes] = b'\x7b'

    MIXTE1: Final[bytes] = b'\x32\x7d'
    MIXTE2: Final[bytes] = b'\x32\x7e'

    OPERATING_STATUS: Final[bytes] = b'\x72'
    OPERATING_STATUS_RES: Final[bytes] = b'\x73'

    ETEN: Final[bytes] = b'\x41'
    C0: Final[bytes] = b'\x43'

    GET_KEYBOARD_STATUS: Final[bytes] = b'\x72'
    REP_KEYBOARD_STATUS: Final[bytes] = b'\x73'

    OFF: Final[bytes] = b'\x60'
    ON: Final[bytes] = b'\x61'

    class Module(Enum):
        SCREEN = 1
        KEYBOARD = 2
        MODEM = 3
        CONNECTOR = 4

    class IO(Enum):
        IN = 1
        OUT = 2

    IO_CODES: Final[dict[Module, dict[IO, bytes]]] = {
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

    def __init__(self) -> None:

        self._comm: Comm | None = None
        self._baudrate: Minitel.ConnectorBaudrate | None = None

        self._manufacturer: Minitel.Manufacturer | None = None
        self._model: Minitel.Model | None = None
        self._fw_version: str | None = None

        self._keyboard_extended: bool | None = None
        self._keyboard_c0: bool | None = None
        self._keyboard_caps_enabled: bool | None = None
        self._pce_enabled: bool | None = None
        self._roll_mode_enabled: bool | None = None
        self._mode: Mode | None = None
        self._vm: VisualizationModule = VisualizationModule.VGP2


        self._filter_bindings: dict[FilterKeyboardCode, Callable[..., None] | None] = {
            FilterKeyboardCode.ANY_KEYS: None,
            FilterKeyboardCode.PRINTABLE_KEYS: None,
            FilterKeyboardCode.OTHER_KEYS: None,
            FilterKeyboardCode.NO_KEYS : None,
        }

        self._bindings: dict[bytes, Callable] = {}

        # TODO - Warning on insertion or suppression when double sizes
        self._text_attribute: TextAttributes = TextAttributes()
        self._zone_attribute: ZoneAttributes = ZoneAttributes()

    def __del__(self):
        if not self._comm:
            return

        if not self._comm.stopped():
            self._comm.stop()
            self._comm.join()

        self._comm.close()

    def connect_socket(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        tcp: socket | None = None
    ) -> None:

        try:
            self._comm = CommSocket(host=host, port=port, timeout=timeout, tcp=tcp)
        except CommException as e:
            raise MinitelSocketConnectionException() from e

        self._comm.set_timeout(None)

        try:
            self._comm.start()
        except RuntimeError:
            log(WARNING, 'Thread of Comm already started')


    def connect_serial(
        self,
        port: str,
        baudrate: ConnectorBaudrate = ConnectorBaudrate.BAUDS_1200,
        timeout: float | None = None
    ) -> None:

        try:
            self._comm = CommSerial(port=port, baudrate=int(baudrate), timeout=timeout)
        except CommException as e:
            raise MinitelSerialConnectionException() from e

        self._comm.set_timeout(None)

        try:
            self._comm.start()
        except RuntimeError:
            log(WARNING, 'Thread of Comm already started')

    def read(self, n: int) -> bytes:

        if self._comm is None:
            raise MinitelNotConnectedException()

        try:
            return self._comm.read(n)
        except CommException as e:
            raise MinitelReadException(n) from e

    def send(self, data: bytes) -> None:

        if self._comm is None:
            raise MinitelNotConnectedException()

        try:
            self._comm.put(data)
        except CommException as e:
            raise MinitelSendException(data.hex()) from e

    def switch_receiver_transmitter(
            self,
            receiver: Module,
            transmitter: Module,
            on: bool = True
    ) -> dict[Module, int]:

        if (
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.CONNECTOR) or
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.MODEM) or
            (receiver == self.Module.CONNECTOR and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.CONNECTOR and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.MODEM and transmitter == self.Module.SCREEN) or
            (receiver == self.Module.KEYBOARD and transmitter == self.Module.SCREEN)
        ):
            raise MinitelInvalidArgumentException(
                'Switching ' + transmitter.name + ' -> ' + receiver.name + 'is not possible'
            )

        command: bytes = self.PRO3
        command += self.ON if on else self.OFF
        command += self.IO_CODES[receiver][self.IO.IN] + self.IO_CODES[transmitter][self.IO.OUT]

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(5)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if (
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.FROM or
            answer[3:4] != self.IO_CODES[receiver][self.IO.IN]
        ):
            raise MinitelInvalidResponseException(
                __name__,
                (self.PRO3 + self.FROM + self.IO_CODES[receiver][self.IO.IN]).hex() + '..',
                answer.hex()
            )

        return {
            Minitel.Module.SCREEN: int.from_bytes(answer[4:5]) & self.SCREEN_STATUS_BITFIELD,
            Minitel.Module.KEYBOARD: int.from_bytes(answer[4:5]) & self.KEYBOARD_STATUS_BITFIELD,
            Minitel.Module.MODEM: int.from_bytes(answer[4:5]) & self.MODEM_STATUS_BITFIELD,
            Minitel.Module.CONNECTOR: int.from_bytes(answer[4:5]) & self.CONNECTOR_STATUS_BITFIELD,
        }

    def block_module(self, module: Module) -> bool:
        '''
        Block the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to block
            Returns:
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''

        modules_status: dict[Minitel.Module, int] = self.switch_receiver_transmitter(module, module, False)
        return modules_status[module] == 1

    def unblock_module(self, module: Module) -> bool:
        '''
        Unblock the Minitel's Module.

            Parameters:
                module (Minitel.Module): Module to unblock
            Returns:
                is_module_unblocked (bool): Is module unblocked, else blocked
        '''

        modules_status: dict[Minitel.Module, int] = self.switch_receiver_transmitter(module, module, True)
        return modules_status[module] == 1

    def get_module_io_status(self, module: Module, io: IO) -> dict[Module, int]:
        # TODO - Try IRL
        command: bytes = self.PRO2 + self.TO + self.IO_CODES[module][io]

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(5)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if (
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.FROM or
            answer[3:4] != self.IO_CODES[module][io]
        ):
            raise MinitelInvalidResponseException(
                __name__,
                (self.PRO3 + self.FROM + self.IO_CODES[module][io]).hex() + '..',
                answer.hex()
            )

        return {
            self.Module.SCREEN: int.from_bytes(answer[4:5], "big") & self.SCREEN_STATUS_BITFIELD,
            self.Module.KEYBOARD: int.from_bytes(answer[4:5], "big") & self.KEYBOARD_STATUS_BITFIELD,
            self.Module.MODEM: int.from_bytes(answer[4:5], "big") & self.MODEM_STATUS_BITFIELD,
            self.Module.CONNECTOR: int.from_bytes(answer[4:5], "big") & self.CONNECTOR_STATUS_BITFIELD,
        }

    def set_module_diffusion(self, module: Module, activate: bool = True) -> None:
        # TODO  - FINISH
        command: bytes = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module][self.IO.IN]

        raise MinitelNotImplementedException()

    def set_module_ack(self, module: Module, activate: bool = True) -> None:
        # TODO - Try IRL
        command: bytes = self.PRO2
        command += self.COMMAND_CODE_ENABLE if activate else self.COMMAND_CODE_DISABLE
        command += self.IO_CODES[module][self.IO.OUT]

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def get_protocol_status(self) -> dict[str, int]:
        # TODO - Try IRL
        command: bytes = self.PRO1 + self.STATUS_PROTOCOL_REQUEST

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(4)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:2] != self.PRO2 or answer[2:3] != self.STATUS_PROTOCOL_ANSWER:
            raise MinitelInvalidResponseException(
                __name__,
                (self.PRO2 + self.STATUS_PROTOCOL_ANSWER).hex() + '..',
                answer.hex()
            )

        return {
            'D1': int.from_bytes(answer[3:4], 'big') & self.BITFIELD_STATUS_PROTOCOL_D1,
            'D2': int.from_bytes(answer[3:4], 'big') & self.BITFIELD_STATUS_PROTOCOL_D2,
            'A1': int.from_bytes(answer[3:4], 'big') & self.BITFIELD_STATUS_PROTOCOL_A1,
            'A2': int.from_bytes(answer[3:4], 'big') & self.BITFIELD_STATUS_PROTOCOL_A2,
            'PAD_X3_COMPATIBLE': int.from_bytes(answer[4:4], 'big') & self.BITFIELD_STATUS_PROTOCOL_PAD,
        }

    def set_protocol_transparency(self, n: int) -> None:
        # TODO - Try IRL
        if n < 1 or n > 127:
            raise MinitelInvalidArgumentException("Invalid Argument, n should be between 1-127 (got: " + str(n) + ")")

        bit_n: bytes = (n | (1 << 7)).to_bytes(1, 'little')

        command: bytes = self.PRO2 + b'\x66' + bit_n

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(2)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:1] != self.SEP or answer[1:2] != b'\x57':
            raise MinitelInvalidResponseException(
                __name__,
                (self.SEP + b'\x57').hex(),
                answer.hex()
            )

    def get_minitel_info(self) -> tuple[Manufacturer, Model, str]:
        command: bytes = self.PRO1 + self.ENQROM

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(5)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:1] != self.SOH or answer[4:5] != self.EOT:
            raise MinitelInvalidResponseException(
                __name__,
                self.SOH.hex() + '......' + self.EOT.hex(),
                answer.hex()
            )

        self._manufacturer = self.Manufacturer(answer[1:2].decode())
        self._model = self.Model(answer[2:3].decode())
        self._fw_version = answer[3:4].decode()

        return self._manufacturer, self._model, self._fw_version

    def get_visualization_module(self) -> VisualizationModule:
        if self._model is None or self._manufacturer is None or self._fw_version is None:
            self.get_minitel_info()

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
                log(WARNING, 'Unknown Visualization Module - Default is ' + self._vm.name)
        else:
            self._vm = VisualizationModule.VGP2
            log(
                WARNING, 'Not handling models other than %s (got model: %s), Default is %s',
                str(self.Model.MINITEL_1B),
                str(self._model),
                str(self._vm.name)
            )
        return self._vm

    def get_module_operating_mode_status(self) -> tuple[bool, bool, bool, Mode]:
        command: bytes = self.PRO1 + self.OPERATING_STATUS

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(4)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:2] != self.PRO2 or answer[2:3] != self.OPERATING_STATUS_RES:
            raise MinitelInvalidResponseException(
                __name__,
                self.PRO2.hex() + self.OPERATING_STATUS_RES.hex() + '..',
                answer.hex()
            )

        status: int = int.from_bytes(answer[3:4])

        keyboard_caps_lock_bit: int = 1 << 3
        pce_bitfield_bit: int = 1 << 2
        roll_mode_bit: int = 1 << 1
        screen_format_bit: int = 1

        self._keyboard_caps_enabled = status & keyboard_caps_lock_bit == 0
        self._pce_enabled = status & pce_bitfield_bit == 1
        self._roll_mode_enabled = status & roll_mode_bit == 1
        if status & screen_format_bit == 0:
            self._mode = Mode.VIDEOTEX
        else:
            self._mode = Mode.MIXED

        return self._keyboard_caps_enabled, self._pce_enabled, self._roll_mode_enabled, self._mode

    def set_video_mode(self, mode: Mode = Mode.VIDEOTEX) -> None:
        if self._mode == mode:
            log(WARNING, 'Video Mode already set in ' + mode.name + ' mode')

        command: bytes = self.PRO2

        if mode == Mode.MIXED:
            command += self.MIXTE1
        else:
            command += self.MIXTE2

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(2)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if mode == Mode.MIXED and answer[0:2] != self.SEP + b'\x70':
            raise MinitelInvalidResponseException(
                __name__,
                self.SEP.hex() + b'\x70'.hex(),
                answer.hex()
            )
        if mode == Mode.VIDEOTEX and answer[0:2] != self.SEP + b'\x71':
            raise MinitelInvalidResponseException(
                __name__,
                self.SEP.hex() + b'\x71'.hex(),
                answer.hex()
            )

        self._mode = mode

    def get_cursor_position(self) -> tuple[int, int]:
        command: bytes = self.ESC + b'\x61'

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(3)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:1] != self.US:
            raise MinitelInvalidResponseException(
                __name__,
                self.US.hex() + '....',
                answer.hex()
            )

        mask: int = 63
        return int.from_bytes(answer[1:2]) & mask, int.from_bytes(answer[2:3]) & mask

    def show_cursor(self) -> None:
        try:
            self.send(b'\x11')
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def hide_cursor(self) -> None:
        try:
            self.send(b'\x14')
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def connect_modem(self) -> None:
        # TODO - Try IRL
        try:
            self.send(self.PRO1 + b'\x68')
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def disconnect_modem(self) -> None:
        # TODO - Try IRL
        try:
            self.send(self.PRO1 + b'\x67')
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def set_ecp(self, enable: bool = False) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def reverse_modem(self) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def set_connector_baudrate(
            self,
            emission_baudrate = ConnectorBaudrate.BAUDS_1200,
            reception_baudrate = ConnectorBaudrate.BAUDS_1200
    ) -> None:
        if emission_baudrate != reception_baudrate and self._model == self.Model.MINITEL_1B:
            raise MinitelException("Emission and Reception Baudrate must be symmetrical for Minitel 1B Models")

        prog_byte: int = 1 << 6
        prog_byte |= emission_baudrate.value << 3
        prog_byte |= reception_baudrate.value

        command: bytes = self.PRO2 + self.PROG + prog_byte.to_bytes(1, 'little')

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        self._baudrate = emission_baudrate

        if isinstance(self._comm, CommSocket):
            return

        time.sleep(.1)
        try:
            if isinstance(self._comm, CommSerial):
                self._comm.set_baudrate(int(emission_baudrate))
        except CommException as e:
            raise MinitelException("Error while attempting Comm::set_baudrate") from e

    def get_connector_baudrate(self) -> ConnectorBaudrate:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def set_keyboard_mode(self, extended: bool = True, c0: bool = False) -> None:
        self.get_keyboard_mode()

        action: bytes = b''
        answer: bytes = b''
        status: int = 0

        if self._keyboard_extended != extended:
            action = self.START
            if not extended:
                action = self.STOP
            try:
                self.send(
                    self.PRO3 +
                    action +
                    self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] +
                    self.ETEN
                )
            except MinitelException as e:
                raise MinitelRequestException(__name__) from e

            try:
                answer = self.read(5)
            except MinitelException as e:
                raise MinitelResponseException(__name__) from e
            if (
                answer[0:2] != self.PRO3 or
                answer[2:3] != self.REP_KEYBOARD_STATUS or
                answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
            ):
                raise MinitelInvalidResponseException(
                    __name__,
                    (self.PRO3 + self.REP_KEYBOARD_STATUS + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]).hex() + '..',
                    answer.hex()
                )

            c0_bitfield: int = 1 << 2
            extended_bitfield: int = 1

            status = int.from_bytes(answer[4:5])
            self._keyboard_extended = bool(status & extended_bitfield)
            self._keyboard_c0 = bool(status &  c0_bitfield)

        if self._keyboard_c0 != c0:
            action = self.START
            if not c0:
                action = self.STOP
            try:
                self.send(
                    self.PRO3 +
                    action +
                    self.IO_CODES[self.Module.KEYBOARD][self.IO.IN] +
                    self.C0
                )
            except MinitelException as e:
                raise MinitelRequestException(__name__) from e

            try:
                answer = self.read(5)
            except MinitelException as e:
                raise MinitelResponseException(__name__) from e

            if (
                answer[0:2] != self.PRO3 or
                answer[2:3] != self.REP_KEYBOARD_STATUS or
                answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
            ):
                raise MinitelInvalidResponseException(
                    __name__,
                    (self.PRO3 + self.REP_KEYBOARD_STATUS + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]).hex() + '..',
                    answer.hex()
                )

            c0_bitfield = 1 << 2
            extended_bitfield = 1

            status = int.from_bytes(answer[4:5])
            self._keyboard_extended = bool(status & extended_bitfield)
            self._keyboard_c0 = bool(status &  c0_bitfield)

    def get_keyboard_mode(self) -> tuple[bool, bool]:
        try:
            self.send(
                self.PRO2 +
                self.GET_KEYBOARD_STATUS +
                self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
            )
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(5)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e
        if (
            answer[0:2] != self.PRO3 or
            answer[2:3] != self.REP_KEYBOARD_STATUS or
            answer[3:4] != self.IO_CODES[self.Module.KEYBOARD][self.IO.IN]
        ):
            raise MinitelInvalidResponseException(
                    __name__,
                    self.PRO3.hex() + self.REP_KEYBOARD_STATUS.hex() + self.IO_CODES[self.Module.KEYBOARD][self.IO.IN].hex() + '..',
                    answer.hex()
                )

        c0_bitfield: int = 1 << 2
        extended_bitfield: int = 1

        status: int = int.from_bytes(answer[4:5])
        self._keyboard_extended = bool(status & extended_bitfield)
        self._keyboard_c0 = bool(status &  c0_bitfield)

        return self._keyboard_extended, self._keyboard_c0

    def enable_keyboard(self, update_cursor: bool = True) -> None:
        self.unblock_module(self.Module.KEYBOARD)

        if update_cursor:
            self.show_cursor()

    def disable_keyboard(self, update_cursor: bool = True) -> None:
        self.block_module(self.Module.KEYBOARD)

        if update_cursor:
            self.hide_cursor()

    def enable_echo(self) -> None:
        self.unblock_module(self.Module.MODEM)

    def disable_echo(self) -> None:
        self.block_module(self.Module.MODEM)

    def set_key_caps_lock(self, enable: bool) -> int:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def set_screen_page_mode(self) -> None:
        if not self._roll_mode_enabled:
            log(WARNING, 'Scroll Mode already disabled.')
            return

        command: bytes = self.PRO2 + self.STOP + self.ROULEAU

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(4)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:2] !=  self.PRO2:
            raise MinitelInvalidResponseException(
                __name__,
                self.PRO2.hex() + '....',
                answer.hex()
            )

        self._roll_mode_enabled = False

    def set_screen_roll_mode(self) -> None:

        if self._roll_mode_enabled:
            log(WARNING, 'Scroll Mode already enabled.')

        command: bytes = self.PRO2 + self.START + self.ROULEAU

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

        try:
            answer: bytes = self.read(4)
        except MinitelException as e:
            raise MinitelResponseException(__name__) from e

        if answer[0:2] !=  self.PRO2:
            raise MinitelInvalidResponseException(
                __name__,
                self.PRO2.hex() + '....',
                answer.hex()
            )

        self._roll_mode_enabled = True

    class CopyMode(Enum):
        FR = b'\x6a'
        USA = b'\x6b'

    def copy_screen_to_connector(self, mode: CopyMode = CopyMode.FR) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def get_modules_functional_states(self) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def set_text_attributes(self, state: TextAttributesState) -> None:
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        if state.double_height:
            r, _ = self.get_cursor_position()
            if r == 1:
                self.new_line()

        try:
            self.send(self._text_attribute.set_attributes(state = state))
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def reset_text_attributes(self) -> None:
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Text Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        try:
            self.set_text_attributes(
                state = TextAttributesState(
                    color = CharacterColor.WHITE,
                    blinking = False,
                    inverted = False,
                    double_height = False,
                    double_width = False
                )
        )
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def set_zone_attributes(self, state: ZoneAttributesState) -> None:
        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        try:
            self.send(self._zone_attribute.set_attributes(state = state))
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e


    def reset_zone_attributes(self) -> None:

        if self._mode == Mode.MIXED:
            log(
                WARNING,
                'Sending Zone Attributes on Mixed Video Mode will be ignored by the Minitel.'
            )

        try:
            self.set_zone_attributes(
                state = ZoneAttributesState(
                    background = BackgroundColor.BLACK,
                    masking = False,
                    highlight = False
                )
        )
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def masking_fullscreen(self) -> None:
        # TODO - Try IRL
        command: bytes = ESC + b'\x23\x20\x58'

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def unmasking_fullscreen(self) -> None:
        # TODO - Try IRL
        command: bytes = ESC + b'\x23\x20\x5f'

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def invert_text(self) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def invert_background(self) -> None:
        # TODO - Implementation
        raise MinitelNotImplementedException()

    def clear(self) -> None:
        command: bytes = Layout.clear()
        if self._mode == Mode.MIXED:
            command = Layout.set_cursor_position() + Layout.erase_in_display()

        try:
            self.send(command)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def new_line(self) -> None:
        try:
            self.send(Layout.carriage_return() + Layout.move_cursor_down())
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e

    def print(self, text: str) -> None:
        data: bytes = b''
        for c in text:
            data += alphanumerical.ascii_to_alphanumerical(c=c, vm=self._vm)

        try:
            self.send(data)
        except MinitelException as e:
            raise MinitelSendException(data.hex()) from e

    def bind(self, key: KeyboardCode, callback: Callable) -> None:
        if isinstance(key, FilterKeyboardCode):
            self._filter_bindings[key] = callback
            return

        self._bindings[key] = callback

    def clear_bindings(self) -> None:
        for filter_it in self._filter_bindings:
            self._filter_bindings[filter_it] = None

        self._bindings = {}

    def read_keyboard(self, timeout: float | None = None) -> None:
        if self._comm is None:
            raise MinitelNotConnectedException()

        old_timeout: float | None = self._comm.get_timeout()
        self._comm.set_timeout(timeout)

        keyboard_input: bytes = b''
        res: bytes = b''

        callback: Callable | None = None

        try:
            keyboard_input = self.read(1)
        except MinitelException as e:
            raise MinitelReadException(1) from e

        while True:
            if keyboard_input[0:1] not in [b'\x19', b'\x13', b'\x1b']:
                break

            try:
                res = self.read(1)
            except MinitelException as e:
                raise MinitelReadException(1) from e

            keyboard_input += res

            if keyboard_input[1:2] not in [b'\x4b', b'\x5b']:
                break

            try:
                res = self.read(1)
            except MinitelException as e:
                raise MinitelReadException(1) from e

            keyboard_input += res

            if keyboard_input[2:3] not in [b'\x34', b'\x32']:
                break

            try:
                res = self.read(1)
            except MinitelException as e:
                raise MinitelReadException(1) from e

            keyboard_input += res
            break

        self._comm.set_timeout(old_timeout)

        callback_called: bool = False

        if len(keyboard_input):
            print(keyboard_input.hex())

        if len(keyboard_input) == 0:
            callback = self._filter_bindings[FilterKeyboardCode.NO_KEYS]
            if callback is not None:
                callback()
            return

        callback = self._filter_bindings[FilterKeyboardCode.ANY_KEYS]
        if callback is not None:
            callback()
            callback_called = True

        try:
            character = char(VideotexKeyboardCode(keyboard_input))

            if str.isprintable(character):
                callback = self._filter_bindings[FilterKeyboardCode.PRINTABLE_KEYS]
                if callback is not None:
                    callback(character)
                    callback_called = True
        except ValueError:
            log(WARNING, 'data is not a VideotexKeyboardCode')

        if keyboard_input in self._bindings:
            callback = self._bindings[keyboard_input]
            callback()
            callback_called = True

        if callback_called:
            return

        callback = self._filter_bindings[FilterKeyboardCode.OTHER_KEYS]
        if callback is not None:
            callback()

    def beep(self) -> None:
        try:
            self.send(self.BEL)
        except MinitelException as e:
            raise MinitelRequestException(__name__) from e
