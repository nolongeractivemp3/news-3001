# news3001

## Docker commands

Build and start the stack:

```bash
docker compose up -d --build
```

Run the scraper as a one-off command:

```bash
docker compose run --rm scraper
```

Follow logs:

```bash
docker compose logs -f backend
docker compose logs -f scraper
docker compose logs -f nginx_server
```

Stop everything:

```bash
docker compose down
```

The web server is currently exposed on `3049:80` (`http://localhost:3049`).

## Docker Compose example

```yaml
services:
  php_app:
    image: php:8.3-fpm
    volumes:
      - ./ui:/var/www/html

  nginx_server:
    image: nginx:alpine
    ports:
      - "3049:80"
    volumes:
      - ./ui:/var/www/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro

  backend:
    build: ./server
    image: news3001-server
    command: uv run server.py
    restart: always
    environment:
      POCKETBASE_URL: http://pocketbase:8080
      POCKETBASE_ADMIN_EMAIL: "<admin-email>"
      POCKETBASE_ADMIN_PASSWORD: "<admin-password>"
      OPENROUTER_API_KEY: "<openrouter-api-key>"

  scraper:
    image: news3001-server
    command: uv run run_scraper.py
    ports:
      - "5001:5001"
    environment:
      POCKETBASE_URL: http://pocketbase:8080
      POCKETBASE_ADMIN_EMAIL: "<admin-email>"
      POCKETBASE_ADMIN_PASSWORD: "<admin-password>"
      OPENROUTER_API_KEY: "<openrouter-api-key>"
      SERPAPI_API_KEY: "<serpapi-api-key>"
    depends_on:
      - backend
      - pocketbase

  pocketbase:
    image: ghcr.io/muchobien/pocketbase:latest
    ports:
      - "8080:8080"
    volumes:
      - ./pb_data:/pb_data
    command:
      - serve
      - --http=0.0.0.0:8080
      - --dir=/pb_data
    restart: unless-stopped
```
