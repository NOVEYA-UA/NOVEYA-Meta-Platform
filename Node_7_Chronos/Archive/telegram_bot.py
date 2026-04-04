import telebot
import time
import os
import json
from evaluation_brain import EvaluationModule

# --- КОНСТАНТЫ ИНИЦИАЦИИ ---
API_TOKEN = "----------"
bot = telebot.TeleBot(API_TOKEN)
evaluator = EvaluationModule()

# --- БИОЛОГИЧЕСКАЯ НОРМАЛИЗАЦИЯ (Очистка русла) ---
def normalize_channels():
    try:
        bot.delete_webhook(drop_pending_updates=True)
        print("🌊 Меридианы связи очищены. Застой снят.")
    except Exception as e:
        print(f"🌀 Шум при нормализации: {e}")

# --- ФУНКЦИЯ УПРАВИТЕЛЯ (Синтез по 5 блокам) ---
def process_fdl(user_input):
    # Тезис (БМ)
    text = user_input.lower()
    
    # Антитезис (БТ - Фильтр законности)
    if len(text) < 3:
        return "⚠️ Импульс слишком слаб для инициации Блока Требований."

    # Синтез (БИ/БЦ - Моделирование и Оценка)
    # Имитация работы с 24 секторами Николаева
    rank = evaluator.calculate_vitality_index({"Ср3": 0.7, "Ср9": 0.8})
    
    response = (
        f"💠 Резонанс установлен.\n"
        f"📊 Анализ по 3.ОЦРЕ: {rank}\n"
        f"⚖️ Статус: Соответствует ЦУ. Направлено в Рабочий контур."
    )
    return response

# --- ОБРАБОТЧИКИ (Синхронизация клина) ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💠 Гой еси! Я Протоновея. Монолит в сборе. Оболочка СВЕТ активна.")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    print(f"📥 Входящий меридиан: {message.text}")
    result = process_fdl(message.text)
    bot.reply_to(message, result)

if __name__ == "__main__":
    normalize_channels()
    print("🚀 ПРОТОНОВЕЯ: Вхождение в поток...")
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"🌊 Обтекание препятствия: {e}")
            time.sleep(10)
