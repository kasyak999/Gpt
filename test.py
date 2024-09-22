from colorama import Fore, Style
from gpt4all import GPT4All


MODEL_NAME = 'Meta-Llama-3-8B-Instruct.Q4_0.gguf'
model = GPT4All(
    model_name=MODEL_NAME, model_path='Model', device='cpu', verbose=False)

# with model.chat_session():
with model.chat_session():
    print('-------------------')
    while True:
        context = input(Fore.GREEN + 'Введите текст: ' + Style.RESET_ALL)
        result = model.generate(prompt=context, temp=0)

        print(Fore.BLUE + 'Ответ: ' + Style.RESET_ALL, result)
        print(model.current_chat_session)
