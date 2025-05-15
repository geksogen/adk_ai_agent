sudo apt update
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
pip install google-adk
pip install litellm
docker-compose up -d
docker exec -it ollama sh
