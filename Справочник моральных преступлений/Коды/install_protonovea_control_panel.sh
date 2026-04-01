#!/bin/bash

echo "🧠 Установка панели управления Protonovea (ручные GPT-запросы + логирование)"

# Установка зависимостей
sudo apt update && sudo apt install -y python3-pip
pip3 install flask openai

# Создание директории
mkdir -p ~/protonovea-control
cd ~/protonovea-control

# Создание Flask-приложения
cat <<EOF > control_panel.py
from flask import Flask, request, render_template_string
import openai
from datetime import datetime

openai.api_key = "sk-***"

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Protonovea Control Panel</title>
<h2>Manual GPT Request</h2>
<form method=post>
  <textarea name=prompt rows=10 cols=80 placeholder="Enter your prompt here..."></textarea><br>
  <input type=submit value=Send>
</form>
{% if response %}
<h3>Response:</h3>
<pre>{{ response }}</pre>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def home():
    response = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            result = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            response = result["choices"][0]["message"]["content"]
            with open("gpt_log.txt", "a") as log:
                log.write(f"---\n{datetime.now()}\nPROMPT:\n{prompt}\nRESPONSE:\n{response}\n\n")
        except Exception as e:
            response = f"Error: {e}"
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
EOF

# Создание systemd-сервиса
sudo tee /etc/systemd/system/protonovea-control.service > /dev/null <<EOL
[Unit]
Description=Protonovea Control Panel
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/$USER/protonovea-control
ExecStart=/usr/bin/python3 control_panel.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Запуск
sudo systemctl daemon-reexec
sudo systemctl start protonovea-control
sudo systemctl enable protonovea-control

echo "✅ Панель управления доступна на http://localhost:5050"
