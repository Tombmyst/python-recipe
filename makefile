.PHONY: .venv configure format test

.venv:
	@mkdir -p venv
	python3 -m venv venv

configure: .venv
	@python3 -V
	. venv/bin/activate
	@export PYTHONPATH=$$(pwd):$$PYTHONPATH
	pip3 install -r requirements_dev.txt

format: configure
	@export PYTHONPATH=$$(pwd):$$PYTHONPATH
	isort . --filter-files --profile black
	docformatter --in-place --recursive --blank --make-summary-multi-line recipe/*.py

test: format
	@python3 -V && export PYTHONPATH="$$(pwd):$$PYTHONPATH" && echo "$$PYTHONPATH"
	pylint recipe
	pytest --log-level DEBUG --cov=. --cov-fail-under=98 --cov-report term-missing

deploy: test
	pip3 install --upgrade build
	python3 -m build
