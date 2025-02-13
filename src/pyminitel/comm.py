import time
import threading

from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from logging import log, ERROR, DEBUG
from queue import Queue, Empty

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from serial import Serial, SerialException, SerialTimeoutException

class CommException(Exception):
    pass

class MinitelDisconnectedException(Exception):
    pass

class Comm(Thread, metaclass=ABCMeta):

    def __init__(self):

        self._out_messages = None
        self._timeout = None

        self.__stop_event = Event()
        self._out_messages = Queue()

        log(level=DEBUG, msg='Event object: id ' + str(id(self.__stop_event)))
        log(level=DEBUG, msg='Queue object: id ' + str(id(self._out_messages)))
        super().__init__()

    def put(self, data: bytes):
        if self.stopped():
            log(ERROR, 'Thread stopped - cannot put message')
            raise CommException

        self._out_messages.put(data)

    def stop(self):
        self.__stop_event.set()

    def stopped(self):
        return self.__stop_event.is_set()

    def get_timeout(self) -> int:
        return self._timeout

    def set_timeout(self, timeout: int = None):
        self._timeout = timeout

    def flush(self):
        try:
            while True:
                self._out_messages.get_nowait()
        except Empty:
            pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read(self, n = int) -> bytes:
        pass

    @abstractmethod
    def run(self):
        pass

class CommSerial(Comm):

    __safe_writing = None

    def __init__(
            self,
            port: str,
            baudrate: int = 1200,
            safe_writing: bool = False,
            timeout: float = None
    ):
        self.__ser = Serial(port=port, baudrate=baudrate, bytesize=7, parity='E', stopbits=1)
        self.__ser.flush()
        self.__safe_writing = safe_writing
        self.set_timeout(timeout=timeout)
        super().__init__()

    def __del__(self):
        if self.__ser:
            self.close()
            del self.__ser

    def read(self, n = int):
        try:
            return self.__ser.read(n)
        except SerialException as e:
            log(ERROR, str(e))
            raise CommException from e

    def open(self):
        try:
            self.__ser.open()
        except SerialException as e :
            log(ERROR, str(e))
            raise CommException from e

    def close(self):
        try:
            self.__ser.close()
        except SerialException as e:
            log(ERROR, str(e))
            raise CommException from e

    def flush(self):
        self.__ser.flush()
        super().flush()

    def set_timeout(self, timeout: int = None):
        self.__ser.timeout = timeout
        super().set_timeout(timeout=timeout)

    def get_baudrate(self):
        return self.__ser.baudrate

    def set_baudrate(self, baudrate: int):
        try:
            while True:
                self._out_messages.get_nowait()
        except Empty:
            pass
        self.close()
        self.__ser.baudrate = baudrate

        self.open()

    def run(self):

        log(level=DEBUG, msg='Started Comm thread: id ' + threading.current_thread().native_id)
        run = True
        while run:
            try:
                queued_data = self._out_messages.get(timeout=1, block=True)
                try:
                    n = self.__ser.write(queued_data)
                    if self.__safe_writing:
                        time.sleep((n * 12 )/ self.__ser.baudrate)
                        while self.__ser.out_waiting:
                            pass
                    self._out_messages.task_done()
                except SerialTimeoutException:
                    log(ERROR, 'Write timeout exceeded, will retry on next loop')
            except Empty:
                if self.stopped():
                    run = False

class CommSocket(Comm):

    __socket = None
    __tcp = None

    def __init__(self, host: int, port: str, timeout: float = None, tcp: socket = None):
        self.set_timeout(timeout=timeout)
        if not tcp:
            self.__socket = socket(AF_INET, SOCK_STREAM)
            self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.__socket.bind((host, port))
            self.open()
        else:
            self.__tcp = tcp
        super().__init__()

    def __del__(self):
        self.close()
        if self.__tcp:
            del self.__tcp
        if self.__socket:
            del self.__socket

    def read(self, n = int):
        try:
            self.__tcp.settimeout(self.get_timeout())
            got = 0
            data_got = b''
            data = b''
            while got < n:
                data_got = self.__tcp.recv(n)
                if data_got is None:
                    raise MinitelDisconnectedException()
                got += len(data_got)
                data += data_got
            self.__tcp.settimeout(None)
            return data
        except TimeoutError:
            # log(level=DEBUG, msg="Timeout caught, returning b''")
            return b''

    def open(self):
        if self.__socket:
            try:
                self.__socket.listen()
                self.__socket.settimeout(self.get_timeout())
                self.__tcp, _ = self.__socket.accept()
            except TimeoutError as e:
                log(ERROR, "Timeout reached")
                raise CommException from e

    def close(self):
        if self.__tcp:
            self.__tcp.close()
        if self.__socket:
            self.__socket.close()

    def set_timeout(self, timeout: int = None):
        super().set_timeout(timeout=timeout)

    def run(self):
        run = True
        while run:
            try:
                queued_data = self._out_messages.get(timeout=1, block=True)
                self.__tcp.sendall(queued_data)
                self._out_messages.task_done()
            except Empty:
                if self.stopped():
                    run = False
            except Exception as e:
                log(ERROR, str(e))
                self.stop()
                run = False
                raise
