# news3001

Local news stack with:
- PHP + Nginx UI (`ui/`)
- FastAPI read API (`server/server.py`)
- FastAPI scraper API (`server/run_scraper.py`)
- PocketBase storage

## Docker quick start

Create your local env file from the template:

```bash
cp .env.example .env
```

Then start or rebuild the full stack:

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
```

Tail logs:

```bash
docker compose logs -f backend scraper nginx_server
```

Stop everything:

```bash
docker compose down
```

## Service URLs (current compose)

- UI (Nginx): `http://localhost:3049`
- Backend API: `http://localhost:4567`
- Scraper API: `http://localhost:987` (mapped from `"0987:5001"` in compose)
- PocketBase: `http://localhost:8080`

## Common API calls

Backend:

```bash
curl http://localhost:4567/
curl "http://localhost:4567/oldnews?date=2026-02-20"
curl http://localhost:4567/report
curl "http://localhost:4567/stats/day?date=2026-02-20"
```

Trigger scraper pipeline:

```bash
curl -X POST http://localhost:987/run
```

## Local development (without Docker)

Install backend dependencies:

```bash
cd server
uv sync --locked
```

Run backend API (port `5000`):

```bash
cd server
uv run server.py
```

Run scraper API (port `5001`):

```bash
cd server
uv run run_scraper.py
```

Run rule tests:

```bash
cd server
uv run tests/rules/run_rules_tests.py
```

## Notes

- The source of truth for container wiring is `docker-compose.yml`.
- Keep secrets in `.env` and commit only `.env.example`.
