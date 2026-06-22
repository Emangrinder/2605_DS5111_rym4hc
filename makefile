default:
	@cat makefile

lint:
	pylint week2/clean_ids.py && pylint week4/extract_transcripts.py && pylint week5/enrich_transcripts.py

test:
	make lint && pytest -vv tests

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update:  env
	. env/bin/activate; pip install -r requirements.txt

test_enrich:
	@. env/bin/activate && cat mock_transcripts.jsonl | python -u week5/enrich_transcripts.py | python week5/validate_schema.py
