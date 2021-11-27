import pytest
from typer.testing import CliRunner

import main


@pytest.fixture
def runner():
    return CliRunner()


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
         'Request is not well formatted:\nabc'),
        ('5 5\n1 2 N\nLFLFLFLFF\n3 3 E',
         'Request is not well formatted:\n5 5\n1 2 N\nLFLFLFLFF\n3 3 E'),
    ]


@pytest.fixture
def invalid_surface_coordinates():
    return [
        ('0 5\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Surface coordinates are not valid: 0 5'),
        ('5 -1\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Surface coordinates are not valid: 5 -1'),
    ]


@pytest.fixture
def invalid_vacuum_coordinates():
    return [
        ('5 5\n-1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Position outside the surface limits: -1 2'),
        ('5 5\n1 -2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Position outside the surface limits: 1 -2'),
        ('5 5\n10 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Position outside the surface limits: 10 2'),
        ('5 5\n1 20 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         'Position outside the surface limits: 1 20'),
        ('5 5\n1 2 N\nLFLFLFLFF\n1 2 E\nFFRFFRFRRF',
         'Position occupied by another vacuum: 1 2'),
    ]


@pytest.fixture
def invalid_cardinal_points():
    return [
        ('5 5\n1 2 Q\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         "'Q' is not a valid CardinalPoint"),
        ('5 5\n1 2 e\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF',
         "'e' is not a valid CardinalPoint"),
    ]


@pytest.fixture
def invalid_instructions():
    return [
        ('5 5\n1 2 N\nQRQRQRQRR\n3 3 E\nFFRFFRFRRF',
         "'Q' is not a valid Instruction"),
        ('5 5\n1 2 N\nlflflflff\n3 3 E\nFFRFFRFRRF',
         "'l' is not a valid Instruction"),
    ]


def test_valid_requests(runner, valid_requests):
    for request, response in valid_requests:
        result = runner.invoke(main.app, [request])
        assert 0 == result.exit_code
        assert f'{response}\n' == result.stdout


def test_invalid_requests(runner, invalid_requests):
    for request, response in invalid_requests:
        result = runner.invoke(main.app, [request])
        assert 1 == result.exit_code
        assert f'{response}\n' == result.stdout


def test_invalid_surface_coordinates(runner, invalid_surface_coordinates):
    for request, response in invalid_surface_coordinates:
        result = runner.invoke(main.app, [request])
        assert 1 == result.exit_code
        assert f'{response}\n' == result.stdout


def test_invalid_vacuum_coordinates(runner, invalid_vacuum_coordinates):
    for request, response in invalid_vacuum_coordinates:
        result = runner.invoke(main.app, [request])
        assert 1 == result.exit_code
        assert f'{response}\n' == result.stdout


def test_invalid_cardinal_points(runner, invalid_cardinal_points):
    for request, response in invalid_cardinal_points:
        result = runner.invoke(main.app, [request])
        assert 1 == result.exit_code
        assert f'{response}\n' == result.stdout


def test_invalid_instructions(runner, invalid_instructions):
    for request, response in invalid_instructions:
        result = runner.invoke(main.app, [request])
        assert 1 == result.exit_code
        assert f'{response}\n' == result.stdout
