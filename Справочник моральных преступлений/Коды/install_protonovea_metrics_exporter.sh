#!/bin/bash

echo "📊 Установка кастомного экспортера метрик Protonovea (GPT Tokens/API Stats)"

# Установка Python окружения
sudo apt install -y python3-pip
pip3 install flask prometheus_client openai

# Создание сервиса экспортера
mkdir -p ~/protonovea-metrics
cd ~/protonovea-metrics

# Создание Flask-приложения
cat <<EOF > metrics_exporter.py
from flask import Response, Flask
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

gpt_input_tokens = Counter('gpt_input_tokens_total', 'Total input tokens sent to GPT')
gpt_output_tokens = Counter('gpt_output_tokens_total', 'Total output tokens received from GPT')
gpt_requests = Counter('gpt_requests_total', 'Total number of GPT API requests')
gpt_errors = Counter('gpt_errors_total', 'Total number of GPT API errors')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/simulate')  # демо-метод для тестов
def simulate():
    gpt_input_tokens.inc(500)
    gpt_output_tokens.inc(1200)
    gpt_requests.inc()
    return "Simulated API Call"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9101)
EOF

# Создание systemd-сервиса
sudo tee /etc/systemd/system/protonovea-metrics.service > /dev/null <<EOL
[Unit]
Description=Protonovea GPT Metrics Exporter
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/$USER/protonovea-metrics
ExecStart=/usr/bin/python3 metrics_exporter.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Запуск сервиса
sudo systemctl daemon-reexec
sudo systemctl start protonovea-metrics
sudo systemctl enable protonovea-metrics

echo "✅ Экспортер запущен на http://localhost:9101/metrics"
