from flask import Flask, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/info')
def info():
    # Ответ, который ожидает расширение для появления сервера в списке
    return jsonify({
        "status": "active",
        "server_name": "PROTONOVEYA_MONOLITH_V3",
        "device_id": "4607b9b524025364977a669d78b7b2a82b6c0c854de395cd9ec988a208c32ac0",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Запуск на портах, которые требует расширение
    print("📡 ОЖИВЛЯЮ МЕРИДИАНЫ: 18789 и 18792...")
    threading.Thread(target=lambda: app.run(port=18789, debug=False, use_reloader=False)).start()
    app.run(port=18792, debug=False, use_reloader=False)
