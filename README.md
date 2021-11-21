# Robotic Mowers

## Run command through Docker

Running the command as a containerized app is as easy as placing this inside the
root folder:

```commandline
docker-compose run --rm command
```

The provided input test case will be processed by default, resulting in this 
output: 

```
1 3 N
5 1 E
```

If you want to process a different input, just add it to the end:

```shell
docker-compose run --rm command $'0 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM'
```

For example, the previous input will result in this output:

```
Plateau coordinates are not valid: 0 5
```

_Note:_ If you want to run the command on Windows, you will have to make some 
minor adjustments:

```powershell
docker compose run --rm command "0 5`n1 2 N`nLMLMLMLMM`n3 3 E`nMMRMMRMRRM"
```

## Run tests through Docker

To run the test suite, place this command inside the root folder: 

```shell
docker-compose run --rm tests
```

Tests are running with **pytest**, so the output will be similar to this:

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

```commandline
pip install --user pipenv
```

Once Pipenv is installed, place this command in the project folder:

```commandline
python -m pipenv install --dev
```

_Note:_ The `--dev` option it is only necessary if you want to run the test suite. 
Otherwise, you can omit it.

Then, activate the virtualenv:

```commandline
python -m pipenv shell
```

Finally, you will be able to run the command:

```commandline
python main.py $'5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM'
```

And the test suite:

```commandline
pytest tests
```