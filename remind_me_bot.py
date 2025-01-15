import telebot
import datetime
import time
import webbrowser
from telebot import types
import threading
import random
import os

bot = telebot.TeleBot("TOKEN")


reminders = []

facts = [
    "Снижение стресса: Когда задачи выполняются вовремя, это помогает избежать стресса, связанного с дедлайнами.",
    "Повышение производительности: Регулярное выполнение задач вовремя способствует улучшению навыков управления временем.",
    "Улучшение качества работы: Когда есть достаточно времени для выполнения задачи, это позволяет уделять больше внимания деталям.",
    "Стимулирование креативности: Когда задачи выполняются без спешки, у вас больше времени на обдумывание и поиск новых идей.",
    "Укрепление репутации: Выполнение задач вовремя демонстрирует вашу надежность и организованность."
]

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Установить напоминание")
    markup.add(item1)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}\nЯ бот, который будет напоминать тебе о невыполненных задачах! \nнажми\n/help", reply_markup=markup)
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}\nВот список доступных команд:\n/start\n/help - помощь\n/site - наш сайт\n/audio\n/video\n/photo\n/fact\n/edit")

@bot.message_handler(commands=["fact"])
def fact_message(message):
    random_fact = random.choice(facts)
    bot.reply_to(message, f"Лови факт о пользе выполнения задач вовремя: {random_fact}")

@bot.message_handler(commands=["site"])
def site(message):
    webbrowser.open("https://google.com")

@bot.message_handler(content_types=["photo", "audio", "video"])
def get_media(message):
    if message.content_type == "photo":
        bot.reply_to(message, "Какое красивое фото!")
    elif message.content_type == "audio":
        bot.reply_to(message, "Прикольно!")
    elif message.content_type == "video":
        bot.reply_to(message, "Прикольно!")

@bot.message_handler(func=lambda message: message.text == "Установить напоминание")
def set_reminder(message):
    msg = bot.send_message(message.chat.id, "Введите время напоминания в формате ЧЧ:ММ и подпись через запятую (например, 10:30, Встреча):")
    bot.register_next_step_handler(msg, process_reminder)

def process_reminder(message):
    try:
        time_str, note = message.text.split(',')
        reminders.append((time_str.strip(), note.strip()))
        bot.send_message(message.chat.id, f"Напоминание установлено на {time_str.strip()} с подписью '{note.strip()}'.")
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат. Попробуйте снова.")

def send_reminders(chat_id):
    video_path = r'C:\Users\Admin\Downloads\PG02. Разработка Telegram-бота_files\SVID_20241223_101509_1.mp4'
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder_time, note in reminders:
            if now == reminder_time:
                random_fact = random.choice(facts)
                bot.send_message(chat_id, f"Напоминание: {note}\nФакт: {random_fact}")
                os.startfile(video_path)
                time.sleep(61)
            time.sleep(1)

bot.infinity_polling()
