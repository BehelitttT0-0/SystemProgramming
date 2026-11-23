# Пример 6. Лайвлок (потоки бесконечно уступают друг другу) и решение через Jitter
import random
import threading
import time

ATTEMPTS = 8
lock_a = threading.Lock()
lock_b = threading.Lock()
start_gate = threading.Barrier(2)  # оба потока стартуют одновременно


def worker(name, first, second, jitter):
    start_gate.wait()
    for attempt in range(1, ATTEMPTS + 1):
        first.acquire()
        time.sleep(0.1)  # оба потока успевают взять свой первый ресурс
        if second.acquire(blocking=False):
            try:
                print(f"{name}: взял оба ресурса и работает (попытка {attempt})")
            finally:
                second.release()
                first.release()
            return
        print(f"{name}: попытка {attempt} - ресурс занят, уступаю")
        time.sleep(0.05)  # уступаем не мгновенно: второй поток тоже успевает отступить
        first.release()
        # без jitter - одинаковая пауза, с jitter - случайная
        time.sleep(random.uniform(0.05, 0.6) if jitter else 0.2)
    print(f"{name}: ЛАЙВЛОК - за {ATTEMPTS} попыток так и не вошёл")


def run(jitter, title):
    print(f"--- {title} ---")
    t1 = threading.Thread(target=worker, args=("Поток 1", lock_a, lock_b, jitter))
    t2 = threading.Thread(target=worker, args=("Поток 2", lock_b, lock_a, jitter))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print()


run(False, "Лайвлок: одинаковая задержка")
run(True, "Решение: случайная задержка (Jitter)")
