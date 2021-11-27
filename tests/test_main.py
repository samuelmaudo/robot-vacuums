import pytest
from typer.testing import CliRunner

import main


@pytest.fixture
def runner():
    return CliRunner()


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
         'Request is not well formatted:\nabc'),
        ('5 5\n1 2 N\nLMLMLMLMM\n3 3 E',
         'Request is not well formatted:\n5 5\n1 2 N\nLMLMLMLMM\n3 3 E'),
    ]


@pytest.fixture
def invalid_plateau_coordinates():
    return [
        ('0 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Plateau coordinates are not valid: 0 5'),
        ('5 -1\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Plateau coordinates are not valid: 5 -1'),
    ]


@pytest.fixture
def invalid_vacuum_coordinates():
    return [
        ('5 5\n-1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Position outside the plateau boundaries: -1 2'),
        ('5 5\n1 -2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Position outside the plateau boundaries: 1 -2'),
        ('5 5\n10 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Position outside the plateau boundaries: 10 2'),
        ('5 5\n1 20 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         'Position outside the plateau boundaries: 1 20'),
        ('5 5\n1 2 N\nLMLMLMLMM\n1 2 E\nMMRMMRMRRM',
         'Position occupied by another vacuum: 1 2'),
    ]


@pytest.fixture
def invalid_cardinal_points():
    return [
        ('5 5\n1 2 Q\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         "'Q' is not a valid CardinalPoint"),
        ('5 5\n1 2 e\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM',
         "'e' is not a valid CardinalPoint"),
    ]


@pytest.fixture
def invalid_instructions():
    return [
        ('5 5\n1 2 N\nQRQRQRQRR\n3 3 E\nMMRMMRMRRM',
         "'Q' is not a valid Instruction"),
        ('5 5\n1 2 N\nlmlmlmlmm\n3 3 E\nMMRMMRMRRM',
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


def test_invalid_plateau_coordinates(runner, invalid_plateau_coordinates):
    for request, response in invalid_plateau_coordinates:
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
