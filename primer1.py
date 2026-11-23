# Пример 1. Счётчик: гонка данных и решение через Monitor (Lock)
import threading
import time

THREADS = 8
INCREMENTS = 5_000
counter = 0
gate = threading.Lock()

def unsafe_worker():
    global counter
    for _ in range(INCREMENTS):
        value = counter
        time.sleep(0)
        counter = value + 1


def safe_worker():
    global counter
    for _ in range(INCREMENTS):
        gate.acquire()
        try:
            value = counter
            time.sleep(0)
            counter = value + 1
        finally:
            gate.release()


def run(worker, title):
    global counter
    counter = 0
    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"{title}: ожидалось {THREADS * INCREMENTS}, получили {counter}")


run(unsafe_worker, "Без блокировки")
run(safe_worker, "С Monitor (Lock)")
