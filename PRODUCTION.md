# Production Images

This repo includes production Dockerfiles for all runtime services.
The production Compose setup builds images without bind mounts, so you can run entirely from images.

## Build Images

```sh
docker compose -f docker-compose.prod.yml build
```

## Build Multi-Arch Images

Create and bootstrap a `buildx` builder:

```sh
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap
```

Build and push each image:

```sh
docker buildx build --platform linux/amd64,linux/arm64 -t jaypoch/news3001:php -f frontend/Dockerfile ./frontend --push
docker buildx build --platform linux/amd64,linux/arm64 -t jaypoch/news3001:nginx -f nginx/Dockerfile . --push
docker buildx build --platform linux/amd64,linux/arm64 -t jaypoch/news3001:backend ./backend --push
docker buildx build --platform linux/amd64,linux/arm64 -t jaypoch/news3001:scraper ./backend --push
```

## Tag Images For Docker Hub

```sh
docker tag news3001-php:latest jaypoch/news3001:php
docker tag news3001-nginx:latest jaypoch/news3001:nginx
docker tag news3001-backend:latest jaypoch/news3001:backend
docker tag news3001-scraper:latest jaypoch/news3001:scraper
```

## Push Images To Docker Hub

```sh
docker push jaypoch/news3001:php
docker push jaypoch/news3001:nginx
docker push jaypoch/news3001:backend
docker push jaypoch/news3001:scraper
```

## Run

```sh
docker compose -f docker-compose.build.yml up -d
```

## Run From Images Only

### Option A: Docker Hub

1. Copy `docker-compose.deploy.yml` and your `.env` file to the target machine.
2. Pull and run:

```sh
docker pull jaypoch/news3001:php
docker pull jaypoch/news3001:nginx
docker pull jaypoch/news3001:backend
docker pull jaypoch/news3001:scraper
docker compose -f docker-compose.deploy.yml up -d --no-build
```

### Option B: Offline Export/Import

1. On a build machine, export images:

```sh
docker save -o news3001-images.tar news3001-php:latest news3001-nginx:latest news3001-backend:latest news3001-scraper:latest
```

2. On the target machine, import the archive:

```sh
docker load -i news3001-images.tar
```

3. Copy `docker-compose.deploy.yml` and your `.env` file to the target machine, then run:

```sh
docker compose -f docker-compose.deploy.yml up -d --no-build
```

## Environment Variables

- `ADMIN_PASSWORD`
- `POCKETBASE_URL` (optional, default `http://pocketbase:8080`)
- `POCKETBASE_ADMIN_EMAIL`
- `POCKETBASE_ADMIN_PASSWORD`
- `OPENROUTER_API_KEY`
- `SERPAPI_API_KEY`
- `SCRAPER_TESTING_MODE` (optional, default `true`)

## Data Persistence

PocketBase data is stored in the named volume `pb_data`.
