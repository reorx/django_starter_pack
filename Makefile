.PHONY: test build

run-dev:
	python manage.py runserver --nothreading 8000

clean:
	rm -rf build dist *.egg-info

test:
	PYTHONPATH=. pytest -v test/

build:
	python setup.py build
