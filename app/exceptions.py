from app.values import CardinalPoint, Coordinates, Instruction

__all__ = (
    'InvalidPlateauCoordinates',
    'InvalidRequest',
    'InvalidVacuumHeading',
    'InvalidVacuumPosition',
    'PositionDoesNotExist',
    'PositionIsNotEmpty',
    'UnknownInstruction',
)


class InvalidPlateauCoordinates(ValueError):

    def __init__(self, coordinates: Coordinates) -> None:
        msg = f'Plateau coordinates are not valid: {coordinates}'
        super().__init__(msg)


class InvalidRequest(ValueError):

    def __init__(self, request: str) -> None:
        super().__init__(f'Request is not well formatted:\n{request}')


class InvalidVacuumHeading(ValueError):

    def __init__(self, heading: CardinalPoint) -> None:
        super().__init__(f'Vacuum heading is not valid: {heading}')


class InvalidVacuumPosition(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Vacuum position is not valid: {position}')


class PositionDoesNotExist(InvalidVacuumPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position outside the plateau boundaries: {position}'
        super(InvalidVacuumPosition, self).__init__(msg)


class PositionIsNotEmpty(InvalidVacuumPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position occupied by another vacuum: {position}'
        super(InvalidVacuumPosition, self).__init__(msg)


class UnknownInstruction(ValueError):

    def __init__(self, instruction: Instruction) -> None:
        super().__init__(f'Instruction is unknown: {instruction}')
