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
