from enum import Enum


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

    def turn_left(self) -> None:
        if self.heading == CardinalPoint.North:
            self.heading = CardinalPoint.West
        elif self.heading == CardinalPoint.East:
            self.heading = CardinalPoint.North
        elif self.heading == CardinalPoint.South:
            self.heading = CardinalPoint.East
        elif self.heading == CardinalPoint.West:
            self.heading = CardinalPoint.South

    def turn_right(self) -> None:
        if self.heading == CardinalPoint.North:
            self.heading = CardinalPoint.East
        elif self.heading == CardinalPoint.East:
            self.heading = CardinalPoint.South
        elif self.heading == CardinalPoint.South:
            self.heading = CardinalPoint.West
        elif self.heading == CardinalPoint.West:
            self.heading = CardinalPoint.North

    def move_forward(self) -> None:
        x = self.position.x
        y = self.position.y

        if self.heading == CardinalPoint.North:
            y += 1
        elif self.heading == CardinalPoint.East:
            x += 1
        elif self.heading == CardinalPoint.South:
            y -= 1
        elif self.heading == CardinalPoint.West:
            x -= 1

        self.change_position(Coordinates(x, y))

    def change_position(self, new_position: Coordinates) -> None:
        self.plateau.validate(new_position)
        self.position = new_position


if __name__ == '__main__':
    plateau = Plateau(Coordinates(5, 5))

    mower_1 = Mower(plateau, Coordinates(1, 2), CardinalPoint.North)
    mower_1.turn_left()
    mower_1.move_forward()
    mower_1.turn_left()
    mower_1.move_forward()
    mower_1.turn_left()
    mower_1.move_forward()
    mower_1.turn_left()
    mower_1.move_forward()
    mower_1.move_forward()

    mower_2 = Mower(plateau, Coordinates(3, 3), CardinalPoint.East)
    mower_2.move_forward()
    mower_2.move_forward()
    mower_2.turn_right()
    mower_2.move_forward()
    mower_2.move_forward()
    mower_2.turn_right()
    mower_2.move_forward()
    mower_2.turn_right()
    mower_2.turn_right()
    mower_2.move_forward()

    assert f'{mower_1.position.x} {mower_1.position.y} {mower_1.heading.value}' == '1 3 N'
    assert f'{mower_2.position.x} {mower_2.position.y} {mower_2.heading.value}' == '5 1 E'

    print('OK')
