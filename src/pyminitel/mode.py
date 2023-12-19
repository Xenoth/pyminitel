from enum import Enum

class Mode(Enum):
    VIDEOTEX = 1
    MIXED = 2

RESOLUTION = {
        Mode.VIDEOTEX: [
            25,
            40,
        ],
        Mode.MIXED: [
            25,
            80,
        ]
    }