path = src spec
files = `find $(path) -name '*.py'`

test:
	mamba spec --format=documentation --enable-coverage

format:
	- add-trailing-comma $(files)
	- pyformat -i $(files)
	- isort -rc $(path)

lint:
	flake8 $(path)

run:
	pipenv run python -m src.main
