from typing import Set

from app.exceptions import (
    InvalidSurfaceCoordinates,
    InvalidVacuumDirection,
    PositionDoesNotExist,
    PositionIsNotEmpty,
    UnknownInstruction
)
from app.values import (
    CardinalPoint,
    Coordinates,
    Instruction
)

__all__ = ('Vacuum', 'Surface')


class Vacuum:

    def __init__(
        self,
        surface: 'Surface',
        position: Coordinates,
        direction: CardinalPoint
    ) -> None:
        surface.validate(position)
        self.surface = surface
        self.position = position
        self.direction = direction

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

        if self.direction is CardinalPoint.NORTH:
            y += 1
        elif self.direction is CardinalPoint.EAST:
            x += 1
        elif self.direction is CardinalPoint.SOUTH:
            y -= 1
        elif self.direction is CardinalPoint.WEST:
            x -= 1
        else:
            raise InvalidVacuumDirection(self.direction)

        new_position = Coordinates(x, y)
        self.surface.validate(new_position)
        self.position = new_position

    def turn_left(self) -> None:
        if self.direction is CardinalPoint.NORTH:
            new_direction = CardinalPoint.WEST
        elif self.direction is CardinalPoint.EAST:
            new_direction = CardinalPoint.NORTH
        elif self.direction is CardinalPoint.SOUTH:
            new_direction = CardinalPoint.EAST
        elif self.direction is CardinalPoint.WEST:
            new_direction = CardinalPoint.SOUTH
        else:
            raise InvalidVacuumDirection(self.direction)

        self.direction = new_direction

    def turn_right(self) -> None:
        if self.direction is CardinalPoint.NORTH:
            new_direction = CardinalPoint.EAST
        elif self.direction is CardinalPoint.EAST:
            new_direction = CardinalPoint.SOUTH
        elif self.direction is CardinalPoint.SOUTH:
            new_direction = CardinalPoint.WEST
        elif self.direction is CardinalPoint.WEST:
            new_direction = CardinalPoint.NORTH
        else:
            raise InvalidVacuumDirection(self.direction)

        self.direction = new_direction


class Surface:

    def __init__(self, top_right_corner: Coordinates) -> None:
        if top_right_corner.x <= 0 or top_right_corner.y <= 0:
            raise InvalidSurfaceCoordinates(top_right_corner)

        self.max_x = top_right_corner.x
        self.max_y = top_right_corner.y
        self.vacuums: Set[Vacuum] = set()

    def add_vacuum(self, position: Coordinates, direction: CardinalPoint) -> Vacuum:
        self.validate(position)
        vacuum = Vacuum(self, position, direction)
        self.vacuums.add(vacuum)
        return vacuum

    def remove_vacuum(self, vacuum: Vacuum) -> None:
        self.vacuums.remove(vacuum)

    def validate(self, position: Coordinates) -> None:
        if (position.x < 0 or position.x > self.max_x
                or position.y < 0 or position.y > self.max_y):
            raise PositionDoesNotExist(position)

        for vacuum in self.vacuums:
            if position == vacuum.position:
                raise PositionIsNotEmpty(position)
