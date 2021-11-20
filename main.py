from collections import OrderedDict
from enum import Enum
from typing import Dict, Optional


class Coordinates:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class CardinalPoint(str, Enum):
    North = 'N'
    East = 'E'
    South = 'S'
    West = 'W'


class Plateau:

    def __init__(self, top_right_corner: Coordinates):
        self.max_x = top_right_corner.x
        self.max_y = top_right_corner.y

    def validate(self, position: Coordinates):
        if (position.x < 0 or position.x > self.max_x
                or position.y < 0 or position.y > self.max_y):
            raise ValueError


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

    def change_plateau(
        self,
        new_plateau: Plateau,
        new_position: Optional[Coordinates] = None,
        new_heading: Optional[CardinalPoint] = None
    ) -> None:
        self.plateau = new_plateau

        if new_position is None:
            self.plateau.validate(self.position)
        else:
            self.change_position(new_position)

        if new_heading is not None:
            self.change_heading(new_heading)

    def change_position(
        self,
        new_position: Coordinates,
        new_heading: Optional[CardinalPoint] = None
    ) -> None:
        self.plateau.validate(new_position)

        self.position = new_position

        if new_heading is not None:
            self.change_heading(new_heading)

    def change_heading(
        self,
        new_heading: CardinalPoint
    ) -> None:
        self.heading = new_heading

    def move_forward(self) -> None:
        x = self.position.x
        y = self.position.y

        if self.heading is CardinalPoint.North:
            y += 1
        elif self.heading is CardinalPoint.East:
            x += 1
        elif self.heading is CardinalPoint.South:
            y -= 1
        elif self.heading is CardinalPoint.West:
            x -= 1

        self.change_position(Coordinates(x, y))

    def turn_left(self) -> None:
        if self.heading is CardinalPoint.North:
            heading = CardinalPoint.West
        elif self.heading is CardinalPoint.East:
            heading = CardinalPoint.North
        elif self.heading is CardinalPoint.South:
            heading = CardinalPoint.East
        elif self.heading is CardinalPoint.West:
            heading = CardinalPoint.South

        self.change_heading(heading)

    def turn_right(self) -> None:
        if self.heading is CardinalPoint.North:
            heading = CardinalPoint.East
        elif self.heading is CardinalPoint.East:
            heading = CardinalPoint.South
        elif self.heading is CardinalPoint.South:
            heading = CardinalPoint.West
        elif self.heading is CardinalPoint.West:
            heading = CardinalPoint.North

        self.change_heading(heading)


class MowerController:

    def handle(self, request: str) -> str:
        lines = request.splitlines()
        if (len(lines) < 3
                or (len(lines) - 1) % 2 != 0):
            raise ValueError

        pieces = lines[0].split(' ', 1)
        plateau = Plateau(Coordinates(int(pieces[0]), int(pieces[1])))
        mowers: Dict[Mower, str] = OrderedDict()
        number_of_instructions = 0

        for i, line in enumerate(lines[1:]):
            if i % 2 == 0:
                pieces = line.split(' ', 2)
                mower = Mower(
                    plateau,
                    Coordinates(int(pieces[0]), int(pieces[1])),
                    CardinalPoint(pieces[2])
                )
            else:
                mowers[mower] = line
                number_of_instructions = max(number_of_instructions, len(line))

        for mower, instructions in mowers.items():
            for instruction in instructions:
                if instruction == 'L':
                    mower.turn_left()
                elif instruction == 'R':
                    mower.turn_right()
                elif instruction == 'M':
                    mower.move_forward()
                else:
                    raise ValueError

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
