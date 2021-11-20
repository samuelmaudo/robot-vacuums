from app.values import CardinalPoint, Coordinates, Instruction

__all__ = (
    'InvalidMowerHeading',
    'InvalidMowerPosition',
    'InvalidPlateauCoordinates',
    'InvalidRequest',
    'PositionDoesNotExist',
    'PositionIsNotEmpty',
    'UnknownInstruction',
)


class InvalidMowerHeading(ValueError):

    def __init__(self, heading: CardinalPoint) -> None:
        super().__init__(f'Mower heading is not valid: {heading}')


class InvalidMowerPosition(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Mower position is not valid: {position}')


class InvalidPlateauCoordinates(ValueError):

    def __init__(self, coordinates: Coordinates) -> None:
        msg = f'Plateau coordinates are not valid: {coordinates}'
        super().__init__(msg)


class InvalidRequest(ValueError):

    def __init__(self, request: str) -> None:
        super().__init__(f'Request is not well formatted:\n{request}')


class PositionDoesNotExist(InvalidMowerPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position outside the plateau boundaries: {position}'
        super(InvalidMowerPosition, self).__init__(msg)


class PositionIsNotEmpty(InvalidMowerPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position occupied by another mower: {position}'
        super(InvalidMowerPosition, self).__init__(msg)


class UnknownInstruction(ValueError):

    def __init__(self, instruction: Instruction) -> None:
        super().__init__(f'Instruction is unknown: {instruction}')
