"""
mode.py

This module contains the two visualization  modules on a Minitel, different between models,
for pyminitel library.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

from enum import Enum

class VisualizationModule(Enum):
    """VisualizationModule class.

    Define the two modules which differs between Minitel models, 
    and so changes the alphanumerical tables.

    Args:
        Enum (Enum): Enumerator class.
    """
    VGP2 = 1
    VGP5 = 2
