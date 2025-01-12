from pyminitel.minitel import Minitel

import threading

class Page(threading.Thread):

    def __init__(self, minitel = Minitel) -> None:
        super(Page, self).__init__()
        
        self._stop_event = threading.Event()
        self.minitel = minitel

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()