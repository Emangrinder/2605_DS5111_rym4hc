default:
	@cat makefile

lint:
	pylint week2/clean_ids.py week4/extract_transcripts.py

test:
	make lint && pytest -vv tests

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update:  env
	. env/bin/activate; pip install -r requirements.txt
