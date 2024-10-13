from colorama import Fore, Style
from gpt4all import GPT4All
import time


MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'
model = GPT4All(
    model_name=MODEL_NAME, model_path='Models', device='cpu', verbose=False)

with model.chat_session():
    print('-------------------')
    while True:
        context = input(Fore.GREEN + 'Введите текст: ' + Style.RESET_ALL)
        print(Fore.BLUE + 'Ответ: ' + Style.RESET_ALL, end='')
        result = model.generate(prompt=context, temp=0)
        for char in result:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()
        # print(model.current_chat_session)
