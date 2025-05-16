sudo apt update
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
pip install google-adk
pip install litellm
docker-compose up -d
if [ $? -eq 0 ]; then
    echo "Контейнер Ollama успешно запущен."

    # Запуск модели qwen2.5:7b
    docker exec -it ollama ollama run qwen2.5:7b

    # Проверка, что модель успешно запущена
    if [ $? -eq 0 ]; then
        echo "Модель qwen2.5:7b успешно запущена."
    else
        echo "Ошибка при запуске модели qwen2.5:7b."
    fi
else
    echo "Ошибка при запуске контейнера Ollama."
fi
