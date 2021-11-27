# Robot Vacuums

## Introduction

This project is a small experiment for building a CLI application with 
[Typer](https://typer.tiangolo.com/).

The problem to be solved is to clean a surface with some robot vacuum cleaners.
However, these robots are not very intelligent, and need to be instructed.

To simplify the problem, the surface will be rectangular, and divided into a grid.

## How does it works?

I have implemented a command which accepts an input with the size of the surface 
and the position of each vacuum cleaner. For example:

```
5 5
1 2 N
LFLFLFLFF
3 3 E
FFRFFRFRRF
```

The first line is the upper-right coordinates of the surface (the bottom-left 
coordinates are assumed to be 0, 0).

The rest of the input is information relating to the vacuums that have been 
deployed. Each vacuum has two input lines. The first line gives the position 
of the vacuum, and the second line is a series of instructions telling the 
vacuum how to traverse the surface.

The position consists of two integers and a letter separated by spaces, 
corresponding to the X and Y coordinates and the direction of the vacuum.

The instructions are given with three different letters: “L” makes the vacuum 
turn 90 degrees to the left (without moving from its current position), “R” 
produces the same effect but to the right, and “F” commands to move one grid 
point forward (keeping the same direction).

The command outputs the results on several lines. For example, the above input 
produces this output:

```
DONE
1 3 N
5 1 E
```

The first line informs whether all instructions have been executed or not. 
Subsequent lines show the end position of each vacuum.

The instructions are executed in parallel. If an instruction fails, it is retried
until the other vacuums have finished their instructions, or can not move.

## Run command through Docker

To make it easier to run the command, I have prepared a Docker Compose file.
If you have [Docker](https://www.docker.com/products/docker-desktop) installed, 
it is as simple as placing this inside the root folder:

```shell
docker-compose run --rm command
```

The example input will be processed by default, but if you want to process a 
different input, just add it to the end:

```shell
docker-compose run --rm command $'0 5\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF'
```

_Note:_ If you want to run the command on Windows, you will have to make some 
minor adjustments:

```powershell
docker compose run --rm command "0 5`n1 2 N`nLFLFLFLFF`n3 3 E`nFFRFFRFRRF"
```

## Run tests through Docker

To run the test suite, place this command inside the root folder: 

```shell
docker-compose run --rm tests
```

Tests are running with [pytest](https://docs.pytest.org/), so the output will be 
similar to this:

```
============================== test session starts =============================
platform linux -- Python 3.9.9, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/app_user
collected 12 items

tests/test_controllers.py ......                                          [ 50%]
tests/test_main.py ......                                                 [100%]

============================== 12 passed in 0.09s ==============================
```

## The traditional way

If you prefer not to use Docker, you can use a dependency manager to install 
the project dependencies. And Python to run the command.

There are several dependency managers for Python, but I recommend using 
[Pipenv](https://pipenv.pypa.io/en/latest/). This manager automatically creates 
and manages a virtualenv for your projects, as well as adds/removes packages.  

If you do not have Pipenv, but you already have Python and pip, you can easily 
install Pipenv into your home directory:

```shell
pip install --user pipenv
```

Once Pipenv is installed, place this command in the project folder:

```shell
python -m pipenv install --dev
```

_Note:_ The `--dev` option it is only necessary if you want to run the test suite. 
Otherwise, you can omit it.

Then, activate the virtualenv:

```shell
python -m pipenv shell
```

Finally, you will be able to run the command:

```shell
python main.py $'5 5\n1 2 N\nLFLFLFLFF\n3 3 E\nFFRFFRFRRF'
```

And the test suite:

```shell
pytest tests
```