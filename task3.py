# Задание 3. Обработка платежа с проверкой исключений
import asyncio

LIMIT = 50_000


async def process_payment_async(amount: float) -> str:
    await asyncio.sleep(0.5)
    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")
    if amount > LIMIT:
        raise RuntimeError(f"Превышен лимит транзакции ({LIMIT})")
    return "Успешно"


async def try_pay(amount: float):
    try:
        # await обязателен, иначе исключение не будет перехвачено
        result = await process_payment_async(amount)
        print(f"Платёж {amount}: {result}")
    except ValueError as e:
        print(f"Платёж {amount}: ошибка суммы - {e}")
    except RuntimeError as e:
        print(f"Платёж {amount}: операция недопустима - {e}")


async def main():
    await try_pay(1500)
    await try_pay(-200)
    await try_pay(75_000)


asyncio.run(main())
