from typing import Set

from app.exceptions import (
    InvalidMowerHeading,
    InvalidPlateauCoordinates,
    PositionDoesNotExist,
    PositionIsNotEmpty,
    UnknownInstruction
)
from app.values import (
    CardinalPoint,
    Coordinates,
    Instruction
)

__all__ = ('Mower', 'Plateau')


class Mower:

    def __init__(
        self,
        plateau: 'Plateau',
        position: Coordinates,
        heading: CardinalPoint
    ) -> None:
        plateau.validate(position)
        self.plateau = plateau
        self.position = position
        self.heading = heading

    def process(self, instruction: Instruction) -> None:
        if instruction is Instruction.TURN_LEFT:
            self.turn_left()
        elif instruction is Instruction.TURN_RIGHT:
            self.turn_right()
        elif instruction is Instruction.MOVE_FORWARD:
            self.move_forward()
        else:
            raise UnknownInstruction(instruction)

    def move_forward(self) -> None:
        x = self.position.x
        y = self.position.y

        if self.heading is CardinalPoint.NORTH:
            y += 1
        elif self.heading is CardinalPoint.EAST:
            x += 1
        elif self.heading is CardinalPoint.SOUTH:
            y -= 1
        elif self.heading is CardinalPoint.WEST:
            x -= 1
        else:
            raise InvalidMowerHeading(self.heading)

        new_position = Coordinates(x, y)
        self.plateau.validate(new_position)
        self.position = new_position

    def turn_left(self) -> None:
        if self.heading is CardinalPoint.NORTH:
            new_heading = CardinalPoint.WEST
        elif self.heading is CardinalPoint.EAST:
            new_heading = CardinalPoint.NORTH
        elif self.heading is CardinalPoint.SOUTH:
            new_heading = CardinalPoint.EAST
        elif self.heading is CardinalPoint.WEST:
            new_heading = CardinalPoint.SOUTH
        else:
            raise InvalidMowerHeading(self.heading)

        self.heading = new_heading

    def turn_right(self) -> None:
        if self.heading is CardinalPoint.NORTH:
            new_heading = CardinalPoint.EAST
        elif self.heading is CardinalPoint.EAST:
            new_heading = CardinalPoint.SOUTH
        elif self.heading is CardinalPoint.SOUTH:
            new_heading = CardinalPoint.WEST
        elif self.heading is CardinalPoint.WEST:
            new_heading = CardinalPoint.NORTH
        else:
            raise InvalidMowerHeading(self.heading)

        self.heading = new_heading


class Plateau:

    def __init__(self, top_right_corner: Coordinates) -> None:
        if top_right_corner.x <= 0 or top_right_corner.y <= 0:
            raise InvalidPlateauCoordinates(top_right_corner)

        self.max_x = top_right_corner.x
        self.max_y = top_right_corner.y
        self.mowers: Set[Mower] = set()

    def add_mower(self, position: Coordinates, heading: CardinalPoint) -> Mower:
        self.validate(position)
        mower = Mower(self, position, heading)
        self.mowers.add(mower)
        return mower

    def remove_mower(self, mower: Mower) -> None:
        self.mowers.remove(mower)

    def validate(self, position: Coordinates) -> None:
        if (position.x < 0 or position.x > self.max_x
                or position.y < 0 or position.y > self.max_y):
            raise PositionDoesNotExist(position)

        for mower in self.mowers:
            if position == mower.position:
                raise PositionIsNotEmpty(position)