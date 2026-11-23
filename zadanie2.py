# Задание 2. EmailWorker: Wait/Pulse вместо пустого цикла
import threading
import time
from collections import deque

mail_queue = deque()
cond = threading.Condition()
running = True
empty_checks = 0


def email_worker():
    global empty_checks
    while True:
        with cond:
            while not mail_queue and running:
                cond.wait()
                if not mail_queue and running:
                    empty_checks += 1
            if not mail_queue and not running:
                return
            letter = mail_queue.popleft()
        print(f"Отправлено письмо: {letter}")


def add_letter(text):
    with cond:
        mail_queue.append(text)
        cond.notify()
    print(f"Принято письмо: {text}")


worker = threading.Thread(target=email_worker)
worker.start()

start = time.perf_counter()
for i in range(1, 4):
    time.sleep(0.5)
    add_letter(f"Письмо №{i}")

time.sleep(2 - (time.perf_counter() - start))

with cond:
    running = False
    cond.notify_all()
worker.join()

print(f"Холостых проверок (emptyChecks): {empty_checks}")
