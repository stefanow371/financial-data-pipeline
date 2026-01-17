setup:
	docker compose up -d --build

run:
	docker compose exec ingest-data python scripts/ingest_data.py

stop:
	docker compose down

shell:
	docker compose exec ingest-data /bin/bash

	# Aktualizuje wszystkie paczki do najnowszych wersji zgodnych z pyproject.toml
poetry-update:
	docker compose exec ingest-data poetry update

poetry-add:
	docker compose exec ingest-data poetry add $(PKG)

poetry-lock:
	docker compose exec ingest-data poetry lock

poetry-show:
	docker compose exec ingest-data poetry show --outdated