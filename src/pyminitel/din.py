from serial import Serial, SerialException
from logging import *
from queue import Queue, Empty
import time, threading

class DIN(threading.Thread):

    __ser = None
    __safeWriting = None

    __out_messages = None

    def __init__(self, port: str, baudrate: int = 1200, safe_writing: bool = False) -> None:
        super(DIN, self).__init__()
        self._stop_event = threading.Event()
        self.__ser = Serial(port=port, baudrate=baudrate, bytesize=7, parity='E', stopbits=1)
        self.__ser.flush()

        self.__out_messages = Queue()

        self.__safeWriting = safe_writing

    def __del__(self):
        if self.__ser:
            self.__ser.close()
            del self.__ser

    def read(self, n = int):
        try:
            return self.__ser.read(n)
        except SerialException as e:
            log(ERROR, e)
            raise SerialException

    def put(self, data: bytes):
        if self.stopped():
            log(ERROR, 'Thread stopped - cannot put message')
            raise SerialException
        
        self.__out_messages.put(data)

    def open(self):
        try: 
            self.__ser.open()
        except SerialException as e :
            log(ERROR, e)

    def close(self):
        try: 
            self.__ser.close()
        except SerialException as e:
            log(ERROR, e)

    def flush(self):
        self.__ser.flush()
        try:
            while True:
                self.__out_messages.get_nowait()
        except Empty:
            pass

    def getTimeout(self) -> int:
        return self.__ser.timeout
    
    def setTimeout(self, timeout: int = None):
        self.__ser.timeout = timeout

    def getBaudrate(self):
        return self.__ser.baudrate

    def setBaudrate(self, baudrate: int):
        self.close()
        self.__ser.baudrate = baudrate
        try:
            while True:
                self.__out_messages.get_nowait()
        except Empty:
            pass
        self.open()

    def run(self):
        run = True
        while run:
            try:
                queued_data = self.__out_messages.get(timeout=1, block=True)
                n = self.__ser.write(queued_data)
                log(DEBUG, (n * 12 )/ self.__ser.baudrate)
                if self.__safeWriting:
                    time.sleep((n * 12 )/ self.__ser.baudrate)
                    while self.__ser.out_waiting:
                        unused = None
                self.__out_messages.task_done()
            except Empty:
                log(DEBUG, 'Empty queue')
                if self.stopped():
                    run = False
            except Exception as e:
                log(ERROR, e)
                self.stop()
                run = False

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
