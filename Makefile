COMPOSE = docker compose --env-file .env -f infra/docker-compose.yml --profile cloud-dev
ALEMBIC = uv run alembic -c packages/arena_core/alembic.ini

.PHONY: ci lint typecheck test redline up down migrate seed

ci: lint typecheck test redline

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run pyright

test:
	uv run pytest

redline:
	uv run arena redline

up:
	$(COMPOSE) up -d --wait

down:
	$(COMPOSE) down

migrate:
	$(ALEMBIC) upgrade head

seed:
	uv run arena seed load
	uv run arena seed verify
