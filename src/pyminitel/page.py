"""
page.py

This module contains the base to implement your own service's page,
see pyminitel/src/examples/ for usages.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

import threading

from pyminitel.minitel import Minitel

class Page(threading.Thread):
    """Page class.

    An abstract class being a Thread, so one Page can be called from another one for a full service.

    Args:
        threading (_type_): Allow to handle the current page in a subprocess.
    """

    def __init__(self, minitel: Minitel) -> None:
        """Page constructor.

        Args:
            minitel (Minitel): Connected minitel client to serve.
        """

        super().__init__()

        self._stop_event = threading.Event()
        self.minitel = minitel

    def stop(self) -> None:
        """Stops the page.
        """

        self._stop_event.set()

    def stopped(self) -> bool:
        """Check if page has been stopped.
        """

        return self._stop_event.is_set()
