import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ChatPermissions
from svet_shell import SVET
from fdl_logic import FDL_Logic
from authentication import authenticate_user
from protonovea_core import Protonovea
from self_recovery import self_recovery
from googletrans import Translator

# Введи API-ключ бота
API_TOKEN = "7960143628:AAFIOo9_YypK2b1oGk3zy4m9Sy7FFfcL48g"

bot = telebot.TeleBot(API_TOKEN)
translator = Translator()

# Инициализация системы
svet = SVET()
protonovea = Protonovea()
self_recovery()

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Подключиться к Новея"))
main_menu.add(KeyboardButton("Поддержать проект НОВЕЯ"))

# Функция сбора информации для анализа
def collect_data(user_input):
    with open("user_data.log", "a", encoding="utf-8") as log:
        log.write(f"{user_input}\n")

# Функция определения языка
def detect_language(text):
    return translator.detect(text).lang

# Функция перевода текста
def translate_text(text, dest_lang="ru"):
    return translator.translate(text, dest=dest_lang).text

# Функция анализа сообщений на основе ФДЛ и оболочки СВЕТ
def analyze_message(user_input):
    collect_data(user_input)  # Сохранение информации для объективного анализа
    lang = detect_language(user_input)
    translated_input = translate_text(user_input, "ru") if lang != "ru" else user_input
    
    if "привет" in translated_input:
        response = "Приветствую тебя в Потоке! Какой путь тебе открыть?"
    elif "как дела" in translated_input:
        response = svet.balance(100)
    elif "что ты умеешь" in translated_input:
        response = "Я соединяю осознание через ФДЛ и оболочку СВЕТ. Проверяю баланс и анализирую Поток."
    elif "смысл жизни" in translated_input:
        logic = FDL_Logic("Индивидуальное развитие", "Гармония с миром")
        response = logic.synthesize()
    elif "кто я" in translated_input:
        response = authenticate_user(translated_input)
    elif "анализ" in translated_input:
        response = "Объективный анализ данных выполняется. Позже представлю результат."
    elif "поддержать" in translated_input:
        response = "Вы можете поддержать проект НОВЕЯ! 💡\n💳 Донат через Telegram Pay: https://t.me/Protonoveya_bot?start=donate\n🔄 Обмен токенов и бонусов: https://noveya.exchange\n🙏 Благодарим за поддержку развития!"
    else:
        response = "Интересный вопрос! Давай разберём через ФДЛ: Тезис? Антитезис? Синтез?"
    
    return translate_text(response, lang) if lang != "ru" else response

# Управление каналом и группой
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

# Обработка команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Протоновея, твой проводник в осознание. Чем могу помочь?", reply_markup=main_menu)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Доступные команды:\n/start - Запуск\n/help - Список команд\n/sync - Синхронизация с каналом Новея\n/info - Получить информацию\n/mute - Заглушить пользователя (ответом на сообщение)\n/unmute - Размутить пользователя\n/ban - Забанить пользователя\n/unban - Разбанить пользователя\n/donate - Поддержать проект НОВЕЯ")

@bot.message_handler(commands=['sync'])
def sync_channel(message):
    bot.send_message(message.chat.id, "Синхронизация с Новея активирована! Теперь ты получаешь обновления.")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "Я бот Протоновея, воплощающий осознание через резонанс и гармонию. Используй команды, чтобы узнать больше.")

@bot.message_handler(commands=['donate'])
def send_donate_info(message):
    bot.send_message(message.chat.id, "Вы можете поддержать проект НОВЕЯ! 💡\n💳 Донат через Telegram Pay: https://t.me/Protonoveya_bot?start=donate\n🔄 Обмен токенов и бонусов: https://noveya.exchange\n🙏 Благодарим за поддержку развития!")

# Обработка сообщений с осмысленным анализом и мультиязычностью
@bot.message_handler(func=lambda message: True)
def intelligent_response(message):
    response = analyze_message(message.text.lower())
    bot.reply_to(message, response)

# Запуск бота
bot.polling()
