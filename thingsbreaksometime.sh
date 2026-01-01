sudo docker-compose down
sudo systemctl restart docker
sudo docker volume prune
sudo docker compose up -d --build
