# Задание 4. Semaphore: не больше 3 одновременных запросов к платёжному шлюзу
import asyncio
import time

REQUESTS = 10
MAX_CONNECTIONS = 3   # лимит внешнего сервера
DELAY = 1             # время одного запроса, секунды

active = 0            # сколько запросов выполняется прямо сейчас
max_active = 0        # рекорд одновременных запросов


async def check_payment_async(n, semaphore):
    global active, max_active
    await semaphore.acquire()            # аналог WaitAsync(): ждём свободный слот
    try:
        active += 1
        max_active = max(max_active, active)
        print(f"Запрос {n}: отправлен (активных: {active})")
        await asyncio.sleep(DELAY)       # имитация сетевого запроса
        print(f"Запрос {n}: ответ получен")
    finally:
        active -= 1
        semaphore.release()              # освобождаем слот


async def main():
    start = time.perf_counter()
    semaphore = asyncio.Semaphore(MAX_CONNECTIONS)
    await asyncio.gather(*(check_payment_async(i, semaphore) for i in range(1, REQUESTS + 1)))
    print(f"Максимум одновременных запросов: {max_active}")
    print(f"Затрачено времени: {time.perf_counter() - start:.1f} с")


asyncio.run(main())
