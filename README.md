commands:
build:
sudo docker compose up -d --build
# important
change port from 80:80 to x:80 where x is the desired port number
# logs
sudo docker compose logs -f news3001
