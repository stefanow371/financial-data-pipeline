build:
	docker compose build

start:
	docker compose up -d

run:
	docker compose exec ingest-data poetry run python -m script.main

stop:
	docker compose down

shell:
	docker compose exec ingest-data /bin/bash

poetry-update:
	docker compose exec ingest-data poetry update

poetry-add:
	docker compose exec ingest-data poetry add $(PKG)

poetry-lock:
	docker compose exec ingest-data poetry lock

poetry-show:
	docker compose exec ingest-data poetry show --outdated