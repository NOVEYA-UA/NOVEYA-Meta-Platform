#!/bin/bash

echo "🔐 Настройка NGINX и HTTPS для Protonovea Node..."

# Установка NGINX
sudo apt update && sudo apt install -y nginx

# Настройка базового прокси
sudo tee /etc/nginx/sites-available/protonovea > /dev/null <<EOL
server {
    listen 80;
    server_name your.domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/protonovea /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Установка Certbot для HTTPS
sudo apt install -y certbot python3-certbot-nginx

# Получение SSL-сертификата
echo "⚠️ ВАЖНО: Убедитесь, что DNS указывает на этот сервер и порт 80 открыт"
sudo certbot --nginx -d your.domain.com

# Автообновление сертификатов
echo "0 3 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab

echo "✅ Настройка завершена. Доступ по https://your.domain.com"
