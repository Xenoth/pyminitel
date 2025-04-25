"""
connector.py

This module contains an utility function that returns an instance of a Minitel,
using serial or tcp communication.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import glob
import sys

from typing import Optional
from logging import log, DEBUG

from socket import socket
from serial import Serial, SerialException

from pyminitel.minitel import Minitel, MinitelException

class ConnectorException(Exception):
    pass

class MinitelNotFoundException(ConnectorException):
    pass

def get_connected_socket_minitel(
    host: str,
    port: int,
    tcp: Optional[socket] = None,
    timeout: Optional[float] = None
) -> Minitel:

    try:
        minitel: Minitel = Minitel()
        minitel.connect_socket(host=host, port=port, tcp=tcp, timeout=timeout)
        minitel.get_minitel_info()
        minitel.get_visualization_module()
        minitel.get_module_operating_mode_status()
        minitel.get_keyboard_mode()

        return minitel

    except MinitelException as e:
        raise MinitelNotFoundException from e

def get_connected_serial_minitel(
    port: Optional[str] = None,
    timeout: Optional[float] = None
) -> Minitel:

    ports = []

    if port is None:
        ports = serial_ports()
    else:
        ports.append(port)

    for current_port in ports:
        for bauds in [
            Minitel.ConnectorBaudrate.BAUDS_1200,
            Minitel.ConnectorBaudrate.BAUDS_4800,
            Minitel.ConnectorBaudrate.BAUDS_300
        ]:
            try:
                minitel: Minitel = Minitel()
                minitel.connect_serial(port=current_port, baudrate=bauds, timeout=timeout)
                minitel.get_minitel_info()
                minitel.get_visualization_module()
                minitel.get_module_operating_mode_status()
                minitel.get_keyboard_mode()

                return minitel

            except MinitelException as e:
                log(DEBUG, str(e))

    raise MinitelNotFoundException()

def serial_ports() -> list[str]:
    """Lists serial port names.

    Raises:
        EnvironmentError: On unsupported or unknown platforms.

    Returns:
        list: A list of the serial ports available on the system.
    """
    if sys.platform.startswith('win'):
        ports = [f'COM{i + 1}' for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result: list[str] = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result
