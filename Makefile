install:
	pip install -e ".[dev]"

dev:
	uvicorn apps.api.app.main:app --reload

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy

check:
	ruff check .
	ruff format --check .
	mypy
	pytest -v

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f