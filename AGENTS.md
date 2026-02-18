# Repository Guidelines

## Project Structure & Module Organization
- `server/`: Python services and scraping pipeline.
- `server/server.py`: Main FastAPI read API (`/`, `/oldnews`, `/report`, `/rss`).
- `server/scraper/`: Scraper pipeline, rule filters, enrichment, and storage.
- `server/tests/`: Backend tests (currently rule-focused, e.g. `test_rules.py`).
- `ui/`: PHP frontend, HTMX-driven components, JS settings logic, and PWA assets.
- `ui/components/`: Render units (`card.php`, `report.php`, `navbar.php`, etc.).
- `ui/homepage/`: Static homepage deployed by GitHub Actions (`.github/workflows/static.yml`).
- `docker-compose.yml`, `nginx.conf`: Local runtime wiring (Nginx + PHP + backend + scraper + PocketBase).

## Build, Test, and Development Commands
- `docker compose up -d --build`: Build and start the full local stack.
- `docker compose down`: Stop all services.
- `docker compose logs -f backend scraper nginx_server`: Tail service logs.
- `cd server && uv sync --locked`: Install Python dependencies with `uv`.
- `cd server && uv run server.py`: Run backend API on port `5000`.
- `cd server && uv run run_scraper.py`: Run scraper API on port `5001`.

## Coding Style & Naming Conventions
- Python: 4-space indentation, `snake_case` for functions/files, `CamelCase` for classes, prefer type hints on new/changed code.
- PHP: Follow existing component style (`ui/components/*.php`), keep variables descriptive (`$ignoredSources`, `$sourceNormalized`).
- JavaScript: Use `const`/`let`, `camelCase`, and small focused functions.
- Keep modules narrowly scoped (rules in `server/scraper/rules/`, UI concerns in `ui/components/`).

## Commit & Pull Request Guidelines
- Commit style in history is short, imperative, and scoped (example: `Add exact-path non-article rejection rule`).
- Prefer one logical change per commit; avoid vague messages like `wip`.
- PRs should include a clear summary of what changed and why.
- Include linked issue or branch context in the PR description.
- Include test evidence (`python -m unittest ...`, manual Docker checks).

## Security & Configuration Tips
- Treat API keys and PocketBase credentials as secrets; use environment variables, not committed plaintext.
- Review `docker-compose.yml` before sharing; sanitize local credentials.
