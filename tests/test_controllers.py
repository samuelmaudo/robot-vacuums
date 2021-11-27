import pytest

from app.controllers import VacuumController
from app.exceptions import (
    InvalidPlateauCoordinates,
    InvalidRequest,
    InvalidVacuumPosition
)


@pytest.fixture
def controller():
    return VacuumController()


@pytest.fixture
def valid_requests():
    return [
        ('5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         '1 3 N\n5 1 E'),
    ]


@pytest.fixture
def invalid_requests():
    return [
        ('abc',
         InvalidRequest,
         'Request is not well formatted:\nabc'),
        ('5 5\n1 2 N\nLMLMLMLMM\n3 3 E',
         InvalidRequest,
         'Request is not well formatted:\n5 5\n1 2 N\nLMLMLMLMM\n3 3 E'),
    ]


@pytest.fixture
def invalid_plateau_coordinates():
    return [
        ('0 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidPlateauCoordinates,
         'Plateau coordinates are not valid: 0 5'),
        ('5 -1\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidPlateauCoordinates,
         'Plateau coordinates are not valid: 5 -1'),
    ]


@pytest.fixture
def invalid_vacuum_coordinates():
    return [
        ('5 5\n-1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidVacuumPosition,
         'Position outside the plateau boundaries: -1 2'),
        ('5 5\n1 -2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidVacuumPosition,
         'Position outside the plateau boundaries: 1 -2'),
        ('5 5\n10 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidVacuumPosition,
         'Position outside the plateau boundaries: 10 2'),
        ('5 5\n1 20 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         InvalidVacuumPosition,
         'Position outside the plateau boundaries: 1 20'),
        ('5 5\n1 2 N\nLMLMLMLMM\n1 2 E\nMMRMMRMRRM',
         InvalidVacuumPosition,
         'Position occupied by another vacuum: 1 2'),
    ]


@pytest.fixture
def invalid_cardinal_points():
    return [
        ('5 5\n1 2 Q\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         ValueError,
         "'Q' is not a valid CardinalPoint"),
        ('5 5\n1 2 e\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         ValueError,
         "'e' is not a valid CardinalPoint"),
    ]


@pytest.fixture
def invalid_instructions():
    return [
        ('5 5\n1 2 N\nQRQRQRQRR\n3 3 E\nMMRMMRMRRM',
         ValueError,
         "'Q' is not a valid Instruction"),
        ('5 5\n1 2 N\nlmlmlmlmm\n3 3 E\nMMRMMRMRRM',
         ValueError,
         "'l' is not a valid Instruction"),
    ]


def test_valid_requests(controller, valid_requests):
    for request, expected_response in valid_requests:
        response = controller.handle(request)
        assert expected_response == response


def test_invalid_requests(controller, invalid_requests):
    for request, exception, message in invalid_requests:
        with pytest.raises(exception, match=message):
            controller.handle(request)


def test_invalid_plateau_coordinates(controller, invalid_plateau_coordinates):
    for request, exception, message in invalid_plateau_coordinates:
        with pytest.raises(exception, match=message):
            controller.handle(request)


def test_invalid_vacuum_coordinates(controller, invalid_vacuum_coordinates):
    for request, exception, message in invalid_vacuum_coordinates:
        with pytest.raises(exception, match=message):
            controller.handle(request)


def test_invalid_cardinal_points(controller, invalid_cardinal_points):
    for request, exception, message in invalid_cardinal_points:
        with pytest.raises(exception, match=message):
            controller.handle(request)


def test_invalid_instructions(controller, invalid_instructions):
    for request, exception, message in invalid_instructions:
        with pytest.raises(exception, match=message):
            controller.handle(request)
