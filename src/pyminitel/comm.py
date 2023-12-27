from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from logging import log, ERROR
from queue import Queue, Empty

from serial import Serial, SerialException
from socket import socket, AF_INET, SOCK_STREAM

import time

class CommException(Exception):
    pass

class Comm(Thread, metaclass=ABCMeta):

    _out_messages = None
    __timeout = None

    def __init__(self):
        self.__stop_event = Event()
        self._out_messages = Queue()
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

    def getTimeout(self) -> int:
        return self.__timeout
    
    def setTimeout(self, timeout: int = None):
        self.__timeout = timeout

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

    __safeWriting = None

    def __init__(self, port: str, baudrate: int = 1200, safe_writing: bool = False):
        self.__ser = Serial(port=port, baudrate=baudrate, bytesize=7, parity='E', stopbits=1)
        self.__ser.flush()
        self.__safeWriting = safe_writing
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
            raise CommException

    def open(self):
        try: 
            self.__ser.open()
        except SerialException as e :
            log(ERROR, str(e))
            raise CommException

    def close(self):
        try: 
            self.__ser.close()
        except SerialException as e:
            log(ERROR, str(e))
            raise CommException

    def flush(self):
        self.__ser.flush()
        super().flush()
    
    def setTimeout(self, timeout: int = None):
        self.__ser.timeout = timeout
        super().setTimeout(timeout=timeout)

    def getBaudrate(self):
        return self.__ser.baudrate

    def setBaudrate(self, baudrate: int):
        try:
            while True:
                self._out_messages.get_nowait()
        except Empty:
            pass
        self.close()
        self.__ser.baudrate = baudrate
        
        self.open()

    def run(self):
        run = True
        while run:
            try:
                queued_data = self._out_messages.get(timeout=1, block=True)
                n = self.__ser.write(queued_data)
                if self.__safeWriting:
                    time.sleep((n * 12 )/ self.__ser.baudrate)
                    while self.__ser.out_waiting:
                        unused = None
                self._out_messages.task_done()
            except Empty:
                if self.stopped():
                    run = False
            except Exception as e:
                log(ERROR, str(e))
                self.stop()
                run = False

class CommSocket(Comm):

    __socket = None
    __tcp = None

    def __init__(self, host: int, port: str, timeout: float = None):
        try:
            self.__socket = socket(AF_INET, SOCK_STREAM)
            self.__socket.bind((host, port))
            self.setTimeout(timeout=timeout)
            self.open()
        except Exception as e:
            log(ERROR, str(e))
            raise CommException
        super().__init__()

    def __del__(self):
        if self.__socket:
            self.close()
            del self.__tcp
            del self.__socket

    def read(self, n = int):
        try:
            return self.__tcp.recv(n)
        except Exception as e:
            log(ERROR, str(e))
            raise CommException

    def open(self):
        try: 
            self.__socket.listen()
            self.__tcp, addr = self.__socket.accept()
        except Exception as e :
            log(ERROR, str(e))
            raise CommException

    def close(self):
        try: 
            self.__tcp.close()
            self.__socket.close()
        except Exception as e:
            log(ERROR, str(e))
            raise CommException

    def flush(self):
        super().flush()
    
    def setTimeout(self, timeout: int = None):
        self.__socket.settimeout(timeout)
        super().setTimeout(timeout=timeout)

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
