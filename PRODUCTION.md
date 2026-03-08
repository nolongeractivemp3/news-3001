Production Images

This repo now has production Dockerfiles for all runtime services.
The production compose file builds images without bind mounts, so you can run from images alone.

Build images
  docker compose -f docker-compose.prod.yml build

Build multi-arch images (amd64 + arm64)
  docker buildx create --name multiarch --use
  docker buildx inspect --bootstrap

  docker buildx build --platform linux/amd64,linux/arm64 \
    -t jaypoch/news3001:php -f frontend/Dockerfile ./frontend --push

  docker buildx build --platform linux/amd64,linux/arm64 \
    -t jaypoch/news3001:nginx -f nginx/Dockerfile . --push

  docker buildx build --platform linux/amd64,linux/arm64 \
    -t jaypoch/news3001:backend ./backend --push

  docker buildx build --platform linux/amd64,linux/arm64 \
    -t jaypoch/news3001:scraper ./backend --push

Tag images for Docker Hub
  docker tag news3001-php:latest jaypoch/news3001:php
  docker tag news3001-nginx:latest jaypoch/news3001:nginx
  docker tag news3001-backend:latest jaypoch/news3001:backend
  docker tag news3001-scraper:latest jaypoch/news3001:scraper

Push images to Docker Hub
  docker push jaypoch/news3001:php
  docker push jaypoch/news3001:nginx
  docker push jaypoch/news3001:backend
  docker push jaypoch/news3001:scraper

Run
  docker compose -f docker-compose.build.yml up -d

Run from images only (no source needed)
Option A: Docker Hub
1) Copy `docker-compose.deploy.yml` and your `.env` file to the target machine.
2) Pull and run:
  docker pull jaypoch/news3001:php
  docker pull jaypoch/news3001:nginx
  docker pull jaypoch/news3001:backend
  docker pull jaypoch/news3001:scraper
  docker compose -f docker-compose.deploy.yml up -d --no-build

Option B: Offline export/import
1) On a build machine, export images:
  docker save -o news3001-images.tar \
    news3001-php:latest \
    news3001-nginx:latest \
    news3001-backend:latest \
    news3001-scraper:latest

2) On the target machine, import:
  docker load -i news3001-images.tar

3) Copy `docker-compose.deploy.yml` and your `.env` file to the target machine, then run:
  docker compose -f docker-compose.deploy.yml up -d --no-build

Environment variables
  ADMIN_PASSWORD
  POCKETBASE_URL (optional, default http://pocketbase:8080)
  POCKETBASE_ADMIN_EMAIL
  POCKETBASE_ADMIN_PASSWORD
  OPENROUTER_API_KEY
  SERPAPI_API_KEY
  SCRAPER_TESTING_MODE (optional, default true)

Data persistence
  PocketBase data is stored in a named volume `pb_data`.
