# AI Agent Guide - `news3001`

This file is a fast orientation map for coding agents working in this repository.

## What this app does

- Aggregates local Koepenick/Treptow news.
- Stores articles, badges, and daily reports in PocketBase.
- Serves a PHP/HTMX frontend through Nginx.
- Runs Python FastAPI services for read API and scraping.

## Top-level structure

```text
news3001/
  docker-compose.yml        # service wiring
  nginx.conf               # php + static routing
  pb_data/                 # PocketBase persistent data
  server/                  # Python backend + scraper
  ui/                      # PHP frontend + JS + components
  .github/workflows/       # deploys ui/homepage to GitHub Pages
```

## Runtime architecture

1. Browser opens `http://localhost:3049` (Nginx).
2. `ui/index.php` loads HTMX components.
3. UI components call backend endpoints at `http://backend:5000/...` (internal Docker DNS).
4. Backend reads from PocketBase and returns JSON/text.
5. Scraper service (`server/scraper/server.py`) fetches and filters articles, then writes new day/news/report records to PocketBase.

## Key backend files

- `server/server.py`
  - Main read API (`/`, `/oldnews`, `/report`, `/oldreport`, `/rss`), port `5000`.
- `server/db/CRUD.py`
  - PocketBase client wrapper and collection read/write methods.
- `server/myclasses.py`
  - Core data objects: `News`, `Badge`, `Day`, `Report`.
- `server/run_scraper.py`
  - Starts scraper API service (port `5001` inside container).
- `server/scraper/pipeline.py`
  - Main scrape pipeline orchestrator.
- `server/scraper/fetchers.py`
  - Google (SerpAPI) and RSS fallback result fetch.
- `server/scraper/enrichment.py`
  - Full article scraping for each candidate URL.
- `server/scraper/filters.py`
  - LLM-based locality checks.
- `server/scraper/rules/*.py`
  - Fast, rule-based pre-filters (domain/path/keyword gates).
- `server/scraper/storage.py`
  - Converts articles to `News`, applies badges, saves day+report.
- `server/content_scraper.py`
  - Trafilatura extraction + LLM locality helper functions.
- `server/openrouter/report.py`
  - Daily summary prompt and save logic.
- `server/openrouter/badges.py`
  - Badge classification prompt and parsing.

## Key frontend files

- `ui/index.php`
  - Main page shell and HTMX mounts.
- `ui/components/card.php`
  - Fetches article JSON and renders cards.
- `ui/components/report.php`
  - Fetches and renders daily report modal.
- `ui/components/navbar.php`
  - Navigation + date picker include.
- `ui/components/datepicker.php`
  - Date-based history selection (`YYYY-MM-DD`).
- `ui/components/settings.php` + `ui/js/settings.js`
  - Source-ignore settings saved in cookies.
- `ui/sw.js`, `ui/manifest.json`
  - PWA service worker + manifest.

## API surface (current)

- Backend (port 5000 inside Docker network):
  - `GET /` -> today news
  - `GET /oldnews?date=YYYY-MM-DD`
  - `GET /report` -> today report text
  - `GET /oldreport?date=YYYY-MM-DD`
  - `GET /rss` -> live RSS feed
- Scraper service (host mapped `0987:5001` in current compose):
  - `GET /` -> health/status
  - `POST /run` -> run full scraping pipeline now

## Typical commands

- Start full stack:
  - `docker compose up -d --build`
- Stop:
  - `docker compose down`
- Follow logs:
  - `docker compose logs -f backend`
  - `docker compose logs -f scraper`
  - `docker compose logs -f nginx_server`
- Trigger scraper manually:
  - important dont run the scraper without user request its expensive and not good to run in a testing enviroment always ask the user before running the scraper
  - `curl -X POST http://localhost:0987/run`

## Environment variables used

- `POCKETBASE_URL`
- `POCKETBASE_ADMIN_EMAIL`
- `POCKETBASE_ADMIN_PASSWORD`
- `OPENROUTER_API_KEY`
- `SERPAPI_API_KEY` (scraper only)

## Where to edit for common tasks

- Change report style/tone: `server/openrouter/report.py`
- Change badge assignment logic: `server/openrouter/badges.py`
- Add fast inclusion/exclusion rules: `server/scraper/rules/*.py`
- Adjust strict/locality AI checks: `server/scraper/filters.py` and `server/content_scraper.py`
- Change card layout or data shown: `ui/components/card.php`
- Change report modal UI: `ui/components/report.php`
- Add/modify backend endpoints: `server/server.py`

## Important caveats for agents

- There are legacy/duplicate paths:
  - `server/scrape.py` is an older monolithic scraper path.
  - `ui/js/main.js` looks legacy and is not used by current HTMX flow.
  - `server/contentscraper.py` is only a thin import shim.
- There are no automated tests in this repo right now.
- `docker-compose.yml` currently contains plaintext secrets; avoid copying or reusing them.
- PocketBase collection name casing is mixed in code (`days`/`Days`, `report`/`Report`); keep this in mind when changing DB calls.

## Quick validation checklist after changes

1. `docker compose up -d --build`
2. Open `http://localhost:3049` and check news list loads.
3. Change date in UI and verify `/oldnews` path still works.
4. Open summary modal and verify report rendering.
5. Confirm new day/news/report records exist in PocketBase (`http://localhost:8080`).
