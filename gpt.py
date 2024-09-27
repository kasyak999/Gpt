from gpt4all import GPT4All
from telebot import TeleBot
import os
from dotenv import load_dotenv
import threading
import time


load_dotenv()  # загрузка переменых окружения
MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'  # отвечает на русском
# MODEL_NAME = 'gpt4all-13b-snoozy-q4_0.gguf'  # отвечает быстро но на английском
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TEMP_BOT = 0.5  # креативность бота
MAX_TOKEN = 5000  # Длина ответа бота
model = GPT4All(
    model_name=MODEL_NAME, model_path='Models', device='cpu', verbose=False)
stop_typing = True


def check_tokens():
    """Проверка переменых окружения."""
    errors = ''
    if not globals()['TELEGRAM_TOKEN']:
        errors += 'Не указан токен бота. \n'
    if not globals()['TELEGRAM_CHAT_ID']:
        errors += 'Не уазан ид чата \n'
    if errors:
        raise ValueError(errors)


def sending_message(bot, message, result):
    """Отправка сообщения"""
    # print(len(result))
    maximum = 4096  # Ограничение символов в телеграме
    for i in range(0, len(result), maximum):
        bot.send_message(
            chat_id=message.chat.id, text=result[i:i+maximum],
            parse_mode='Markdown')


def task_runner(bot_value, message):
    """Надпись бот печатает"""
    global stop_typing
    while stop_typing:
        bot_value.send_chat_action(chat_id=message, action='typing')
        time.sleep(4)
    stop_typing = True


if __name__ == '__main__':
    check_tokens()
    bot = TeleBot(token=TELEGRAM_TOKEN)

    with model.chat_session():
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            """Ввод команды /start"""
            bot.reply_to(message, "Привет! Я бот gpt, как я могу помочь?")

        @bot.message_handler(commands=['exit'])
        def exit_script(message):
            """Отключение бота"""
            bot.reply_to(message, "Пока")
            bot.stop_polling()
            os._exit(0)

        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            """Диалог с ботом"""
            threading.Thread(  # запускаем в фоном режиме
                target=task_runner, args=(bot, message.chat.id)).start()
            if int(TELEGRAM_CHAT_ID) == message.chat.id:
                result = model.generate(
                    prompt=message.text, temp=TEMP_BOT, max_tokens=MAX_TOKEN)
            else:
                result = (
                    'Вы не можете отправлять запросы боту \n'
                    f'***Ваш id {message.chat.id}***'
                )
            global stop_typing
            stop_typing = False
            sending_message(bot, message, result)

        try:
            bot.polling()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
