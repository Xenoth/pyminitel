"""
mode.py

This module contains the two display mode of a Minitel and their resolutions for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

from enum import Enum
from typing import Final

class Mode(Enum):
    """Mode class.

    Define the 2 screen's mode of the Minitel, Videotex and Mixed.

    Args:
        Enum (Enum): Enumerator.
    """

    VIDEOTEX = 1
    MIXED = 2

RESOLUTION: Final[dict[Mode, list[int]]] = {
        Mode.VIDEOTEX: [
            25,
            40,
        ],
        Mode.MIXED: [
            25,
            80,
        ]
    }
