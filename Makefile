.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with pylint"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -rf .tox/

lint:
	pip install logilab-common==0.63.0
	pip install pylint
	python setup.py pylint > pylint.log || exit 0
	cat pylint.log

test:
	pip install nose
	pip install nose-testconfig
	pip install nosexcover
	python setup.py nosetests || exit 0

test-all:
	pip install tox
	tox || exit 0

docs:
	pip install sphinx
	python setup.py install
	rm -f docs/dxskytap.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ dxskytap
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: clean
	pip install wheel
	pip install twine
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload -r pypi-local dist/*

dist: clean
	pip install wheel
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
