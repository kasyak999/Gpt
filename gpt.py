from gpt4all import GPT4All
from telebot import TeleBot
import os
from dotenv import load_dotenv


load_dotenv()  # загрузка переменых окружения
MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'  # отвечает на русском
# MODEL_NAME = 'gpt4all-13b-snoozy-q4_0.gguf'  # отвечает быстро но на английском
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TEMP_BOT = 0.5  # креативность бота
MAX_TOKEN = 1024  # Длина ответа бота
model = GPT4All(
    model_name=MODEL_NAME, model_path='Models', device='cpu', verbose=False)


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
    if len(result) > 4096:
        bot.send_message(
            chat_id=message.chat.id, text=result[:4095], parse_mode='Markdown')
        bot.send_message(
            chat_id=message.chat.id, text=result[4095:], parse_mode='Markdown')
    else:
        bot.send_message(
            chat_id=message.chat.id, text=result, parse_mode='Markdown')


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
            bot.send_chat_action(chat_id=message.chat.id, action='typing')
            if int(TELEGRAM_CHAT_ID) == message.chat.id:
                result = model.generate(
                    prompt=message.text, temp=TEMP_BOT, max_tokens=MAX_TOKEN)
                sending_message(bot, message, result)
            else:
                result = (
                    'Вы не можете отправлять запросы боту \n'
                    f'<b>Ваш id {message.chat.id}</b>'
                )
                bot.send_message(
                    chat_id=message.chat.id, text=result, parse_mode='HTML')

        try:
            bot.polling()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
