COMPOSE = docker compose --env-file .env -f infra/docker-compose.yml --profile cloud-dev
ALEMBIC = uv run alembic -c packages/arena_core/alembic.ini

.PHONY: ci lint typecheck test test-js load-test redline up down migrate seed bundle app demo-room

ci: lint typecheck test test-js redline

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run pyright

test:
	uv run pytest

load-test:
	ARENA_LOAD_TEST=1 uv run pytest packages/arena_rounds/tests/test_launch_analysis.py -k large -s

test-js:
	node --test apps/arena/tests/*.test.mjs

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

# AI Futures Fingerprint (docs/fingerprint/). Serves http://localhost:8800
bundle:
	uv run python scripts/build_fingerprint.py

app: migrate
	uv run python scripts/rooms.py ensure
	uv run python -m arena_api.app

demo-room: migrate
	uv run python scripts/rooms.py demo
