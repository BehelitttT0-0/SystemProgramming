# Задание 2. Агрегатор курсов валют (параллельно через gather)
import asyncio
import time


async def get_rate_bank_a() -> float:
    await asyncio.sleep(1.0)
    return 78.50


async def get_rate_bank_b() -> float:
    await asyncio.sleep(1.5)
    return 79.10


async def get_rate_bank_c() -> float:
    await asyncio.sleep(2.0)
    return 78.80


async def main():
    start = time.perf_counter()

    # все три запроса стартуют одновременно
    rates = await asyncio.gather(
        get_rate_bank_a(),
        get_rate_bank_b(),
        get_rate_bank_c(),
    )

    print(f"Банк A: {rates[0]}")
    print(f"Банк B: {rates[1]}")
    print(f"Банк C: {rates[2]}")
    print(f"Средний курс: {sum(rates) / len(rates):.2f}")
    print(f"Затрачено времени: {time.perf_counter() - start:.1f} с")


asyncio.run(main())
