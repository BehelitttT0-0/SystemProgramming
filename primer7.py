# Пример 7. Обычный lock против Semaphore
import asyncio
import threading
import time

TASKS = 6
DELAY = 1
SLOTS = 3

# Часть 1. Обычный lock: пускает по одному
my_lock = threading.Lock()


def process_with_lock(n):
    with my_lock:
        print(f"Задача {n}: ВОШЛА и работает")
        time.sleep(DELAY)
        print(f"Задача {n}: ВЫШЛА")


def run_lock():
    print("--- Обычный lock ---")
    start = time.perf_counter()
    threads = [threading.Thread(target=process_with_lock, args=(i,))
               for i in range(1, TASKS + 1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Время с lock: {time.perf_counter() - start:.1f} с\n")


# Часть 2. Semaphore: пускает пачками по 3
async def process_data_async(n, semaphore):
    await semaphore.acquire()
    try:
        print(f"Задача {n}: ВОШЛА и работает")
        await asyncio.sleep(DELAY)
        print(f"Задача {n}: ВЫШЛА")
    finally:
        semaphore.release()


async def run_semaphore():
    print("--- Semaphore на 3 места ---")
    start = time.perf_counter()
    semaphore = asyncio.Semaphore(SLOTS)
    tasks = [process_data_async(i, semaphore) for i in range(1, TASKS + 1)]
    await asyncio.gather(*tasks)
    print(f"Время с Semaphore: {time.perf_counter() - start:.1f} с")


run_lock()
asyncio.run(run_semaphore())