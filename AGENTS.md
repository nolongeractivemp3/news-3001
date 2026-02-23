# Repository Guidelines

## Project Structure

```
news3001/
├── server/           # Python backend services
│   ├── server.py     # FastAPI read API
│   ├── scraper/      # Scraping pipeline, rules, enrichment
│   ├── tests/        # Backend tests
│   └── db/           # Database utilities
├── ui/               # PHP frontend (HTMX-driven)
│   ├── index.php     # Homepage
│   └── app/          # Components and assets
├── pb_data/          # PocketBase data
├── docker-compose.yml
└── nginx.conf
```

## Development

- Python package management: `uv` (see `server/pyproject.toml`)
- Local runtime: `docker compose up -d --build`

## Scraper Warning

**IMPORTANT**: The scraper pipeline runs periodically and fetches content from external sources. When modifying scraper logic in `server/scraper/`, be aware that:
- Changes may affect live data ingestion
- Test thoroughly before deploying
- Consider rate limiting and external API quotas
