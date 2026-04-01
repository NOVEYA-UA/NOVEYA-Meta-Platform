from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# Твой пароль (токен), который ты впишешь в расширение
MY_PASSWORD = "12345"

@app.route('/')
@app.route('/info')
@app.route('/relay')
def connect():
    # Проверяем, совпадает ли пароль из расширения с нашим
    check = request.headers.get('Authorization') or request.args.get('token')
    if check != MY_PASSWORD:
        return jsonify({"error": "Wrong Token"}), 401
    
    # Отдаем расширению данные твоего девайса, чтобы оно тебя узнало
    return jsonify({
        "status": "online",
        "server_name": "PROTONOVEYA_NODE",
        "deviceId": "4607b9b524025364977a669d78b7b2a82b6c0c854de395cd9ec988a208c32ac0"
    })

if __name__ == "__main__":
    # Запускаем прослушку сразу на двух портах, как просит система
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=18789)).start()
    app.run(host='0.0.0.0', port=18792)
