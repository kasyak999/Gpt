import time

qwe = 'qwqwqwqwqwqwqq'

for char in qwe:
    print(char, end='', flush=True)  # Выводит символ без новой строки
    time.sleep(0.01)  # Ждет 0.5 секунды перед выводом следующего символа

print()  # Переход на новую строку после завершения