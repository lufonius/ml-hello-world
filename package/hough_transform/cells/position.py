from enum import Enum

class Position(Enum):
    TOP_LEFT = 0,
    TOP = 1,
    TOP_RIGHT = 2,
    RIGHT = 3,
    BOTTOM_RIGHT = 4,
    BOTTOM = 5,
    BOTTOM_LEFT = 6,
    LEFT = 7,
    MIDDLE = 8

POSITION = {
    Position.TOP_LEFT: (-1, 1),
    Position.TOP: (0, 1),
    Position.TOP_RIGHT: (1, 1),
    Position.RIGHT: (1,0),
    Position.BOTTOM_RIGHT: (1, -1),
    Position.BOTTOM: (0, -1),
    Position.BOTTOM_LEFT: (-1, -1),
    Position.LEFT: (-1, 0)
}

