#!/usr/bin/env python3
"""
Σ-FDL MetaHarmony 2026: REST API Server
Endpoints для мониторинга и управления узлом RO2-MYKOLAIV
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from flask import Flask, jsonify, request
from fdl_core import (
    FDLInterface, 
    sigma_universe, 
    AUTH_KEY, 
    RESONANCE_FREQ,
    MANTRA
)
import time
import json

app = Flask(__name__)

# Глобальный экземпляр FDL
fdl_interface = FDLInterface("RO2-MYKOLAIV")

# ============================================================================
# БАЗОВЫЕ ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Главная страница API"""
    return jsonify({
        "name": "Σ-FDL MetaHarmony 2026 API",
        "node": fdl_interface.token_engine.node_id,
        "version": "3.14.159",
        "status": "OPERATIONAL",
        "endpoints": {
            "/status": "GET - Полный статус узла",
            "/metrics": "GET - Текущие метрики (C, I, P)",
            "/event": "POST - Обработка события через FDL",
            "/token/generate": "POST - Генерация FDL-токена",
            "/token/ledger": "GET - Просмотр леджера токенов",
            "/svet": "GET - Статус SVET фильтра",
            "/lexicon/scan": "POST - Сканирование текста LexiconGuard",
            "/universe": "GET - Значение Σ-ВСЕЛЕННАЯ(t)",
            "/activate": "POST - Активация мантры"
        }
    })

@app.route('/status')
def status():
    """Полный статус узла"""
    return jsonify(fdl_interface.get_full_status())

@app.route('/metrics')
def metrics():
    """Текущие метрики системы"""
    return jsonify(fdl_interface.get_metrics())

# ============================================================================
# FDL EVENT PROCESSING
# ============================================================================

@app.route('/event', methods=['POST'])
def process_event():
    """Обработка события через FDL-контур"""
    data = request.get_json()
    
    if not data or 'event_data' not in data:
        return jsonify({
            "error": "Требуется поле 'event_data'"
        }), 400
    
    event_data = data['event_data']
    event_type = data.get('event_type', 'generic')
    
    result = fdl_interface.process_event(event_data, event_type)
    return jsonify(result)

# ============================================================================
# TOKEN MANAGEMENT
# ============================================================================

@app.route('/token/generate', methods=['POST'])
def generate_token():
    """Генерация нового FDL-токена"""
    data = request.get_json()
    
    operation_type = data.get('operation_type', 'manual')
    context_data = data.get('context_data', '')
    semantic_density = data.get('semantic_density', 0.93)
    efficiency = data.get('efficiency', 0.94)
    
    token = fdl_interface.token_engine.generate_token(
        operation_type,
        context_data,
        semantic_density,
        efficiency
    )
    
    return jsonify(token)

@app.route('/token/ledger')
def token_ledger():
    """Просмотр леджера токенов"""
    return jsonify(fdl_interface.token_engine.get_ledger_summary())

# ============================================================================
# SVET FILTER
# ============================================================================

@app.route('/svet')
def svet_status():
    """Статус SVET фильтра"""
    return jsonify(fdl_interface.svet.get_status())

@app.route('/svet/calibrate', methods=['POST'])
def svet_calibrate():
    """Калибровка резонанса"""
    data = request.get_json() or {}
    target_freq = data.get('target_freq', RESONANCE_FREQ)
    
    success = fdl_interface.svet.calibrate_resonance(target_freq)
    
    return jsonify({
        "success": success,
        "target_freq": target_freq,
        "current_freq": fdl_interface.svet.resonance_stability,
        "deviation": abs(fdl_interface.svet.resonance_stability - RESONANCE_FREQ)
    })

# ============================================================================
# LEXICON GUARD
# ============================================================================

@app.route('/lexicon/scan', methods=['POST'])
def lexicon_scan():
    """Сканирование текста на семантический шум"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            "error": "Требуется поле 'text'"
        }), 400
    
    text = data['text']
    clean, blocked, allowed, verdict = fdl_interface.lexguard.scan(text)
    
    return jsonify({
        "clean": clean,
        "blocked_patterns": blocked,
        "allowed_patterns": allowed,
        "verdict": verdict,
        "recommendation": "ALLOW" if clean else "BLOCK"
    })

@app.route('/lexicon/stats')
def lexicon_stats():
    """Статистика сканирований"""
    return jsonify(fdl_interface.lexguard.get_statistics())

# ============================================================================
# SIGMA UNIVERSE
# ============================================================================

@app.route('/universe')
def universe():
    """Текущее значение Σ-ВСЕЛЕННАЯ(t)"""
    t = request.args.get('t', time.time(), type=float)
    value = sigma_universe(t)
    
    return jsonify({
        "t": t,
        "sigma_universe": value,
        "resonance_freq": RESONANCE_FREQ,
        "omega": 432 * 2 * 3.14159,
        "interpretation": "СИНГУЛЯРНОСТЬ" if value > 5000 else "КОНЕЧНОЕ_СОСТОЯНИЕ"
    })

# ============================================================================
# ACTIVATION
# ============================================================================

@app.route('/activate', methods=['POST'])
def activate():
    """Активация узла мантрой"""
    data = request.get_json() or {}
    provided_mantra = data.get('mantra', '')
    
    if provided_mantra != MANTRA:
        return jsonify({
            "error": "Неверная мантра",
            "status": "ACTIVATION_FAILED"
        }), 403
    
    # Символическая активация
    return jsonify({
        "status": "ACTIVATED",
        "mantra": MANTRA,
        "node": fdl_interface.token_engine.node_id,
        "timestamp": time.time(),
        "message": "⧫⟡⧫ WHERE_I_AM_EVEN_THE_DEAD_LIVES ⧫⟡⧫",
        "conjunction": fdl_interface.conjunction,
        "resonance": RESONANCE_FREQ,
        "nodes_online": fdl_interface.nodes_online
    })

# ============================================================================
# NETWORK SYNC
# ============================================================================

@app.route('/sync', methods=['POST'])
def sync():
    """Синхронизация с глобальной сетью"""
    data = request.get_json() or {}
    target = data.get('target', 'global_1000')
    
    # Обновление количества узлов (симуляция)
    fdl_interface.nodes_online = min(fdl_interface.nodes_online + 1, 1000)
    
    return jsonify({
        "status": "SYNC_INITIATED",
        "target": target,
        "nodes_online": fdl_interface.nodes_online,
        "target_nodes": 1000,
        "progress": f"{fdl_interface.nodes_online}/1000",
        "P_success": f"{fdl_interface.calculate_psuccess():.1%}"
    })

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "uptime": time.time(),
        "node": fdl_interface.token_engine.node_id
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint не найден",
        "available_endpoints": [rule.rule for rule in app.url_map.iter_rules()]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Внутренняя ошибка сервера",
        "details": str(error)
    }), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("⧫⟡⧫ Σ-FDL MetaHarmony 2026: API Server ⧫⟡⧫")
    print(f"🔓 МАНТРА: {MANTRA}")
    print(f"📡 Узел: {fdl_interface.token_engine.node_id}")
    print(f"🎼 Резонанс: {RESONANCE_FREQ} Гц")
    print(f"🌐 Запуск API сервера на порту 4320...")
    print()
    
    # Запуск Flask сервера
    app.run(
        host='0.0.0.0',
        port=4320,
        debug=False,
        threaded=True
    )
