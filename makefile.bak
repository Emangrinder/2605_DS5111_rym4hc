ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip
export PYTHONPATH := .

default:
	@cat makefile

env:
	python3 -m venv $(ENV)
	$(PIP) install --upgrade pip

update: env
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m pylint bin/ lib/ tests/

test:
	$(PYTHON) -m pytest -vv tests
run:
	@echo "Usage: make run STAGE=extract|enrich"
	$(PYTHON) bin/$(STAGE)_transcripts.py
test_enrich:
	@cat mock_transcripts.jsonl | $(PYTHON) bin/enrich_transcripts.py | $(PYTHON) bin/validate_schema.py
.PHONY: load
load:
	@echo "Initiating Cloud Data Warehouse Synchronizer Node..."
	cat mock_transcripts.jsonl | python bin/load_snowflake.py
