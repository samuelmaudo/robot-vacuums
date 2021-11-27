from app.values import CardinalPoint, Coordinates, Instruction

__all__ = (
    'InvalidRequest',
    'InvalidSurfaceCoordinates',
    'InvalidVacuumDirection',
    'InvalidVacuumPosition',
    'NoFurtherInstructions',
    'PositionDoesNotExist',
    'PositionIsNotEmpty',
    'UnknownInstruction',
)


class InvalidRequest(ValueError):

    def __init__(self, request: str) -> None:
        super().__init__(f'Request is not well formatted:\n{request}')


class InvalidSurfaceCoordinates(ValueError):

    def __init__(self, coordinates: Coordinates) -> None:
        msg = f'Surface coordinates are not valid: {coordinates}'
        super().__init__(msg)


class InvalidVacuumDirection(ValueError):

    def __init__(self, direction: CardinalPoint) -> None:
        super().__init__(f'Vacuum direction is not valid: {direction}')


class InvalidVacuumPosition(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Vacuum position is not valid: {position}')


class NoFurtherInstructions(StopIteration):

    def __init__(self) -> None:
        super().__init__('Vacuum has no further instructions')


class PositionDoesNotExist(InvalidVacuumPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position outside the surface limits: {position}'
        super(InvalidVacuumPosition, self).__init__(msg)


class PositionIsNotEmpty(InvalidVacuumPosition):

    def __init__(self, position: Coordinates) -> None:
        msg = f'Position occupied by another vacuum: {position}'
        super(InvalidVacuumPosition, self).__init__(msg)


class UnknownInstruction(ValueError):

    def __init__(self, instruction: Instruction) -> None:
        super().__init__(f'Instruction is unknown: {instruction}')
