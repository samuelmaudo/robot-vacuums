from enum import Enum
from typing import Any

__all__ = ('Coordinates', 'CardinalPoint', 'Instruction')


class Coordinates:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.x} {self.y}>'

    def __str__(self) -> str:
        return f'{self.x} {self.y}'

    def __eq__(self, other: Any) -> bool:
        if other.__class__ != self.__class__:
            raise NotImplementedError

        return other.x == self.x and other.y == self.y


class CardinalPoint(str, Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


class Instruction(str, Enum):
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'F'
