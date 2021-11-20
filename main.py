from collections import OrderedDict
from enum import Enum
from typing import Dict, List, Set


class Coordinates:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class PositionDoesNotExist(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Position outside the plateau boundaries: {position}')


class PositionIsNotEmpty(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Position occupied by another mower: {position}')


class CardinalPoint(str, Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


class InvalidCardinalPoint(ValueError):

    def __init__(self, instruction: str) -> None:
        super().__init__(f'Cardinal point is not valid: {instruction}')


class Instruction(str, Enum):
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'M'


class UnknownInstruction(ValueError):

    def __init__(self, instruction: str) -> None:
        super().__init__(f'Instruction is unknown: {instruction}')


class Plateau:

    def __init__(self, top_right_corner: Coordinates) -> None:
        self.max_x = top_right_corner.x
        self.max_y = top_right_corner.y
        self.mowers: Set['Mower'] = set()

    def add_mower(self, position: Coordinates, heading: CardinalPoint) -> 'Mower':
        self.validate(position)
        mower = Mower(self, position, heading)
        self.mowers.add(mower)
        return mower

    def remove_mower(self, mower: 'Mower') -> None:
        self.mowers.remove(mower)

    def validate(self, position: Coordinates) -> None:
        if (position.x < 0 or position.x > self.max_x
                or position.y < 0 or position.y > self.max_y):
            raise PositionDoesNotExist(position)

        for mower in self.mowers:
            if position == mower.position:
                raise PositionIsNotEmpty(position)


class Mower:

    def __init__(
        self,
        plateau: Plateau,
        position: Coordinates,
        heading: CardinalPoint
    ) -> None:
        plateau.validate(position)
        self.plateau = plateau
        self.position = position
        self.heading = heading

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
            raise InvalidCardinalPoint(self.heading)

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
            raise InvalidCardinalPoint(self.heading)

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
            raise InvalidCardinalPoint(self.heading)

        self.heading = new_heading


class InvalidRequest(ValueError):

    def __init__(self, request: str) -> None:
        super().__init__(f'Request is not well formatted:\n\n{request}')


class MowerController:

    def handle(self, request: str) -> str:
        lines = request.splitlines()
        if (len(lines) < 3
                or (len(lines) - 1) % 2 != 0):
            raise InvalidRequest(request)

        pieces = lines[0].split(' ', 1)
        plateau = Plateau(Coordinates(int(pieces[0]), int(pieces[1])))
        mowers: Dict[Mower, List[Instruction]] = OrderedDict()

        for i, line in enumerate(lines[1:]):
            if i % 2 == 0:
                pieces = line.split(' ', 2)
                mower = plateau.add_mower(
                    Coordinates(int(pieces[0]), int(pieces[1])),
                    CardinalPoint(pieces[2])
                )
            else:
                instructions = [Instruction(letter) for letter in line]
                mowers[mower] = instructions

        for mower, instructions in mowers.items():
            for instruction in instructions:
                if instruction is Instruction.TURN_LEFT:
                    mower.turn_left()
                elif instruction is Instruction.TURN_RIGHT:
                    mower.turn_right()
                elif instruction is Instruction.MOVE_FORWARD:
                    mower.move_forward()
                else:
                    raise UnknownInstruction(instruction)

        response = ''
        for mower in mowers.keys():
            response += f'{mower.position.x} {mower.position.y} {mower.heading.value}\n'

        return response.strip()


if __name__ == '__main__':
    request = '5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM'
    expected_response = '1 3 N\n5 1 E'

    controller = MowerController()
    response = controller.handle(request)

    assert response == expected_response

    print('OK')
