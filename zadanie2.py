# Задание 2. EmailWorker: Wait/Pulse вместо пустого цикла
import threading
import time
from collections import deque

mail_queue = deque()
cond = threading.Condition()   # монитор с Wait/Pulse
running = True
empty_checks = 0               # холостые пробуждения без письма


def email_worker():
    global empty_checks
    while True:
        with cond:
            while not mail_queue and running:
                cond.wait()                      # Monitor.Wait: спим, CPU не тратим
                if not mail_queue and running:
                    empty_checks += 1            # проснулись зря
            if not mail_queue and not running:
                return                           # очередь пуста и работа закончена
            letter = mail_queue.popleft()
        print(f"Отправлено письмо: {letter}")


def add_letter(text):
    with cond:
        mail_queue.append(text)
        cond.notify()                            # Monitor.Pulse: будим воркера
    print(f"Принято письмо: {text}")


worker = threading.Thread(target=email_worker)
worker.start()

start = time.perf_counter()
for i in range(1, 4):
    time.sleep(0.5)
    add_letter(f"Письмо №{i}")

time.sleep(2 - (time.perf_counter() - start))   # всего работаем 2 секунды

with cond:
    running = False
    cond.notify_all()                            # будим воркера для завершения
worker.join()

print(f"Холостых проверок (emptyChecks): {empty_checks}")
