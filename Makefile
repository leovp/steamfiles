help:
	@echo "test - run tests quickly with the default Python"
	#@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

coverage:
	coverage run --branch --source=steamfiles -m pytest
	coverage report -m
	coverage html

test:
	py.test

test-all:
	tox
