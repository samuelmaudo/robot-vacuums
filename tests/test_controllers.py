import pytest

from app.controllers import VacuumController
from app.exceptions import (
    InvalidRequest,
    InvalidSurfaceCoordinates,
    InvalidVacuumPosition
)


@pytest.fixture
def controller():
    return VacuumController()


@pytest.fixture
def valid_requests():
    return [
        ('5 5\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'DONE\n1 3 N\n5 1 E'),
        ('5 5\n1 3 N\nRFFF\n2 3 S\nRFFF',
         'FAILED\n1 3 E\n2 3 W'),
        ('5 5\n1 3 N\nRFFF\n2 3 S\nLLFF',
         'DONE\n4 3 E\n2 5 N'),
        ('5 5\n1 3 N\nRFFFFF\n2 3 S\nLLFFFF',
         'FAILED\n5 3 E\n2 5 N'),
    ]


@pytest.fixture
def invalid_requests():
    return [
        ('abc',
         InvalidRequest,
         'Request is not well formatted:\nabc'),
        ('5 5\n1 2 N\nLFLFLFLFF\n3 3 E',
         InvalidRequest,
         'Request is not well formatted:\n5 5\n1 2 N\nLFLFLFLFF\n3 3 E'),
    ]


@pytest.fixture
def invalid_surface_coordinates():
    return [
        ('0 5\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidSurfaceCoordinates,
         'Surface coordinates are not valid: 0 5'),
        ('5 -1\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidSurfaceCoordinates,
         'Surface coordinates are not valid: 5 -1'),
    ]


@pytest.fixture
def invalid_vacuum_coordinates():
    return [
        ('5 5\n-1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidVacuumPosition,
         'Position outside the surface limits: -1 2'),
        ('5 5\n1 -2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidVacuumPosition,
         'Position outside the surface limits: 1 -2'),
        ('5 5\n10 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidVacuumPosition,
         'Position outside the surface limits: 10 2'),
        ('5 5\n1 20 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         InvalidVacuumPosition,
         'Position outside the surface limits: 1 20'),
        ('5 5\n1 2 N\nLFLFLFLFF\n1 2 E\nFFRFFRFRRF',
         InvalidVacuumPosition,
         'Position occupied by another vacuum: 1 2'),
    ]


@pytest.fixture
def invalid_cardinal_points():
    return [
        ('5 5\n1 2 Q\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         ValueError,
         "'Q' is not a valid CardinalPoint"),
        ('5 5\n1 2 e\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         ValueError,
         "'e' is not a valid CardinalPoint"),
    ]


@pytest.fixture
def invalid_instructions():
    return [
        ('5 5\n1 2 N\nQRQRQRQRR\n3 3 E\nFFRFFRFRRF',
         ValueError,
         "'Q' is not a valid Instruction"),
        ('5 5\n1 2 N\nlflflflff\n3 3 E\nFFRFFRFRRF',
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


def test_invalid_surface_coordinates(controller, invalid_surface_coordinates):
    for request, exception, message in invalid_surface_coordinates:
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
