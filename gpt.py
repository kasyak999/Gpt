from gpt4all import GPT4All
from telebot import TeleBot
import os
from dotenv import load_dotenv


load_dotenv()  # загрузка переменых окружения
MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'  # отвечает на русском
# MODEL_NAME = 'gpt4all-13b-snoozy-q4_0.gguf'  # отвечает быстро но на английском
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = TeleBot(token=TELEGRAM_TOKEN)

model = GPT4All(
    model_name=MODEL_NAME, model_path='Models', device='cpu', verbose=False)

with model.chat_session():
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Привет! Я бот gpt, как я могу помочь?")

    @bot.message_handler(commands=['exit'])
    def exit_script(message):
        bot.reply_to(message, "Пока")
        bot.stop_polling()
        # sys.exit(0)
        os._exit(0)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        if int(TELEGRAM_CHAT_ID) == message.chat.id:
            result = model.generate(
                prompt=message.text, temp=0, max_tokens=1024)
            bot.send_chat_action(chat_id=message.chat.id, action='typing')
            bot.send_message(
                chat_id=message.chat.id, text=result, parse_mode='Markdown')
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
