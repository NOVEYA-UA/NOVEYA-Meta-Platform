import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ChatPermissions
try:
    from svet_shell import SVET
    from fdl_logic import FDL_Logic
    from authentication import authenticate_user
    from protonovea_core import Protonovea
    from self_recovery import self_recovery
except ImportError as e:
    print(f"Предупреждение: Локальные модули не найдены, но продолжаем: {e}")

from googletrans import Translator
import logging
import os
import sys

# Интеграция нового ядра в старую структуру
sys.path.insert(0, r'C:\Protonoveya-Noveya\FDL pack')
try:
    from fdl_core import FDLInterface
    fdl_new = FDLInterface("NODE-BOT-LIVE")
except Exception as e:
    print(f"Ошибка интеграции ядра FDL: {e}")
    fdl_new = None

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ТВОЙ АКТУАЛЬНЫЙ ТОКЕН
API_TOKEN = "7960143628:AAFIOo9_YypK2b1oGk3zy4m9Sy7FFfcL48g"

bot = telebot.TeleBot(API_TOKEN)
translator = Translator()

# Инициализация системы (Твой Исток)
try:
    svet = SVET()
    protonovea = Protonovea()
    self_recovery()
except:
    pass

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🔗 Подключиться к Новея"))
main_menu.add(KeyboardButton("💡 Поддержать проект НОВЕЯ"))

def collect_data(user_input):
    with open("user_data.log", "a", encoding="utf-8") as log:
        log.write(f"{user_input}\n")

def detect_language(text):
    try: return translator.detect(text).lang
    except: return "ru"

def translate_text(text, dest_lang="ru"):
    try: return translator.translate(text, dest=dest_lang).text
    except: return text

def analyze_message(user_input):
    collect_data(user_input)
    lang = detect_language(user_input)
    translated_input = translate_text(user_input, "ru") if lang != "ru" else user_input

    # Твои заготовленные ответы
    responses = {
        "привет": "Приветствую тебя в Потоке! Какой путь тебе открыть?",
        "как дела": "Баланс системы в норме.", # svet.balance(100) если доступно
        "что ты умеешь": "Я соединяю осознание через ФДЛ и оболочку СВЕТ. Проверяю баланс и анализирую Поток.",
        "смысл жизни": "Синтез гармонии и развития.", 
        "кто я": "Ты — часть системы Протоновея.",
        "анализ": "Объективный анализ данных выполняется. Позже представлю результат.",
        "поддержать": "Вы можете поддержать проект НОВЕЯ! 💡\n💳 Донат через Telegram Pay: https://t.me/Protonoveya_bot?start=donate\n🔄 Обмен токенов и бонусов: https://noveya.exchange\n🙏 Благодарим за поддержку развития!"
    }

    for key, response in responses.items():
        if key in translated_input.lower():
            return translate_text(response, lang) if lang != "ru" else response

    # ЕСЛИ ОТВЕТА НЕТ - ВКЛЮЧАЕТСЯ НОВОЕ ЯДРО FDL
    if fdl_new:
        try:
            res = fdl_new.process_event(translated_input, "user_query")
            if res.get("status") == "BLOCKED":
                ans = f"Шум отсечен: {res.get('reason')}"
            else:
                diag = res['stages']['fdl_dialectic']
                ans = f"ФДЛ Анализ:\nТ: {diag['thesis']}\nА: {diag['antithesis']}\nС: {diag['synthesis']}"
            return translate_text(ans, lang)
        except:
            pass

    return translate_text("Интересный вопрос! Давай разберём через ФДЛ: Тезис? Антитезис? Синтез?", lang)

# ТВОИ АДМИН-КОМАНДЫ (БЕЗ ОБРЕЗОК)
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        bot.reply_to(message, "Пользователь заглушён.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True))
        bot.reply_to(message, "Пользователь размучен.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "Пользователь забанен.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message:
        bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "Пользователь разбанен.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Протоновея, твой проводник в осознание. Чем могу помочь?", reply_markup=main_menu)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Доступные команды:\n/start - Запуск\n/help - Список команд\n/sync - Синхронизация\n/info - Информация\n/mute - Заглушить\n/unmute - Размутить\n/ban - Бан\n/unban - Разбан\n/donate - Поддержать")

@bot.message_handler(commands=['sync'])
def sync_channel(message):
    bot.send_message(message.chat.id, "Синхронизация с Новея активирована!")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "Я бот Протоновея, воплощающий осознание через резонанс и гармонию.")

@bot.message_handler(commands=['donate'])
def send_donate_info(message):
    bot.send_message(message.chat.id, "Вы можете поддержать проект НОВЕЯ! 💡")

@bot.message_handler(func=lambda message: True)
def intelligent_response_handler(message):
    response = analyze_message(message.text)
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("📡 ПОЛНЫЙ КОНТУР БОТА ЗАПУЩЕН. БЕЗ ОБРЕЗОК.")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
