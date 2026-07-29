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

DOCKER_IMAGE = emmetthannam26/ds5111-pipeline:latest
INPUT_IDS = tests/fixtures/weekly_youtube_ids

# All docker- targets run as the invoking user (no sudo) -- the ubuntu
# user is a member of the docker group, so plain `docker` is sufficient.
.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE) .

.PHONY: docker-run
docker-run:
	cat $(INPUT_IDS) | docker run -i --env-file .env $(DOCKER_IMAGE)

.PHONY: docker-clean
docker-clean:
	-docker rm -f $$(docker ps -aq --filter ancestor=$(DOCKER_IMAGE)) 2>/dev/null
	-docker rmi $(DOCKER_IMAGE) 2>/dev/null

.PHONY: docker-push
docker-push:
	docker push $(DOCKER_IMAGE)

.PHONY: docker-all
docker-all: docker-build docker-run docker-clean
