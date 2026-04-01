#!/bin/bash

echo "🔧 Установка Protonovea Node..."

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker и Docker Compose
sudo apt install -y docker.io docker-compose

# Создание проекта
mkdir -p ~/protonovea-node
cd ~/protonovea-node

# Распаковка проекта, если архив заранее скопирован в домашнюю папку
if [ -f ~/protonovea-node.zip ]; then
    unzip ~/protonovea-node.zip -d ~/protonovea-node/
else
    echo "❗ Архив protonovea-node.zip не найден. Скопируйте его в домашнюю папку."
    exit 1
fi

# Настройка прав
sudo chown -R $USER:$USER ~/protonovea-node

# Запуск
cd ~/protonovea-node
sudo docker-compose up -d --build

echo "✅ Установка завершена. Узел Protonovea запущен!"
