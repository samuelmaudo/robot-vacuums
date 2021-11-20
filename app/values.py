from enum import Enum

__all__ = ('Coordinates', 'CardinalPoint', 'Instruction')


class Coordinates:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class CardinalPoint(str, Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


class Instruction(str, Enum):
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'M'
