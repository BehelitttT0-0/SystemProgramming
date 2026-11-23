# Самостоятельное задание 5. Асинхронный генератор случайных чисел
import asyncio
import random
import time


async def get_random_number_async() -> int:
    await asyncio.sleep(1)
    return random.randint(1, 100)


async def main():
    start = time.perf_counter()

    n1 = await get_random_number_async()
    print(f"Число 1: {n1}")
    n2 = await get_random_number_async()
    print(f"Число 2: {n2}")
    n3 = await get_random_number_async()
    print(f"Число 3: {n3}")

    print(f"Сумма: {n1 + n2 + n3}")
    print(f"Затрачено времени: {time.perf_counter() - start:.1f} с")


asyncio.run(main())
