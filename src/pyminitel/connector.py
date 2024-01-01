from pyminitel.minitel import Minitel, MinitelException

from serial import Serial, SerialException
from logging import log, ERROR
import glob, sys

def get_connected_serial_minitel(port: str = None, ip: str = None)-> Minitel:
    minitel = None
    ports = []

    if port is None:
        ports = serial_ports()
    else:
        ports.append(port)

    for port in ports:
        for bauds in [Minitel.ConnectorBaudrate.BAUDS_1200, Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_300]:
            try:
                minitel = Minitel(port=port, baudrate=bauds, ip=ip)
                return minitel;
            except MinitelException:
                log(ERROR, 'Minitel not connected on ' + str(bauds.to_int()) + ' bauds.')

    if minitel is None:
        log(ERROR, 'Unable to find appropriate baudrate for the minitel, exiting...')
        return None

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result