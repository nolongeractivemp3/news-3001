commands:
build:
sudo docker compose up -d --build
build tools 
sudo docker compose --profile tools build
run tools
sudo docker compose --profile tools run --rm scraper
# important
change port from 80:80 to x:80 where x is the desired port number
# logs
sudo docker compose logs -f news3001

docker compose example:
```yaml
services:
  php_app:
    image: php:8.3-fpm
    volumes:
      - ./ui:/var/www/html

  nginx_server:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./ui:/var/www/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro

  backend:
    build: ./server
    command: uv run server.py
    restart: always
    environment:
      POCKETBASE_URL: http://pocketbase:8080
      POCKETBASE_ADMIN_EMAIL: "your-admin@example.com"
      POCKETBASE_ADMIN_PASSWORD: "your-admin-password"
      OPENROUTER_API_KEY: "your-openrouter-key"

  scraper:
    build: ./server
    command: uv run python scrape.py
    profiles: ["tools"]
    environment:
      POCKETBASE_URL: http://pocketbase:8080
      POCKETBASE_ADMIN_EMAIL: "your-admin@example.com"
      POCKETBASE_ADMIN_PASSWORD: "your-admin-password"
      OPENROUTER_API_KEY: "your-openrouter-key"
      SERPAPI_API_KEY: "your-serpapi-key"

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
