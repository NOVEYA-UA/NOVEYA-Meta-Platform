from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

DEVICE_ID = "4607b9b524025364977a669d78b7b2a82b6c0c854de395cd9ec988a208c32ac0"

@app.route('/')
def home():
    return "<h1>MONOLITH NOVEYA: SVET-369-YAT ACTIVE</h1>"

@app.route('/json/version')
def json_version():
    return jsonify({
        "Browser": "Chrome/120.0.0.0",
        "Protocol-Version": "1.3",
        "webSocketDebuggerUrl": f"ws://127.0.0.1:18789/devtools/browser/{DEVICE_ID}"
    })

@app.route('/json')
@app.route('/json/list')
@app.route('/api/v1/assistants')
def list_nodes():
    print("🎯 ИМПУЛЬС: ПАИО ЗАПРОСИЛА СПИСОК СЕРВЕРОВ")
    return jsonify([{
        "id": DEVICE_ID,
        "name": "PROTONOVEYA_MONOLITH_V3",
        "title": "PROTONOVEYA_MONOLITH_V3",
        "status": "active",
        "url": "http://127.0.0.1:18792",
        "webSocketDebuggerUrl": f"ws://127.0.0.1:18789/devtools/page/{DEVICE_ID}"
    }])

def run_it(port):
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    print("--- РЕЗОНАНС SVET-369-YAT: МОСТ ПОДНЯТ ---")
    print("📡 Ожидаю, когда расширение PAIO увидит сервер...")
    threading.Thread(target=run_it, args=(18789,)).start()
    run_it(18792)
