# Задание 4. Фоновый расчёт с прогрессом (аналог Task.Run)
import asyncio
import threading
import time

STEPS = 5
DELAY = 0.6


def batch_processing():
    """Тяжёлая синхронная работа - выполняется в отдельном потоке."""
    for step in range(1, STEPS + 1):
        print(f"Шаг {step} из {STEPS} (поток: {threading.current_thread().name})")
        time.sleep(DELAY)
    return "Обработка завершена"


async def main():
    print(f"Главный поток: {threading.current_thread().name}")

    # asyncio.to_thread - аналог Task.Run: работа уходит в фоновый поток
    task = asyncio.create_task(asyncio.to_thread(batch_processing))
    print("Пакетная обработка запущена, главный поток не заблокирован")

    result = await task
    print(result)


asyncio.run(main())
