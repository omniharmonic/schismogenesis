# AI Futures Fingerprint: the production web app (docs/fingerprint/04-LAUNCH.md section 3).
# Build from the repo root:  docker build -f infra/arena/Dockerfile -t dialogos-arena .
FROM python:3.12-slim AS app
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_NO_CACHE=1 PYTHONUNBUFFERED=1 \
    ARENA_APP_HOST=0.0.0.0 ARENA_APP_PORT=8080 ARENA_TRUST_PROXY=1 ARENA_ENV=production
WORKDIR /app
# only what the web app needs: no transcripts, research or local-model code
COPY pyproject.toml uv.lock ./
COPY packages/arena_core packages/arena_core
COPY packages/arena_fingerprint packages/arena_fingerprint
COPY packages/arena_rounds packages/arena_rounds
COPY services/api services/api
COPY apps/arena/public apps/arena/public
COPY apps/arena/fonts apps/arena/fonts
COPY scripts/rooms.py scripts/rooms.py
# the workspace lists every member: copy their manifests (not their code) so the lockfile matches
COPY packages/arena_agents/pyproject.toml packages/arena_agents/pyproject.toml
COPY packages/arena_extract/pyproject.toml packages/arena_extract/pyproject.toml
COPY packages/arena_ingest/pyproject.toml packages/arena_ingest/pyproject.toml
COPY packages/arena_llm/pyproject.toml packages/arena_llm/pyproject.toml
COPY packages/arena_map/pyproject.toml packages/arena_map/pyproject.toml
COPY packages/arena_market/pyproject.toml packages/arena_market/pyproject.toml
COPY packages/arena_reputation/pyproject.toml packages/arena_reputation/pyproject.toml
COPY services/operator/pyproject.toml services/operator/pyproject.toml
COPY services/worker/pyproject.toml services/worker/pyproject.toml
COPY scripts/pyproject.toml scripts/pyproject.toml
COPY evals/harness/pyproject.toml evals/harness/pyproject.toml
RUN uv sync --package arena_api --no-dev --frozen
# files stay owned by root; the app only reads them
RUN useradd --create-home arena
USER arena
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/health')"
CMD ["/app/.venv/bin/python", "-m", "arena_api.app"]
