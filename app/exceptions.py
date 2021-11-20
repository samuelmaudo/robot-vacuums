from app.values import Coordinates

__all__ = (
    'InvalidCardinalPoint',
    'InvalidRequest',
    'PositionDoesNotExist',
    'PositionIsNotEmpty',
    'UnknownInstruction',
)


class InvalidCardinalPoint(ValueError):

    def __init__(self, instruction: str) -> None:
        super().__init__(f'Cardinal point is not valid: {instruction}')


class InvalidRequest(ValueError):

    def __init__(self, request: str) -> None:
        super().__init__(f'Request is not well formatted:\n{request}')


class PositionDoesNotExist(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Position outside the plateau boundaries: {position}')


class PositionIsNotEmpty(ValueError):

    def __init__(self, position: Coordinates) -> None:
        super().__init__(f'Position occupied by another mower: {position}')


class UnknownInstruction(ValueError):

    def __init__(self, instruction: str) -> None:
        super().__init__(f'Instruction is unknown: {instruction}')
